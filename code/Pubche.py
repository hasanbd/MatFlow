import pandas as pd
from . import utils
import os
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
    # data.describe()
    utils.ShowHistogramCharts(data, 'extraction-pubChem')
    utils.SaveDataToOutput(data, 'extraction-pubChem')
    utils.LoadDataFromOutput('extraction-pubChem')