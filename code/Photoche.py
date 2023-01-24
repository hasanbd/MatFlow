import pandas as pd
from . import utils
def photoche():
    data = pd.read_csv('./rawData/PhotoChemCAD3/2018_03 PCAD3.csv')
    temp = pd.read_csv('./rawData/PhotoChemCAD3/SmilesData.csv')
    temp['Smiles'] = temp['Correct Smiles'].fillna(temp['Generated Smiles'])
    # temp.head(1)

    data = data.merge(temp[['Structure', 'Smiles']], on='Structure')
    # print('Total Count: ' + str(len(data)))
    # data.head(1)
    data.columns = data.columns.str.replace('_', ' ').str.title()
    utils.DropAllNullColumns(data)
    utils.ConvertStringColumnsToInt(data)
    utils.ConvertFloatColumnsToIntegerIfNoDataLoss(data)
    utils.CompressIntegerColumns(data)
    ##data.info()
    utils.InspectColumnValues(data)
    # data.describe()
    utils.ShowHistogramCharts(data, 'extraction-photoChemCAD3')
    utils.SaveDataToOutput(data, 'extraction-photoChemCAD3')
    utils.LoadDataFromOutput('extraction-photoChemCAD3')