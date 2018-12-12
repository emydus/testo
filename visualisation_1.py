"""
Computer program to load in data from MWay Comms database

ELoisa Paver
"""
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import os
from matplotlib.dates import DateFormatter, HourLocator
import numpy as np

#Find relative path to data (see yjt_master.py)
workdir = 'C:/Users/Eloisa/Google Drive/MWay_Comms/'
# workdir = os.path.dirname(__file__)
# dataA = os.path.join(workdir,"data", 'M42 A Carriageway 40091017.tcd.csv')
dataA = os.path.join(workdir, 'M42 A Carriageway 40091017.tcd.csv')

#import data as a panda dataframe
def data_pdreadin(data):
    df = pd.read_csv(data, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Flow(Category 1)',
        'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values = ['-1'])
    #change header names to remove white spaces
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.columns = df.columns.str.replace('(', '').str.replace(')', '')
    return df

dfA = data_pdreadin(dataA)
dfA['avg_speed'] = dfA[['speedlane_1', 'speedlane_2', 'speedlane_3',
                    'speedlane_4', 'speedlane_5', 'speedlane_6',
                    'speedlane_7']].mean(axis=1)

dfA['time'] = pd.to_datetime(dfA['time'],format= '%H:%M' ).dt.time
dfA['congested'] = dfA['avg_speed'].apply(lambda x: x < 60)
group_by_time = dfA.groupby(['time', 'congested'])
count_congested = group_by_time.size().unstack()
ax = count_congested.plot(kind='barh', stacked=True)
plt.show()
