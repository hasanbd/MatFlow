import pandas as pd
import numpy as np
from . import utils
import os

import re
from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfparser import PDFParser

def deep4che():
    data = pd.read_csv('./rawData/Deep4Chem/DB for chromophore_Sci_Data_rev02.csv')
    # Loading the verified data and correcting any issue we found
    df=pd.read_csv('./rawData/Deep4Chem/DoubleCheck-High Extinction.csv')
    temp = df[['Tag','Should be']]
    temp['log(Epsilon)'] = temp['Should be'].apply(lambda x: x if x != 'x' else np.nan).astype('float').apply(np.log10)
    data = data.merge(temp, on='Tag', how='left')
    data['log(Epsilon)'] = data['log(Epsilon)'].fillna(data['log(e/mol-1 dm3 cm-1)'])

    data.drop(['Tag', 'Reference', 'Should be', 'log(e/mol-1 dm3 cm-1)'], axis='columns', inplace=True)

    ## Removing rows that don't have a log(Epsilon)
    data = data[data['log(Epsilon)'].isnull() == False].copy().reset_index(drop = True)
    #print('Total Count: ' + str(len(data)))
    #data.head(1)

    data = data[data['log(Epsilon)'].isnull() == False].copy().reset_index(drop=True)
    data.columns = data.columns.str.replace('_', ' ').str.title()
    utils.DropAllNullColumns(data)
    utils.ConvertStringColumnsToInt(data)
    utils.ConvertFloatColumnsToIntegerIfNoDataLoss(data)
    utils.CompressIntegerColumns(data)
    utils.InspectColumnValues(data)
    utils.ShowHistogramCharts(data,'extraction-deep4Chem')
    utils.SaveDataToOutput(data, 'extraction-deep4Chem')
    utils.LoadDataFromOutput('extraction-deep4Chem')

def dynamocs():
    # display(HTML("<style>.container { width:100% !important; }</style>"))
    def GetPageText(page, resourceManager):
        result = StringIO()
        converter = TextConverter(resourceManager, result,
                                  laparams=LAParams(boxes_flow=1, char_margin=1000, line_margin=10,
                                                    detect_vertical=True, all_texts=False))
        PDFPageInterpreter(resourceManager, converter).process_page(page)

        return result.getvalue()

    pagesRaw = []
    with open('./rawData/Dyomics/Dyomics_2017.pdf', 'rb') as in_file:
        resourceManager = PDFResourceManager()

        count = 0
        for page in PDFPage.create_pages(PDFDocument(PDFParser(in_file))):
            pageText = GetPageText(page, resourceManager)
            pagesRaw.append({'page number': count, 'id': page.pageid, 'page text': pageText})
            count += 1

    def GetDyeInformationText(text):
        dyeInformation = re.split('(.+)\n(?=Absorption.+)', text)
        if (len(dyeInformation) == 1):
            return None

        results = []

        #print(dyeInformation)
        for i in range(1, len(dyeInformation), 2):
            results.append([dyeInformation[i], dyeInformation[i + 1]])

        return results

    pages = pd.DataFrame(pagesRaw)
    pages['dye information text list'] = pages['page text'].apply(GetDyeInformationText)
    pages.head(1)

    data = pages[pages['dye information text list'].isnull() == False]['dye information text list'] \
        .apply(lambda x: pd.Series(x)) \
        .stack() \
        .reset_index(level=1, drop=True) \
        .apply(lambda x: pd.Series(x)) \
        .rename(columns={0: 'name', 1: 'dye information text'}) \
        .join(pages) \
        .reset_index(drop=True)

    #data.head(1)

    def BreakOutTextChunks(dyeText):
        dyeText = dyeText.strip()
        result = {}
        temp = re.search('^Absorption/emission max.+\n', dyeText)
        if (temp):
            result['absorption text'] = temp.group(0).strip()
        else:  # Handling page 91's different format
            temp = re.search('^Absorption max.+\n(Emission max.+)*', dyeText)
            result['absorption text'] = temp.group(0).strip()

        dyeText = dyeText.replace(result['absorption text'], '').strip()
        temp = re.search('^Molar absorbance.+\n', dyeText)
        result['molar absorbance text'] = temp.group(0).strip()
        dyeText = dyeText.replace(result['molar absorbance text'], '').strip()

        temp = re.search('.+Productnumber.*\n', dyeText)
        tableHeader = temp.group(0).strip()
        temp = dyeText.split(tableHeader)
        result['comments text'] = temp[0].strip()
        result['table information text'] = temp[1].strip()

        return result

    data = data['dye information text'].apply(BreakOutTextChunks) \
        .apply(lambda x: pd.Series(x)) \
        .join(data)

    #data.head(1)

    def GetMolarAbsorbance(molarAbsorbanceText):
        return re.search('(([0-9]|,)+)', molarAbsorbanceText).group(0)

    data['molar absorbance'] = data['molar absorbance text'].apply(GetMolarAbsorbance)
    #data.head(1)

    data = data['table information text'].apply(lambda x: x.splitlines()) \
        .apply(lambda x: pd.Series(x)) \
        .stack() \
        .reset_index(level=1, drop=True) \
        .to_frame('table information row text') \
        .join(data) \
        .reset_index(drop=True)

    #data.head(1)

    def GetWeight(line):
        if (len(line) <= 10):
            return 'Error: Short string found'

        weightText = re.search('([0-9]+\.[0-9]+)', line)
        if (weightText == None):
            if (re.search('^[^0-9]+$', line)):
                return 'Error: Label found'

            if (re.search('^[A-Z]*([0-9]| |,)+$', line)):
                return 'Error: Graph axis found'

            if (re.search('[0-9]+nm', line)):
                return 'Error: Label found'

            return 'Error: No weight found'

        return weightText.group(0)

    def GetTableRowInformation(tableInformationRow):
        result = {}
        result['weight'] = GetWeight(tableInformationRow)

        if ('Error' in result['weight']):
            return result

        temp = tableInformationRow.split(result['weight'])
        result['available modification'] = temp[0].strip()

        t = re.split('([^\s]+)', temp[1])
        result['product number'] = t[len(t) - 2]

        result['formula'] = temp[1].replace(result['product number'], '').strip()

        return result

    data = data['table information row text'].apply(GetTableRowInformation) \
        .apply(lambda x: pd.Series(x)) \
        .join(data)

    #data.head(1)

    # Dropping MitoDy-1 that have errors since one row is correct except for the product number and formula
    data = data[
        (data['name'] != 'MitoDy-1') | ((data['name'] == 'MitoDy-1') & (data['weight'].str.contains('Error') == False))]

    # Fixing product number
    mask = data['name'] == 'MitoDy-1'
    data.loc[mask, 'product number'] = 'MTD-1'
    data.loc[mask, 'formula'] = 'C21H25N2O3 * BF4'

    # Fixing some spaces in names
    data['name'] = data['name'].str.strip()

    if (len(data[data['weight'] == 'Error: No weight found']) != 0):
        raise 'new unhandled errors found'

    data = data[(data['weight'].str.contains('Error') == False)]

    utils.InspectColumnValues(data[['available modification', 'product number', 'formula', 'weight']])

    # for column in ['product number', 'formula', 'weight', 'molar absorbance', 'emission max']:
    #     #print('All values for ' + column)
    #
    #     #print(data.columns.unique())
    #     #print()
    data.drop(data.columns[data.columns.str.contains(' text')], axis='columns', inplace=True)
    data.drop(['page number', 'id'], axis='columns', inplace=True)
    temp = pd.read_csv('./rawData/Dyomics/SmilesData.csv')
    temp['Name'] = temp['Name'].str.upper()
    temp['Smiles'] = temp['Correct Smiles'].fillna(temp['Generated Smiles'])
    temp = temp[['Name', 'Smiles']]
    # temp

    data = data.merge(temp, left_on='name', right_on='Name')
    data.drop(['Name'], axis='columns', inplace=True)
    #print('Total Count: ' + str(len(data)))
    #data.head(1)

    data.columns = data.columns.str.replace('_', ' ').str.title()
    utils.DropAllNullColumns(data)
    utils.ConvertStringColumnsToInt(data)
    utils.ConvertStringColumnsToFloat(data)
    utils.CompressIntegerColumns(data)
    ##data.info()
    utils.InspectColumnValues(data)
    #data.describe()
    utils.ShowHistogramCharts(data,'extraction-dyomics')
    utils.SaveDataToOutput(data, 'extraction-dyomics')
    utils.LoadDataFromOutput('extraction-dyomics')
