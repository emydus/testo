# -*- coding: utf-8 -*-
"""
Created on Thu Feb  7 18:17:59 2019

@author: Tom Lockwood
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
    for file in allFiles:
        df = pd.read_csv(file, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes',
        'Flow(Category 1)', 'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values = ['-1'], low_memory=False)
        list_.append(df)
    dframe = pd.concat(list_)
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
dframe = loadfiles(allFiles)

#change header names to remove white spaces
dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
#Defining average values
#Essentially adds an extra column with an average lane value in
dframe['avg_occupancy'] = dframe[['occupancylane_1', 'occupancylane_2', 'occupancylane_3','occupancylane_4', 'occupancylane_5', 'occupancylane_6','occupancylane_7']].mean(axis=1)
dframe['avg_speed'] = dframe[['speedlane_1', 'speedlane_2', 'speedlane_3','speedlane_4', 'speedlane_5', 'speedlane_6','speedlane_7']].mean(axis=1)
dframe['avg_headway'] = dframe[['headwaylane_1','headwaylane_2','headwaylane_3','headwaylane_4','headwaylane_5','headwaylane_6','headwaylane_7']].mean(axis=1)
dframe['avg_flow'] = dframe[['flowlane_1','flowlane_2','flowlane_3','flowlane_4','flowlane_5','flowlane_6','flowlane_7']].mean(axis=1)

#Quick ways of referring to groups of columns
speed_all=['avg_speed','speedlane_1', 'speedlane_2', 'speedlane_3',	'speedlane_4', 'speedlane_5', 'speedlane_6','speedlane_7']
flow_all_lane=['flowlane_1','flowlane_2','flowlane_3','flowlane_4','flowlane_5','flowlane_6','flowlane_7']
flow_all_cats=['flowcategory_1','flowcategory_2','flowcategory_3']
occupancy_all=['avg_occupancy','occupancylane_1', 'occupancylane_2', 'occupancylane_3','occupancylane_4', 'occupancylane_5', 'occupancylane_6','occupancylane_7']
headway_all=['avg_headway','headwaylane_1','headwaylane_2','headwaylane_3','headwaylane_4','headwaylane_5','headwaylane_6','headwaylane_7']
dframe['flow_total']=dframe[flow_all_lane].sum(axis=1)
lane_data_all=[speed_all,flow_all_lane,occupancy_all,headway_all]
#%%
geo_grouped = dframe.groupby("geographic_address",sort=False)
time_grouped = dframe.groupby("datetime",sort=False)
#%%
"""
Pinch a lot of functions of Eloisas Weather work here so hopefully we can be more consistent/compatible with future work
"""
def rushGrouping():
    #set index to datetime and generate a new dframe of specified time bins for all days
    dframe = dframe.set_index(pd.DatetimeIndex(dframe['datetime']))
    dframe_rush_morning=dframe.between_time('6:30','9:30')
    dframe_rush_evening=dframe.between_time('16:30','18:30')
    dframe_between_rush=dframe.between_time('9:30','16:30')

def sensorsD(column):
    """
    Create dictionary of keys and ids e.g for M42 A Carriageway 40091017,
    (0,1,...189) & (M42/6111A...M42/6738J)
    """
    sensors = list(dict.fromkeys(dframe[column]))
    sensorsD = {}
    index = 0
    for id in sensors:
        sensorsD[index] = id
        index += 1
    return sensorsD

sensorDict_geo = sensorsD("geographic_address")
sensorDict_time = sensorsD("datetime")

def geochoice(index):
    return geo_grouped.get_group(sensorDict_geo[index])
def time_choice(index):
    return time_grouped.get_group(sensorDict_time[index])

#create function which outputs speeds for all times dataframe for a single sensor
def sensspeed(sensorname):
    '''
    Takes the name of a sensor, outputs the speed data for all times, ready for plotting.
    Make sure input is of the from: 'M42/6111A' (ie uses slashes, not underscores).
    '''
    particular_df = geo_grouped.get_group(sensorname)
    SensorSpeeds = particular_df[['datetime','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
    SensorSpeeds = pd.melt(SensorSpeeds, id_vars = ['datetime'], var_name = 'lane', value_name = 'speed')
    return SensorSpeeds

def get_region(Start_Location,End_Location):
    """
    Produces a dataframe over a given section of motorway

    """
    dframe_region_list=[]
    for pos in sensorDict_geo:
        dframe_region_list.append(geochoice(pos))
    dframe_region=pd.concat(dframe_region_list)
    return dframe_region

#Plots speed against time with speed averaged over the whole range
def RegionAvgSpeedTime(Start_Location,End_Location,Day):
    return
#%%
#print(geochoice(0))
#print(sensorsD(0))
print(dframe)
"""
To-do 



Flow heatmap for pos against time for specific regions
"""
print(get_region(1,4))
#Pos_Time_Flow=get_region(0,10).pivot(index='geographic_address', columns='datetime', values='flow_total')
#sns.heatmap(Pos_Time_Flow)