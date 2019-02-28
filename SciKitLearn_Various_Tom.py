import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC


t_path = 'data'
csv = '40011018.tcd.csv'
file = os.path.join(t_path, csv)
usecols = [
    'Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Speed(Lane 1)',
    'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
    'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
    'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)',
    'Occupancy(Lane 2)',
    'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
    'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
    'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'
]
na_values = ['-1']

df = pd.read_csv(file, usecols=usecols, na_values=na_values)


def edit(dframe):
    # change header names to remove white spaces
    dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
    dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
    # convert to datetime
    dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
    dframe["date"] = pd.to_datetime(dframe["date"], format="%d/%m/%y %H:%M")
    dframe = dframe.drop(columns='time')
    dframe = dframe.rename(columns={'date': 'datetime'})
    return dframe


def averagevar(dframe, variable):
    """
   calculates the average of specified variable across lanes and creates column
   at the end of the dataframe
   """
    dframe['avg_' + variable] = dframe[[variable + 'lane_1', variable + 'lane_2', variable + 'lane_3',
                                        variable + 'lane_4', variable + 'lane_5', variable + 'lane_6',
                                        variable + 'lane_7']].mean(axis=1)
    return dframe['avg_' + variable]


df = edit(df)
averagevar(df, 'speed')
averagevar(df, 'flow')
averagevar(df, 'occupancy')
averagevar(df, 'headway')

congested = df[df['avg_speed'] <= 45].index
not_congested = df[df['avg_speed'] > 45].index
pre_congested = congested - 1
new_df = df.ix[pre_congested]
pre_congested = new_df[new_df['avg_speed'] > 45].index
df['congested'] = np.nan
df['congested'].iloc[not_congested] = 'not_congested'
df['congested'].iloc[pre_congested] = 'pre_congested'
df['congested'].iloc[congested] = 'congested'
df = df[['avg_flow', 'avg_occupancy', 'avg_headway', 'congested']]
df = df.dropna()

#df.to_csv('data/processed_df_' + csv)


def load_processed_df(file_name):
    return df.read_csv(file_name)


# #box and whisker plots
# df.plot(kind='box', subplots=True, layout=(2,2), sharex=False, sharey=False)
# plt.show()

# Split-out validation dataset
array = df.values
X = array[:, 0:3]
Y = array[:, 3]
validation_size = 0.20
seed = 7
X_train, X_validation, Y_train, Y_validation = model_selection.train_test_split(X, Y, test_size=validation_size,
                                                                                random_state=seed)

# Test options and evaluation metric
seed = 7
scoring = 'accuracy'

# Spot Check Algorithms
models = {
    'LR': LogisticRegression(solver='liblinear', multi_class='ovr'),
    'LDA': LinearDiscriminantAnalysis(),
    'KNN': KNeighborsClassifier(),
    'CART': DecisionTreeClassifier(),
    'NB': GaussianNB()
}
# evaluate each model in turn
results = {}
for name, model in models.items():
    if name == "KNN":
        kfold = model_selection.KFold(n_splits=10, random_state=seed)
        cv_results = model_selection.cross_val_score(model, X_train, Y_train, cv=kfold, scoring=scoring)
        results[name] = cv_results
        msg = "%s: %f (%f)" % (name, cv_results.mean(), cv_results.std())
        print(msg)
"""
# Compare Algorithms
fig = plt.figure()
fig.suptitle('Algorithm Comparison')
ax = fig.add_subplot(111)
plt.boxplot(results.values)
ax.set_xticklabels(result.keys)
plt.show()
"""
# %%
'''
Tom
'''
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as date
from pathlib import Path
import glob

cwd = Path.cwd()
cwd = cwd.resolve(strict=True)


