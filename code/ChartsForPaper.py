import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import sklearn.metrics as skm
import dask
import dask.dataframe as dd

from sklearn.utils import resample

from dask.diagnostics import ProgressBar
import sys
import multiprocessing as mp

pbar = ProgressBar()
import dask
import dask.dataframe as dd
from dask.diagnostics import ProgressBar

import ast

from IPython.core.display import display, HTML

import tqdm.notebook
tqdm.notebook.tqdm_notebook.pandas()

from . import utils
from . import labels
from . import train

def Overall_Data():
    # display(HTML("<style>.container { width:100% !important; }</style>"))
    sns.set_theme(style="whitegrid", font_scale=1.1, font='Calibri')
    sns.despine(left=True)

    colors = ['#e66101', '#fdb863', '#b2abd2', '#5e3c99']
    sns.set_palette(sns.color_palette(colors))
    figureSize = (4, 3)
    padInches = 0.05
    data = utils.LoadDataFromOutput('dataset-allKnownEpsilon')
    # data.head(1)

    limit = 800000
    print('Number of entries >= 800K: ' + str(len(data[data['Epsilon'] >= limit])))
    data = data[data['Epsilon'] < limit].copy()

    numberColumns = data.select_dtypes(exclude='object').columns
    # print(
    #     'Columns with infinate values: ' + str(data[numberColumns].columns[np.isinf(data[numberColumns]).any()].values))
    # print('Number of entries with infinate values: ' + str(
    #     len(data[numberColumns].index[np.isinf(data[numberColumns]).any(1)])))
    data.replace([np.inf, -np.inf], np.nan, inplace=True)
    data.dropna(inplace=True)
    data.reset_index(drop=True, inplace=True)
    graphData = data[data['Epsilon'] != -1].copy()
    graphData['IsHigh'] = graphData['Epsilon'] >= 150000
    graphData = graphData.groupby(['Source']).agg(Total=('IsHigh', 'count'), High_ε=('IsHigh', 'sum')).reset_index()

    temp = graphData.sum()
    temp['Source'] = 'Total'
    temp.to_frame().T

    graphData = pd.concat([temp.to_frame().T, graphData])
    # graphData

    graphData.columns = graphData.columns.str.replace('_', ' ')
    graphData['Low ' + labels.Epsilon] = graphData['Total'] - graphData['High ' + labels.Epsilon]
    graphData = graphData[['Source', 'Low ' + labels.Epsilon, 'High ' + labels.Epsilon]].melt(id_vars='Source')

    g = sns.barplot(data=graphData, x='Source', y='value', hue='variable', palette=[colors[1], colors[0]])
    g.set_ylabel('Count')
    for ax in g.axes.containers:
        g.axes.bar_label(ax, label_type='edge')

    g.legend(title='');
    g.figure.tight_layout()
    g.get_figure().savefig('./output/chart-overall-data.png', bbox_inches='tight', dpi=600)

