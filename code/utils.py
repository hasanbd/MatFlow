# This file contains the various functions needed to process the raw data into a usable format

import os
import re
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

outputDirectory = './output'
tempDirectory = './temp'


def DropAllNullColumns(data):
    columnsToDrop = []
    for column in data.columns:
        if data[column].isnull().values.all():
            columnsToDrop.append(column)

    # print('Dropping all the following columns since all NaN values')
    # print(columnsToDrop)
    data.drop(columnsToDrop, axis=1, inplace=True)


def UpperCaseStringColumns(data):
    for column in data.columns:
        if (pd.api.types.infer_dtype(data[column]) == 'string'):
            # print(column + ': Upper Casing')
            data[column] = data[column].str.upper()


def CompressIntegerColumns(data):
    for column in data.columns:
        if (np.issubdtype(data[column].dtype, np.integer)):
            minValue = data[column].min()
            maxValue = data[column].max()

            info = np.iinfo
            if minValue >= 0:
                types = (np.uint8, np.uint16, np.uint32, np.uint64)
            else:
                types = (np.int8, np.int16, np.int32, np.int64)

            for t in types:
                if info(t).min <= minValue and maxValue <= info(t).max:
                    # print(column + ': Converting to ' + t.__name__)
                    data[column] = data[column].astype(t)
                    break


def ConvertFloatColumnsToIntegerIfNoDataLoss(data):
    for column in data.columns:
        try:
            if (np.issubdtype(data[column].dtype, np.float)):
                temp = data[column].astype(np.int64)

                if ((temp == data[column]).all()):
                    # print(column + ': Converting to ' + str(temp.dtype))
                    data[column] = temp
        except:
            pass


def ConvertStringColumnsToInt(data):
    for column in data.columns:
        if (pd.api.types.infer_dtype(data[column]) == 'string'):
            if data[column].isnull().values.any():
                continue

            if (data[column].apply(lambda x: re.match('^[0-9,-]+$', x) != None).all()):
                # print(column + ': Converting to int')
                data[column] = data[column].str.replace(',', '')
                data[column] = data[column].astype(np.int64)


def ConvertStringColumnsToFloat(data):
    for column in data.columns:
        if (pd.api.types.infer_dtype(data[column]) == 'string'):
            if data[column].isnull().values.any():
                continue

            if (data[column].apply(lambda x: re.match('^[0-9,-\.]+$', x) != None).all()):
                # print(column + ': Converting to float')
                data[column] = data[column].str.replace(',', '')
                data[column] = data[column].astype(np.float64)


def InspectColumnValues(data):
    for column in data.columns:
        try:
            values = data[column].unique()
            # print(column + ': ' + str(len(values)))
            # print(values[0:10])
            # print()
        except:
            print('Error with: ' + column)


def RemoveStaticColumns(data):
    # print('Removing columns with only one value')
    # for column in data.columns[data.nunique() == 1]:
    #     print(column + ' only has: ' + str(data[column].iloc[0]))

    data.drop(data.columns[data.nunique() == 1], inplace=True, axis='columns')


def RemoveDuplicateColumns(data):
    dups = []
    maxColumn = len(data.columns)
    for i in range(maxColumn):
        column1 = data.columns[i]

        for j in range(i + 1, maxColumn):
            column2 = data.columns[j]

            if (data[column1].equals(data[column2])):
                # print(column1 + ' == ' + column2)
                dups.append(column2)

    # print()
    # print('Removing duplicate columns')
    # print(dups)

    data.drop(columns=dups, axis='columns', inplace=True)





def ShowHistogramCharts(data,name):

    cnt = 0
    columnsToDisplay = data.select_dtypes(exclude='object').columns
    numberOfColumns = min(len(columnsToDisplay), 5)
    for i, column in enumerate(columnsToDisplay):
        if (i % numberOfColumns == 0):
            fig, axes = plt.subplots(ncols=numberOfColumns, figsize=(3 * numberOfColumns, 3), constrained_layout=True)
        sns.histplot(data[column], bins=20, ax=axes[i % numberOfColumns])
        if (i % numberOfColumns == numberOfColumns - 1):
            if cnt == 0:
                try:
                    if 'table' not in st.session_state:
                        st.session_state.table = []
                        st.session_state.graph=[]
                    pdd = pd.DataFrame(data.describe())

                    with st.expander('Processed data of '+name):
                        st.session_state.table.append({name:pdd})
                        st.table(pdd)
                    cnt += 1
                    st.session_state.graph.append({name:fig})
                except:
                    pass

            plt.show()

def savefigure(name,fig):
    if 'graph' not in st.session_state:
        st.session_state.graph=[]
    st.session_state.graph.append({name:fig})
def convert_df(df):
   return df.to_csv(index=False).encode('utf-8')

def SaveDataToOutput(data, name):
    if (os.path.exists(outputDirectory) == False):
        os.mkdir(outputDirectory)
    
    data.to_parquet(os.path.join(outputDirectory, name + '.gzip.parquet'), compression='gzip')
    csv = convert_df(df)
    st.download_button(
       "Press to Download",
       csv,
       name+".csv",
       "text/csv",
       key='download-csv'+name
        )


def LoadDataFromOutput(name):
    return pd.read_parquet(os.path.join(outputDirectory, name + '.gzip.parquet'))

def SaveDataToTemp(data, name):
    if (os.path.exists(tempDirectory) == False):
        os.mkdir(tempDirectory)
    data.to_parquet(os.path.join(tempDirectory, name + '.gzip.parquet'), compression='gzip')


def LoadDataFromTemp(name):
    return pd.read_parquet(os.path.join(tempDirectory, name + '.gzip.parquet'))


def RotateAllXText(axes):
    for ax in axes:
        plt.setp(ax.get_xticklabels(), rotation=30, horizontalalignment='right')
