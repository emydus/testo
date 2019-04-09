import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn import model_selection
import glob
import seaborn as sns

def edit(dframe):  
    #change header names to remove white spaces
    dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
    dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
    #convert to datetime
    dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
    dframe["date"] = pd.to_datetime(dframe["date"],format="%d/%m/%y %H:%M")
    # dframe = dframe.drop(columns='time')
    dframe['time'] = pd.to_datetime(dframe["time"],format="%H:%M")
    dframe = dframe.rename(columns = {'date':'datetime'})
    return dframe

def loadtraffic(allFiles):
    """loop through all csv files and concatenate into a dataframe"""
    list_ = []
    for file in allFiles:
        df = pd.read_csv(file, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes',
        'Flow(Category 1)', 'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values = ['-1'])
        list_.append(df)
    dframe = pd.concat(list_)
    dframe = edit(dframe)
    return dframe

path = 'D:\\D Drive temp backup\\Uni\\3rd Year\\MWay Comms Project Group\\Git\\PHY346_MWayComms\data' # use your path
allFiles = glob.glob(path + "/*.csv")
df = loadtraffic(allFiles)
t_path = 'D:\\D Drive temp backup\\Uni\\3rd Year\\MWay Comms Project Group\\Git\\PHY346_MWayComms\data'
csv1 = '40011018.tcd.csv'
file1 = os.path.join(t_path, csv1)

df2 = pd.read_csv(file1, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes',
        'Flow(Category 1)', 'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values = ['-1'])

# df2 = pd.read_csv(file2, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Speed(Lane 1)',
#         'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
#         'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
#         'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
#         'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
#         'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
#         'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
#         na_values = ['-1'])

def GetSlip(LetterCode):
#Returns wether it is an on off slip or the main
#also returns which Side of the road the sensor belongs to
    if LetterCode in ('A','J','K'):
        Carriage='A'
    elif LetterCode in ('B','M','L'):
        Carriage='B'
    if LetterCode in ('A','B'):
        Slip='Main'
    elif LetterCode in ('J','L'):
        Slip='Off'
    elif LetterCode in ('K','M'):
        Slip='On'
    return Slip,Carriage

def slip_codes(dframe):
    LetterCodes=[i[8] for i in dframe['geographic_address']]
    SlipStatus=[]
    CarriageStatus=[]
    for i in LetterCodes:
        Slip,Carriage=GetSlip(i)
        SlipStatus.append(Slip)
        CarriageStatus.append(Carriage)
    dframe['carriage']=pd.Series(CarriageStatus)
    dframe['slip']=pd.Series(SlipStatus)
    return(dframe)


def averagevar(dframe, variable):
    """
    calculates the average of specified variable across lanes and creates column
    at the end of the dataframe
    """
    dframe['avg_'+ variable] = dframe[[variable +'lane_1', variable + 'lane_2', variable + 'lane_3',
                    variable + 'lane_4', variable + 'lane_5', variable + 'lane_6',
                    variable + 'lane_7']].mean(axis=1)
    return dframe['avg_'+ variable]

def address_convert(df):
    """creates integer using geographic address"""
    df['address_int'] = df['geographic_address'].str.slice(start=4, stop=8)
    df['address_int'] = pd.to_numeric(df['address_int'])
    return df

def time_to_int(df):
    df['time_change'] = df['time'] - df['time'].min()
    df['time_change'] = df['time_change'].dt.total_seconds()
    return df

def weekday_number(row):
    """convert weekday to integer"""
    if row =='Monday':
        return 1
    if row == 'Tuesday':
        return 2
    if row == 'Wednesday':
        return 3
    if row == 'Thursday':
        return 4
    if row == 'Friday':
        return 5
    if row == 'Saturday':
        return 6
    if row == 'Sunday':
        return 7
    return other


#preprocess data and average main variables
averagevar(df, 'speed')
averagevar(df, 'flow')
averagevar(df, 'occupancy')
averagevar(df, 'headway')
df2 = edit(df2)
averagevar(df2, 'speed')
averagevar(df2, 'flow')
averagevar(df2, 'occupancy')
averagevar(df2, 'headway')
df = slip_codes(df)
df = address_convert(df)
df2 = slip_codes(df2)
df2 = address_convert(df2)
df['day'] = df['datetime'].dt.weekday_name
df2['day'] = df2['datetime'].dt.weekday_name
df = time_to_int(df)
df2 = time_to_int(df2)
df ['day_int'] = df['day'].apply (lambda row: weekday_number(row))
df2['day_int'] = df2['day'].apply (lambda row: weekday_number(row))

def GetCongestion(dFrame):
    #create a column assigning a congested label to each row based on speed
    congested = dFrame[dFrame['avg_speed']<=45].index
    not_congested = dFrame[dFrame['avg_speed']>45].index
    pre_congested = np.concatenate((
        congested - 1,
        congested - 2,
        congested - 3,
        congested - 4,
        congested - 5,
        congested - 6,
        congested - 7),
        axis=0
    )
    
    dFrame['congested'] = np.nan
    dFrame['congested'].iloc[not_congested] = 'not_congested'
    dFrame['congested'].iloc[pre_congested] = 'pre_congested'
    dFrame['congested'].iloc[congested] = 'congested'
    return dFrame
#%%

df=GetCongestion(df)
df2=GetCongestion(df2)
#%%
congest_df = df[df['congested'] != 'not_congested']
#df.to_csv('all_days.csv')
sns.scatterplot(x='datetime', y='geographic_address', hue='congested', data=congest_df)
plt.show()
#%%
df_short = df.drop(columns=['geographic_address','datetime','time','day','slip','carriage','speedlane_4','flowlane_4','headwaylane_4','occupancylane_4','speedlane_3','flowlane_3','headwaylane_3','occupancylane_3']).dropna(axis=1,how='all')
df_short = df_short.dropna()
df2_short = df2.drop(columns=['geographic_address','datetime','time','day','slip','carriage','speedlane_4','flowlane_4','headwaylane_4','occupancylane_4','speedlane_3','flowlane_3','headwaylane_3','occupancylane_3']).dropna(axis=1,how='all')
df2_short = df2_short.dropna()
#%%
df_short = df[['avg_speed','avg_flow', 'avg_occupancy', 'avg_headway', 'congested', 'time_change', 'address_int', 'day_int']]
df_short = df_short.dropna()
df2_short = df2[['avg_speed','avg_flow', 'avg_occupancy', 'avg_headway', 'congested', 'time_change', 'address_int', 'day_int']]
df2_short = df2_short.dropna()
#%%
X_train = df_short.drop(columns=['congested'])
Y_train = df_short['congested']
X_test=df2_short.drop(columns=['congested'])
Y_test=df2_short['congested']


clf=RandomForestClassifier()
clf.fit(X=X_train,y=Y_train)
print('Feature importances\n',[(X_train.columns.values[i],clf.feature_importances_[i]) for i in range(len(clf.feature_importances_))],'\n')
ClassPredictionAccuracy=clf.score(X=X_test, y=Y_test)
print('Class prediction accuracy=',ClassPredictionAccuracy) #How accurate the predictions are on a test set