def Ovall_RandomForest_Classifaications():
    sns.set_theme(style="whitegrid", font_scale=1.1, font='Calibri')
    sns.despine(left=True)

    colors = ['#e66101', '#fdb863', '#b2abd2', '#5e3c99']
    sns.set_palette(sns.color_palette(colors))
    figureSize = (4, 3)
    padInches = 0.05
    development = utils.LoadDataFromOutput('dataset-development')
    validation = utils.LoadDataFromOutput('dataset-validation')
    print('Developement Dataset Count: ' + str(len(development)))
    print('Validate Dataset Count: ' + str(len(validation)))

    data = pd.concat([development, validation]).reset_index(drop=True)
    # print('Total Count: ' + str(len(data)))
    # print('Number of Training Features: ' + str(len(development.columns)))
    # development.head(1)
    models = pd.read_parquet('./code/trainedModels-RandomForestClassifier.gzip.parquet')
    models['Model Params'] = models['Model'].apply(ast.literal_eval)
    # models.head(1)
    def ComputeAllowsLowAccuracy(threshold, data):
        _, y = train.GetXandY(data)
        y = train.ComputeLabel(y, threshold)
        y_pred = data['Epsilon'].apply(lambda x: 'low ε')
        return skm.accuracy_score(y, y_pred)

    temp = models.copy()
    # print(temp)
    temp = temp.join(temp['Model Params'].apply(lambda x: pd.Series(x, dtype='object')))
    temp['Accuracy'] = temp['Accuracy'].apply(lambda x: np.round(x, 2))
    # %%
    temp['Total Information Used'] = temp.apply(
        lambda row: train.ComputeTotalInfomationUsed(row, len(development.columns)), axis='columns')
    maxAccuracy = temp.groupby(['Threshold']).max('Accuracy')['Accuracy'].reset_index()
    # maxAccuracy
    totalInformationUsed = temp.merge(maxAccuracy, on=['Threshold', 'Accuracy']).groupby(['Threshold']).min('Total Information Used')[['Accuracy', 'Total Information Used']].reset_index()
    mostAccurateAndPreciseWithTheLeastAmountOfInformation = temp.merge(totalInformationUsed,on=['Threshold', 'Accuracy','Total Information Used']).groupby(['Threshold']).max('Precision (High ε)').reset_index()
    bestModels = temp.merge(mostAccurateAndPreciseWithTheLeastAmountOfInformation[['Threshold', 'Accuracy', 'Total Information Used', 'Precision (High ε)']],on=['Threshold', 'Accuracy', 'Total Information Used', 'Precision (High ε)'])
    bestModels = bestModels.groupby(['Threshold']).first().reset_index()
    bestModels['Model'] = bestModels.progress_apply(lambda x: train.TrainRandomForestClassifier(x['Model Params'], x['Threshold'], development), axis='columns')
    bestModels['Random Forest Classifier(Development)'] = bestModels.apply(lambda x: train.ComputeClassifierAccuracy(x['Model'], x['Threshold'], development), axis='columns')
    bestModels['Random Forest Classifier(Validation)'] = bestModels.apply(lambda x: train.ComputeClassifierAccuracy(x['Model'], x['Threshold'], validation), axis='columns')
    bestModels['Always Low ε(Development)'] = bestModels.apply(lambda x: ComputeAllowsLowAccuracy(x['Threshold'], development), axis='columns')
    bestModels['Always Low ε(Validation)'] = bestModels.apply(lambda x: ComputeAllowsLowAccuracy(x['Threshold'], validation), axis='columns')
    bestModels.head(1)
    #
    #
    classifierModelUsed = bestModels.iloc[1]
    #
    low = data[data['Epsilon'] < classifierModelUsed['Threshold']].reset_index(drop=True).copy()
    high = data[data['Epsilon'] >= classifierModelUsed['Threshold']].reset_index(drop=True).copy()
    total = len(low) + len(high)
    #
    percentageLowRuns = []
    for lowPercent in range(50, 100, 2):
        lowPercent = lowPercent / 100
        numberOfHighsNeeded = int(len(low) / lowPercent - len(low))
        newHighs = resample(high, n_samples=numberOfHighsNeeded, random_state=82219)
        lowEpsilonDevelopment, lowEpsilonValidation = train.SplitData(pd.concat([low, newHighs], ignore_index=True))
        percentageLowRuns.append([lowPercent, lowEpsilonDevelopment, lowEpsilonValidation])
    #
    percentageLowRuns = pd.DataFrame(percentageLowRuns, columns=['Percentage Low ε', 'Development', 'Validation'])
    percentageLowRuns['Model'] = percentageLowRuns.progress_apply(lambda x: train.TrainRandomForestClassifier(classifierModelUsed['Model Params'],classifierModelUsed['Threshold'], x['Development']), axis='columns')
    percentageLowRuns['Random Forest Classifier(Development)'] = percentageLowRuns.apply(lambda x: train.ComputeClassifierAccuracy(x['Model'], classifierModelUsed['Threshold'], x['Development']),axis='columns')
    percentageLowRuns['Random Forest Classifier(Validation)'] = percentageLowRuns.apply(lambda x: train.ComputeClassifierAccuracy(x['Model'], classifierModelUsed['Threshold'], x['Validation']),axis='columns')
    percentageLowRuns['Always Low ε(Development)'] = percentageLowRuns.apply(lambda x: ComputeAllowsLowAccuracy(classifierModelUsed['Threshold'], x['Development']), axis='columns')
    percentageLowRuns['Always Low ε(Validation)'] = percentageLowRuns.apply(lambda x: ComputeAllowsLowAccuracy(classifierModelUsed['Threshold'], x['Validation']), axis='columns')
    fig, axes = plt.subplots(ncols=2, figsize=(11, 4), constrained_layout=True)
    #
    graphData = bestModels[['Threshold', 'Random Forest Classifier(Development)', 'Random Forest Classifier(Validation)','Always Low ε(Development)', 'Always Low ε(Validation)']]
    graphData = graphData.melt(id_vars=['Threshold'])
    graphData['Threshold'] = graphData['Threshold'] / 1000

    g = sns.lineplot(data=graphData, x='Threshold', y='value', hue='variable', ax=axes[0])
    g.set(ylim=(.9, 1), ylabel='Accuracy', xlabel=labels.EpsilonFull);
    ##error##
    g
    # g.legend_.set_bestModels['Model'] = bestModels.progress_apply(lambda x: train.TrainRandomForestClassifier(x['Model Params'], x['Threshold'], development), axis='columns')
    bestModels['Random Forest Classifier(Development)'] = bestModels.apply(
        lambda x: train.ComputeClassifierAccuracy(x['Model'], x['Threshold'], development), axis='columns')
    bestModels['Random Forest Classifier(Validation)'] = bestModels.apply(
        lambda x: train.ComputeClassifierAccuracy(x['Model'], x['Threshold'], validation), axis='columns')
    bestModels['Always Low ε(Development)'] = bestModels.apply(
        lambda x: ComputeAllowsLowAccuracy(x['Threshold'], development), axis='columns')
    bestModels['Always Low ε(Validation)'] = bestModels.apply(
        lambda x: ComputeAllowsLowAccuracy(x['Threshold'], validation), axis='columns')
    bestModels.head(1)
    #
    #
    classifierModelUsed = bestModels.iloc[1]

    low = data[data['Epsilon'] < classifierModelUsed['Threshold']].reset_index(drop=True).copy()
    high = data[data['Epsilon'] >= classifierModelUsed['Threshold']].reset_index(drop=True).copy()
    total = len(low) + len(high)

    percentageLowRuns = []
    for lowPercent in range(50, 100, 2):
        lowPercent = lowPercent / 100
        numberOfHighsNeeded = int(len(low) / lowPercent - len(low))
        newHighs = resample(high, n_samples=numberOfHighsNeeded, random_state=82219)
        lowEpsilonDevelopment, lowEpsilonValidation = train.SplitData(pd.concat([low, newHighs], ignore_index=True))

        percentageLowRuns.append([lowPercent, lowEpsilonDevelopment, lowEpsilonValidation])

    percentageLowRuns = pd.DataFrame(percentageLowRuns, columns=['Percentage Low ε', 'Development', 'Validation'])

    percentageLowRuns['Model'] = percentageLowRuns.progress_apply(
        lambda x: train.TrainRandomForestClassifier(classifierModelUsed['Model Params'],
                                                    classifierModelUsed['Threshold'],
                                                    x['Development']), axis='columns')
    percentageLowRuns['Random Forest Classifier(Development)'] = percentageLowRuns.apply(
        lambda x: train.ComputeClassifierAccuracy(x['Model'], classifierModelUsed['Threshold'], x['Development']),
        axis='columns')
    percentageLowRuns['Random Forest Classifier(Validation)'] = percentageLowRuns.apply(
        lambda x: train.ComputeClassifierAccuracy(x['Model'], classifierModelUsed['Threshold'], x['Validation']),
        axis='columns')
    percentageLowRuns['Always Low ε(Development)'] = percentageLowRuns.apply(
        lambda x: ComputeAllowsLowAccuracy(classifierModelUsed['Threshold'], x['Development']), axis='columns')
    percentageLowRuns['Always Low ε(Validation)'] = percentageLowRuns.apply(
        lambda x: ComputeAllowsLowAccuracy(classifierModelUsed['Threshold'], x['Validation']), axis='columns')
    # title('Model (Dataset)')

    graphData = percentageLowRuns.drop(['Development', 'Validation', 'Model'], axis='columns').melt('Percentage Low ε')

    g = sns.lineplot(data=graphData, x='Percentage Low ε', y='value', hue='variable', ax=axes[1])
    g.set(ylabel='Accuracy', xlabel='Percentage Low ε in Dataset');
    g.legend_.set_title('Model(Dataset)')

    fig.savefig('./output/chart-overall-RandomForestClassifier.png', bbox_inches='tight', dpi=600)

    print('Classifier model used in experiments:')
    print('Threshold of ' + str(classifierModelUsed['Threshold']))
    display(classifierModelUsed['Model Params'])

