import pandas as pd
import numpy as np
from rdkit import Chem
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

from IPython.core.display import display, HTML

from . import utils
from . import features

import tqdm.notebook
tqdm.notebook.tqdm_notebook.pandas()

def Experimental():
    data = pd.read_csv('./rawData/Experimental_SMILES_Predictions.csv')

    data.rename(columns={'SMILES': 'Smiles', 'Min ε': 'Min Epsilon', 'Max ε': 'Max Epsilon', 'Dye': 'Source Key',
                         'TD-DFT μ (D)': 'TD-DFT (Debye)'}, inplace=True)

    data = data[['Source Key', 'TD-DFT (Debye)', 'Min Epsilon', 'Max Epsilon', 'Smiles']]
    data = data.join(data['Smiles'].progress_apply(features.ComputeAllFeatures).apply(
        lambda x: pd.Series(x, dtype='object'))).fillna(0)
    # Standardizing Column names
    data.columns = data.columns.str.replace('_', ' ').str.title()

    # Compressing data
    utils.ConvertFloatColumnsToIntegerIfNoDataLoss(data)
    utils.CompressIntegerColumns(data)
    data.drop(['Smiles', 'Inchikey'], axis='columns', inplace=True)
    utils.RemoveStaticColumns(data)
    # print('-----------------')
    # print('-----------------')
    # print('-----------------')
    utils.RemoveDuplicateColumns(data)
    # data.info()
    utils.InspectColumnValues(data)
    # data.describe()
    utils.ShowHistogramCharts(data,'dataset-experimental')
    utils.SaveDataToOutput(data, 'dataset-experimental')
    utils.LoadDataFromOutput('dataset-experimental')
def Training():
    # display(HTML("<style>.container { width:100% !important; }</style>"))
    temp = utils.LoadDataFromOutput('extraction-deep4Chem')
    temp['Source'] = 'Deep4Chem'
    # print(len(temp))
    # temp.head(1)
    temp['Epsilon'] = temp['Log(Epsilon)'].apply(lambda x: 10 ** x)

    temp['Smiles'] = temp['Chromophore']
    temp.rename(columns={'Chromophore': 'Source Key'}, inplace=True)

    temp = temp[['Source', 'Source Key', 'Epsilon', 'Smiles']]

    data = temp.copy()
    st.write('11111')
    temp = utils.LoadDataFromOutput('extraction-PhotoChemCAD3')
    st.write('11112')
    temp['Source'] = 'PhotoChemCAD3'
    temp.columns = temp.columns.str.replace('_', ' ').str.title()
    # print(len(temp))
    # temp.head(1)
    temp.rename(columns={'Name': 'Source Key'}, inplace=True)

    temp = temp[['Source', 'Source Key', 'Epsilon', 'Smiles']]

    data = data.append(temp)
    temp = utils.LoadDataFromOutput('extraction-dyomics')
    temp['Source'] = 'Dyomics'
    temp.columns = temp.columns.str.replace('_', ' ').str.title()
    # print(len(temp))
    # temp.head(1)
    temp.rename(columns={'Molar Absorbance': 'Epsilon', 'Name': 'Source Key'}, inplace=True)

    temp = temp[['Source', 'Source Key', 'Epsilon', 'Smiles']]

    data = data.append(temp)
    data.reset_index(drop=True, inplace=True)
    # data
    temp = data['Smiles'].drop_duplicates().to_frame()

    temp = temp.join(temp['Smiles'].progress_apply(features.ComputeAllFeatures).apply(
        lambda x: pd.Series(x, dtype='object'))).fillna(0)

    data = data.merge(temp, on='Smiles')
    if ('Error' in data.columns):
        data = data[data['Error'] != True].reset_index(drop=True)
        data.drop(['Error'], axis='columns', inplace=True)
    data.columns = data.columns.str.replace('_', ' ').str.title()

    # Compressing data
    utils.ConvertFloatColumnsToIntegerIfNoDataLoss(data)
    utils.CompressIntegerColumns(data)
    utils.SaveDataToOutput(data, 'dataset-allKnownEpsilon')
    utils.LoadDataFromOutput('dataset-allKnownEpsilon')
    data.drop(['Source', 'Source Key', 'Smiles', 'Inchikey'], axis='columns', inplace=True)
    # data.head(1)
    limit = 800000
    # print('Number of entries >= 800K: ' + str(len(data[data['Epsilon'] >= limit])))
    data = data[data['Epsilon'] < limit].copy()

    # print('Columns with infinate values: ' + str(data.columns[np.isinf(data).any()].values))
    # print('Number of entries with infinate values: ' + str(len(data.index[np.isinf(data).any(1)])))

    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    utils.RemoveStaticColumns(data)
    # print('-----------------')
    # print('-----------------')
    # print('-----------------')
    utils.RemoveDuplicateColumns(data)
    # data.info()
    utils.InspectColumnValues(data)
    # data.describe()
    utils.ShowHistogramCharts(data,'dataset-training')

    def SplitData(data):
        validation = data.sample(frac=.1, random_state=82219)
        development_mask = pd.Series(True, index=data.index)
        development_mask[validation.index] = False
        development = data[development_mask].copy()
        development.reset_index(drop=True, inplace=True)
        validation.reset_index(drop=True, inplace=True)

        return development, validation

    development, validation = SplitData(data)
    utils.SaveDataToOutput(development, 'dataset-development')
    utils.LoadDataFromOutput('dataset-development')
    utils.SaveDataToOutput(validation, 'dataset-validation')
    utils.LoadDataFromOutput('dataset-validation')
    # print('Number of entries in development dataset: ' + str(len(development)))
    # print('Number of entries in validation dataset: ' + str(len(validation)))
    #
