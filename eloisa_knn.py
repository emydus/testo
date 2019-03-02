import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn import model_selection
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.neighbors import KNeighborsClassifier

# t_path =r'/Users/Eloisa/Google Drive/MWay_Comms/Oct_2018/'
t_path = 'D:\\D Drive temp backup\\Uni\\3rd Year\\MWay Comms Project Group\\Git\\PHY346_MWayComms\data'
csv1 = '40011018.tcd.csv'
csv2 = '40021018.tcd.csv'
file1 = os.path.join(t_path, csv1)
file2 = os.path.join(t_path, csv2)

df = pd.read_csv(file1, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values = ['-1'])

df2 = pd.read_csv(file2, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values = ['-1'])

def edit(dframe):  
    #change header names to remove white spaces
    dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
    dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
    #convert to datetime
    dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
    dframe["date"] = pd.to_datetime(dframe["date"],format="%d/%m/%y %H:%M")
    dframe = dframe.drop(columns='time')
    dframe = dframe.rename(columns = {'date':'datetime'})
    return dframe

def averagevar(dframe, variable):
    """
    calculates the average of specified variable across lanes and creates column
    at the end of the dataframe
    """
    dframe['avg_'+ variable] = dframe[[variable +'lane_1', variable + 'lane_2', variable + 'lane_3',
                    variable + 'lane_4', variable + 'lane_5', variable + 'lane_6',
                    variable + 'lane_7']].mean(axis=1)
    return dframe['avg_'+ variable]

#preprocess data and average main variables
df = edit(df)
averagevar(df, 'speed')
averagevar(df, 'flow')
averagevar(df, 'occupancy')
averagevar(df, 'headway')

df2 = edit(df2)
averagevar(df2, 'speed')
averagevar(df2, 'flow')
averagevar(df2, 'occupancy')
averagevar(df2, 'headway')

#create a column assigning a congested label to each row based on speed
congested = df[df['avg_speed']<=45].index
not_congested = df[df['avg_speed']>45].index
pre_congested = np.concatenate((
    congested - 1,
    congested - 2,
    congested - 3),
    axis=0
)
new_df = df.ix[pre_congested]
pre_congested = new_df[new_df['avg_speed']>45].index
df['congested'] = np.nan
df['congested'].iloc[not_congested] = 'not_congested'
df['congested'].iloc[pre_congested] = 'pre_congested'
df['congested'].iloc[congested] = 'congested'


congest_df = df[df['congested'] != 'not_congested']
sns.scatterplot(x='datetime', y='geographic_address', hue='congested', data=congest_df)
plt.show()


df_short = df[['avg_flow', 'avg_occupancy', 'avg_headway', 'congested']]
df_short = df_short.dropna()

X_train = df_short[['avg_flow', 'avg_occupancy', 'avg_headway']]
Y_train = df_short['congested']
knn = KNeighborsClassifier()
knn.fit(X_train, Y_train)
df2_short = df2[['avg_flow', 'avg_occupancy', 'avg_headway']]
df2_short = df2_short.dropna()
X_new = df2_short
df2_short['predicted'] = knn.predict(X_new)

df3 =pd.concat([df2, df2_short], axis=1)
df3= df3.dropna(subset=['predicted'])
# df2 = pd.melt(df2, 'predicted', var_name='measurement')
df3 = df3[['datetime', 'geographic_address', 'predicted']]
# sns.swarmplot(x='measurement', y="value", hue="predicted", data=df2)
# sns.pairplot(df2, hue="predicted")
# plt.show()

# congest_df = df3[df3['predicted'] != 'not_congested']
# sns.scatterplot(x='datetime', y='geographic_address', hue='predicted', data=congest_df)
# plt.show()
from collections import Counter
Counter(list(df['congested']))