def Ovall_RandomForestRegrassion():

    pbar = ProgressBar()
    pbar.register()  # global registration
    if (sys.platform == 'win32' and mp.cpu_count() >= 61):
        dask.config.set(num_workers=61)
    sns.set_theme(style="whitegrid", font_scale=1.1, font='Calibri')
    sns.despine(left=True)

    colors = ['#e66101', '#fdb863', '#b2abd2', '#5e3c99']
    sns.set_palette(sns.color_palette(colors))
    figureSize = (4, 3)
    padInches = 0.05
    development = utils.LoadDataFromOutput('dataset-development')
    validation = utils.LoadDataFromOutput('dataset-validation')
    # print('Developement Dataset Count: ' + str(len(development)))
    # print('Validate Dataset Count: ' + str(len(validation)))

    data = pd.concat([development, validation]).reset_index(drop=True)
    # print('Total Count: ' + str(len(data)))
    # print('Number of Training Features: ' + str(len(development.columns)))
    # development.head(1)
    regressorModelUsed = pd.read_parquet('./code/modelUsed-RandomForestRegressor.gzip.parquet').iloc[0]
    regressorModelUsed['Thresholds'] = ast.literal_eval(regressorModelUsed['Thresholds'])

    regressorModelUsed['Model'] = train.TrainRandomForestRegressor(regressorModelUsed['Model Params'],
                                                                   regressorModelUsed['Trial Type'],
                                                                   regressorModelUsed['High Epsilon Weight']
                                                                   , regressorModelUsed['Thresholds'], data)

    # print('Model Used:')
    # print(regressorModelUsed['Trial Type'])
    # if (regressorModelUsed['Trial Type'] == 'Thresholds Trial'):
    #     print('Thresholds: ' + str(regressorModelUsed['Thresholds']))
    # else:
    #     print('High Epsilon Weight: ' + str(regressorModelUsed['High Epsilon Weight']))
    # display(regressorModelUsed['Model'])
    #graphs

    def GraphResults(data, model, title, ax):
        X, y = train.GetXandY(data)
        y_weights = train.ComputeWeightsForRegressor(y, model['Trial Type'], model['High Epsilon Weight'],
                                                     model['Thresholds'])

        predict_y = model['Model'].predict(X)
        score = model['Model'].score(X, y, y_weights)
        chart = sns.scatterplot(x=y / 1000, y=predict_y / 1000, ax=ax)
        chart.set(title=title + ' Score: ' + format(score, '.2f'))
        chart.xaxis.set_label_text('Actual ' + labels.EpsilonFull)
        chart.yaxis.set_label_text('Predicted ' + labels.EpsilonFull)
        chart.axvline(150, color='#5e3c99')
        chart.axhline(150, color='#5e3c99')

        fig, axes = plt.subplots(ncols=2, figsize=(8, 4), constrained_layout=True, sharey=True, sharex=True)
        GraphResults(development, regressorModelUsed, 'Development', axes[0])
        GraphResults(validation, regressorModelUsed, 'Validation', axes[1])

        fig.savefig('./output/chart-overall-RandomForestRegressor.png', bbox_inches='tight', dpi=600)