def loadfiles(allFiles):
    """loop through all csv files and concatenate into a dataframe"""
    
    NumFiles=7
    list_ = []
    for file in allFiles:
        df = pd.read_csv(file, usecols=['Geographic Address', 'Date', 'Time', 'Number of Lanes',
                                        'Flow(Category 1)', 'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)',
                                        'Speed(Lane 1)',
                                        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)',
                                        'Speed(Lane 6)',
                                        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
                                        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)',
                                        'Occupancy(Lane 2)',
                                        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)',
                                        'Occupancy(Lane 6)',
                                        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
                                        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
                         na_values=['-1'], low_memory=False)
        list_.append(df)
        if len(list_)>=NumFiles:
            break
    """


   Change number of days being looked at here


   """
    dframe = list_[7]
    # change header names to remove white spaces
    dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
    dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
    # convert to datetime
    dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
    dframe["date"] = pd.to_datetime(dframe["date"], format="%d/%m/%y %H:%M")
    dframe = dframe.drop(columns='time')
    dframe = dframe.rename(columns={'date': 'datetime'})
    return dframe


#Load in files
#path =r'D:\D Drive temp backup\Uni\3rd Year\MWay Comms Project Group\Git\PHY346_MWayComms\data' # use your path
#allFiles = glob.glob(path + "/*.csv")
datafolderpath = cwd.joinpath("data")
allFiles = datafolderpath.glob("*.tcd.csv*")
dframe_test = loadfiles(allFiles)
#change header names to remove white spaces
dframe_test.columns = dframe_test.columns.str.strip().str.lower().str.replace(' ', '_')
dframe_test.columns = dframe_test.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
#Defining average values
#Essentially adds an extra column with an average lane value in
dframe_test['avg_occupancy'] = dframe_test[['occupancylane_1', 'occupancylane_2', 'occupancylane_3','occupancylane_4', 'occupancylane_5', 'occupancylane_6','occupancylane_7']].mean(axis=1)
dframe_test['avg_speed'] = dframe_test[['speedlane_1', 'speedlane_2', 'speedlane_3','speedlane_4', 'speedlane_5', 'speedlane_6','speedlane_7']].mean(axis=1)
dframe_test['avg_headway'] = dframe_test[['headwaylane_1','headwaylane_2','headwaylane_3','headwaylane_4','headwaylane_5','headwaylane_6','headwaylane_7']].mean(axis=1)
dframe_test['avg_flow'] = dframe_test[['flowlane_1','flowlane_2','flowlane_3','flowlane_4','flowlane_5','flowlane_6','flowlane_7']].mean(axis=1)

#Quick ways of referring to groups of columns
speed_all=['avg_speed','speedlane_1', 'speedlane_2', 'speedlane_3',	'speedlane_4', 'speedlane_5', 'speedlane_6','speedlane_7']
flow_all_lane=['flowlane_1','flowlane_2','flowlane_3','flowlane_4','flowlane_5','flowlane_6','flowlane_7']
flow_all_cats=['flowcategory_1','flowcategory_2','flowcategory_3']
occupancy_all=['avg_occupancy','occupancylane_1', 'occupancylane_2', 'occupancylane_3','occupancylane_4', 'occupancylane_5', 'occupancylane_6','occupancylane_7']
headway_all=['avg_headway','headwaylane_1','headwaylane_2','headwaylane_3','headwaylane_4','headwaylane_5','headwaylane_6','headwaylane_7']
dframe_test['flow_total']=dframe_test[flow_all_lane].sum(axis=1)
lane_data_all=[speed_all,flow_all_lane,occupancy_all,headway_all]
# %%
congested = dframe_test[dframe_test['avg_speed'] <= 45].index
not_congested = dframe_test[dframe_test['avg_speed'] > 45].index
pre_congested = congested - 1
new_dframe_test = dframe_test.ix[pre_congested]
pre_congested = new_dframe_test[new_dframe_test['avg_speed'] > 45].index
dframe_test['congested'] = np.nan
dframe_test['congested'].iloc[not_congested] = 'not_congested'
dframe_test['congested'].iloc[pre_congested] = 'pre_congested'
dframe_test['congested'].iloc[congested] = 'congested'
test_congested = dframe_test.values[:, 3]
Counter(test_congested)
#%%
dframe_test = dframe_test[['avg_flow', 'avg_occupancy', 'avg_headway']]
dframe_test = dframe_test.dropna()
#Fit the model using X as training data and Y as target values
KNN_model = models['KNN'].fit(X,Y)

predicted=KNN_model.predict(dframe_test)
#%%
from collections import Counter
Counter(list(predicted))
#%%