def Photoche():
    # display(HTML("<style>.container { width:100% !important; }</style>"))
    data = pd.read_csv('./rawData/PhotoChemCAD3/2018_03 PCAD3.csv')
    temp = pd.read_csv('./rawData/PhotoChemCAD3/SmilesData.csv')
    temp['Smiles'] = temp['Correct Smiles'].fillna(temp['Generated Smiles'])
    # temp.head(1)

    data = data.merge(temp[['Structure', 'Smiles']], on='Structure')
    #print('Total Count: ' + str(len(data)))
    #data.head(1)
    data.columns = data.columns.str.replace('_', ' ').str.title()
    utils.DropAllNullColumns(data)
    utils.ConvertStringColumnsToInt(data)
    utils.ConvertFloatColumnsToIntegerIfNoDataLoss(data)
    utils.CompressIntegerColumns(data)
    ##data.info()
    utils.InspectColumnValues(data)
    #data.describe()
    utils.ShowHistogramCharts(data,'extraction-photoChemCAD3')
    utils.SaveDataToOutput(data, 'extraction-photoChemCAD3')
    utils.LoadDataFromOutput('extraction-photoChemCAD3')
def pubche():

    temp = []
    dataDirectory = './rawData/PubChem/'
    for file in os.listdir(dataDirectory):
        temp.append(pd.read_csv(os.path.join(dataDirectory, file)))

    data = pd.concat(temp).drop_duplicates(ignore_index=True)
    data.columns = data.columns.str.replace('_', ' ').str.title()
    utils.DropAllNullColumns(data)
    utils.ConvertStringColumnsToInt(data)
    utils.ConvertFloatColumnsToIntegerIfNoDataLoss(data)
    utils.CompressIntegerColumns(data)
    ##data.info()
    utils.InspectColumnValues(data)
    #data.describe()
    utils.ShowHistogramCharts(data,'extraction-pubChem')
    utils.SaveDataToOutput(data, 'extraction-pubChem')
    utils.LoadDataFromOutput('extraction-pubChem')

def run_all():
    
    st.write('done')
    deep4che()
#     dynamocs()
#     Photoche()
#     pubche()

