#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 26 13:01:50 2019

@author: Titus

Adds 'carriage' and 'slip' columns to dataframe, which give info on what carriage the sensor is in,
and if it is a sliproad, wether it is an ON or OFF sliproad

TO DO: 
    - Find getaround to include 'M' sensors without each sensor being counted (string selection?)
    - Split the large dataframe into A and B dataframes
"""

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
    list_ = []
    n=0
    for file in allFiles:
        df = pd.read_csv(file, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes',
        'Flow(Category 1)', 'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values = ['-1'], low_memory=True)
        list_.append(df)
        n+=1
        # Included print statement for troubleshooting:
        print('Done %s!'%n)
    """
    
    
    Change number of days being looked at here
    
    
    """
    dframe = pd.concat(list_[0:1])
    #change header names to remove white spaces
    dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
    dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
    #convert to datetime
    dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
    dframe["date"] = pd.to_datetime(dframe["date"],format="%d/%m/%y %H:%M")
    dframe = dframe.drop(columns='time')
    dframe = dframe.rename(columns = {'date':'datetime'})
    return dframe

#Load in files
#path =r'D:\D Drive temp backup\Uni\3rd Year\MWay Comms Project Group\Git\PHY346_MWayComms\data' # use your path
#allFiles = glob.glob(path + "/*.csv")
datafolderpath = cwd.joinpath("data")
allFiles=datafolderpath.glob("*.tcd.csv*")
df = loadfiles(allFiles)


def averagevar(dframe, variable):
    """
   calculates the average of specified variable across lanes and creates column
   at the end of the dataframe
   """
    dframe['avg_' + variable] = dframe[[variable + 'lane_1', variable + 'lane_2', variable + 'lane_3',
                                        variable + 'lane_4', variable + 'lane_5', variable + 'lane_6',
                                        variable + 'lane_7']].mean(axis=1)
    return dframe['avg_' + variable]


averagevar(df, 'speed')
averagevar(df, 'flow')
averagevar(df, 'occupancy')
averagevar(df, 'headway')

# %%

congested = df[df['avg_speed'] <= 45].index
not_congested = df[df['avg_speed'] > 45].index
pre_congested = congested - 1
new_df = df.ix[pre_congested]
pre_congested = new_df[new_df['avg_speed'] > 45].index

df['congested'] = np.nan
df['congested'].iloc[not_congested] = 'not_congested'
df['congested'].iloc[pre_congested] = 'pre_congested'
df['congested'].iloc[congested] = 'congested'
df = df[['geographic_address','datetime','avg_flow', 'avg_occupancy', 'avg_headway', 'congested']]
df = df.dropna()


# Sort data into A and B carriageway data
Sensors=list(dict.fromkeys(df['geographic_address']))
carriage = []
slip = []



for sensor in Sensors:
    if "A"  in sensor:
        carriage.append('A')
        slip.append('NA')
    elif "K" in sensor:
        carriage.append('A')
        slip.append('ON')
    elif "J" in sensor:
        carriage.append('A')
        slip.append('OFF')
#    elif "M" in sensor:
#        slip.append('ON')
    elif "L" in sensor:
        carriage.append('B')
        slip.append('OFF')
    else:
        carriage.append('B')
        slip.append('NA')


zipcarr =  list(zip(Sensors, carriage, slip))
dfcarr = pd.DataFrame(zipcarr, columns = ['geographic_address','carriage','slip'])
df = pd.merge(df, dfcarr, on='geographic_address', how='outer')


# Group data into separate dataframes
geo_grouped = df.groupby('geographic_address',sort=False)



#Export to CSV for checking everything is as it should be
#df.to_csv('TESTCSV')





        


