def prediction():
    sns.set_theme(style="whitegrid", font_scale=1.1, font='Calibri')
    sns.despine(left=True)

    colors = ['#e66101', '#fdb863', '#b2abd2', '#5e3c99']
    sns.set_palette(sns.color_palette(colors))
    figureSize = (4, 3)
    padInches = 0.05
    development = utils.LoadDataFromOutput('dataset-development')
    validation = utils.LoadDataFromOutput('dataset-validation')
    data = pd.concat([development, validation]).reset_index(drop=True)
    temp = pd.read_parquet('./code/modelUsed-RandomForestRegressor.gzip.parquet').iloc[0]
    temp['Thresholds'] = ast.literal_eval(temp['Thresholds'])

    regressor = train.TrainRandomForestRegressor(temp['Model Params'], temp['Trial Type'], temp['High Epsilon Weight']
                                                 , temp['Thresholds'], data)

    print('Model Used:')
    print(temp['Trial Type'])
    if (temp['Trial Type'] == 'Thresholds Trial'):
        print('Thresholds: ' + str(temp['Thresholds']))
    else:
        print('High Epsilon Weight: ' + str(temp['High Epsilon Weight']))
    display(regressor)
    data = utils.LoadDataFromOutput('dataset-experimental')
    results = data[['Source Key', 'Td-Dft (Debye)', 'Min Epsilon', 'Max Epsilon']].copy()
    results['Min Epsilon'] = results['Min Epsilon'] / 1000
    results.loc[results['Min Epsilon'] == 0, 'Min Epsilon'] = np.nan

    results['Max Epsilon'] = results['Max Epsilon'] / 1000
    results.loc[results['Max Epsilon'] == 0, 'Max Epsilon'] = np.nan

    emptyDataFrame = pd.DataFrame(columns=regressor.feature_names_in_)
    formatted = pd.concat([data, emptyDataFrame]).fillna(0)
    results['Regressor Prediction'] = regressor.predict(formatted[emptyDataFrame.columns]) / 1000

    # results
    epsilons = results['Source Key'].to_frame().join(results[['Min Epsilon', 'Max Epsilon']].apply(pd.Series)).melt(
        'Source Key').dropna()[['Source Key', 'value']]

    g = sns.lineplot(data=results, x='Source Key', y='Td-Dft (Debye)', color='#5e3c99'
                     , label=labels.TD_DFT, legend=False)
    g.axes.set_ylabel(labels.MuFull)

    ax2 = g.axes.twinx()
    sns.lineplot(data=epsilons, x='Source Key', y='value', color='#e66101'
                 , label='Actual ' + labels.Epsilon + ' Range', legend=False, ax=ax2)

    sns.scatterplot(data=results, x='Source Key', y='Regressor Prediction', color='#e66101'
                    , label='Pred. ' + labels.Epsilon, legend=False, ax=ax2, marker='d', s=100)

    g.axes.figure.legend(bbox_to_anchor=(.75, .5), frameon=True)

    ax2.set_ylabel(labels.EpsilonFull)
    ax2.set_ylim((0, 300))
    g.axes.set_ylim((0, 22))
    g.set_xlabel('')
    utils.RotateAllXText([g])
    g.figure.tight_layout()

    g.figure.savefig('./output/chart-prediction-experimental.png', bbox_inches='tight', dpi=600)

    data = utils.LoadDataFromOutput('dataset-unknownEpsilon')
    results = data[['Source Key']].copy()

    emptyDataFrame = pd.DataFrame(columns=regressor.feature_names_in_)
    formatted = pd.concat([data, emptyDataFrame]).fillna(0)
    results['Regressor Prediction'] = regressor.predict(formatted[emptyDataFrame.columns]) / 1000
    # results
    # graph 2

    g = sns.scatterplot(data=results, x=results.index, y='Regressor Prediction')
    g.set(xticklabels=[], ylabel='Regressor Predicted ' + labels.EpsilonFull)

    g.figure.savefig('./output/chart-prediction-unknown.png', bbox_inches='tight', dpi=600)
    combined = results.merge(data, on='Source Key')
    combined[(combined['Regressor Prediction'] >= 150)].to_csv('./output/highUnknownPredictions.csv')
    pd.read_csv('./output/highUnknownPredictions.csv')