def unknown():
    # display(HTML("<style>.container { width:100% !important; }</style>"))
    data = utils.LoadDataFromOutput('extraction-pubChem')
    data['Source'] = 'PubChem'
    data.columns = data.columns.str.replace('_', ' ').str.title()
    # print(len(data))
    # data.head(1)
    data['Source Key'] = data['Cid'].astype(str)
    data.rename(columns={'Isosmiles': 'Smiles'}, inplace=True)
    data = data[['Source', 'Source Key', 'Smiles']]
    temp = data['Smiles'].drop_duplicates().to_frame()

    temp = temp.join(temp['Smiles'].progress_apply(features.ComputeAllFeatures).apply(
        lambda x: pd.Series(x, dtype='object'))).fillna(0)

    # Removing any entry that failed to compute all features
    temp = temp[temp['Total Atom Count'].isna() == False].drop_duplicates()

    data = data.merge(temp, on='Smiles')

    # len(data)
    data = data[data['Error'] != True].reset_index(drop=True)
    data.drop(['Error'], axis='columns', inplace=True)
    knownEpsilons = utils.LoadDataFromOutput('dataset-allKnownEpsilon')['Smiles'].progress_apply(
        lambda x: Chem.inchi.MolToInchiKey(Chem.MolFromSmiles(x))).to_list()

    data = data[data['InchiKey'].isin(knownEpsilons) == False].reset_index(drop=True)
    # len(data)
    data.drop(['InchiKey'], axis='columns', inplace=True)

    # Standardizing Column names
    data.columns = data.columns.str.replace('_', ' ').str.title()

    # Compressing data
    utils.ConvertFloatColumnsToIntegerIfNoDataLoss(data)
    utils.CompressIntegerColumns(data)
    utils.RemoveStaticColumns(data)
    # print('-----------------')
    # print('-----------------')
    # print('-----------------')
    utils.RemoveDuplicateColumns(data)
    # data.info()
    utils.InspectColumnValues(data)
    # data.describe()
    utils.ShowHistogramCharts(data,'dataset-unknownEpsilon')
    utils.SaveDataToOutput(data, 'dataset-unknownEpsilon')
    utils.LoadDataFromOutput('dataset-unknownEpsilon')

def run_all():
    Experimental()
    Training()
    unknown()
