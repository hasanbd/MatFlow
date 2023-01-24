import pandas as pd

from . import utils
from . import features

import tqdm.notebook
tqdm.notebook.tqdm_notebook.pandas()
def experimental():
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
    utils.ShowHistogramCharts(data, 'dataset-experimental')
    utils.SaveDataToOutput(data, 'dataset-experimental')
    utils.LoadDataFromOutput('dataset-experimental')