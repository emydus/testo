#%%
import seaborn as sns
import scipy 
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as date
from pathlib import Path
import glob
import os

#from fbprophet import Prophet

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
        na_values = ['-1'])
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

path =r'D:\D Drive temp backup\Uni\3rd Year\MWay Comms Project Group\Git\PHY346_MWayComms\data' # use your path
allFiles = glob.glob(path + "/*.csv")
dframe = loadfiles(allFiles)

#change header names to remove white spaces
dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')

#calculate average occupancy accross all lanes
dframe['avg_occupancy'] = dframe[['occupancylane_1', 'occupancylane_2', 'occupancylane_3',
					'occupancylane_4', 'occupancylane_5', 'occupancylane_6',
					'occupancylane_7']].mean(axis=1)

#calculate average speed across lanes
dframe['avg_speed'] = dframe[['speedlane_1', 'speedlane_2', 'speedlane_3',
					'speedlane_4', 'speedlane_5', 'speedlane_6',
					'speedlane_7']].mean(axis=1)
dframe['avg_headway'] = dframe[['headwaylane_1','headwaylane_2','headwaylane_3','headwaylane_4','headwaylane_5','headwaylane_6','headwaylane_7']].mean(axis=1)
dframe['avg_flow'] = dframe[['flowlane_1','flowlane_2','flowlane_3','flowlane_4','flowlane_5','flowlane_6','flowlane_7']].mean(axis=1)

#Hopefully removes duplicate columns from dframe to enable group function to work
dframe = dframe.loc[:,~dframe.columns.duplicated()]

#All of named var excluding avg
speed_all=['avg_speed','speedlane_1', 'speedlane_2', 'speedlane_3',	'speedlane_4', 'speedlane_5', 'speedlane_6','speedlane_7']
flow_all_lane=['flowlane_1','flowlane_2','flowlane_3','flowlane_4','flowlane_5','flowlane_6','flowlane_7']
flow_all_cats=['flowcategory_1','flowcategory_2','flowcategory_3']
occupancy_all=['avg_occupancy','occupancylane_1', 'occupancylane_2', 'occupancylane_3','occupancylane_4', 'occupancylane_5', 'occupancylane_6','occupancylane_7']
headway_all=['avg_headway','headwaylane_1','headwaylane_2','headwaylane_3','headwaylane_4','headwaylane_5','headwaylane_6','headwaylane_7']
dframe['flow_total']=dframe[flow_all_lane].sum(axis=1)
lane_data_all=[speed_all,flow_all_lane,occupancy_all,headway_all]



print('Data Loaded')
#%%
#set index to datetime and generate a new dframe of just morning data for all days
dframe = dframe.set_index(pd.DatetimeIndex(dframe['datetime']))
dframe_rush_morning=dframe.between_time('6:30','9:30')
dframe_rush_evening=dframe.between_time('16:30','18:30')
dframe_between_rush=dframe.between_time('9:30','16:30')
#%%
#dframe.set_index('geographic_address')
def group(column):
	"""
	Group by column and create separate dataframes
	"""
	grouped = dframe.groupby(column)
	dframe1 = {}
	for name, group in grouped:
		dframe[name] = group
	return(dframe1)
#dframe1 = group('geographic_address')




#Sensors=list(set(df['geographic_address'])) # Dated Below should preserve order
Sensors=list(dict.fromkeys(dframe['geographic_address']))
#%%
'''
#Convert Sensors list into indexed pandas dataframe
SensorFrame = pd.DataFrame(data=Sensors,index=Sensors)

#Plots speeds against time for all (selected) Sensor locations
def Speedtime(sensor1,sensor2):
    """
    Plot sensors' speed-time data from lanes 1-3 and avg. speed, 
    ranging from sensor1 to sensor2
    """
    i=1
    for pos in SensorFrame.loc[sensor1:sensor2,0]:
        speeds= dframe[pos][['time','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
        speeds = pd.melt(speeds, id_vars = ['time'], var_name = 'lane', value_name = 'speed')
        LinePlot= sns.lineplot(x = 'time', y = 'speed', hue = 'lane', data = speeds).set_title(pos)
        time_start = date.time(6,30)    
        time_end = date.time(9,30)
        plt.xlim(time_start,time_end)
        plt.subplot(4,4,i)
        i+=1
        del LinePlot   
        del speeds
    plt.show()
def SpeedOccupancy(sensor1,sensor2):
    """
    Plot sensors' speed-Occupancy data from lanes 1-3 and avg. speed, 
    ranging from sensor1 to sensor2
    """
    i=1
    for pos in SensorFrame.loc[sensor1:sensor2,0]:
        speeds= dframe[pos][['speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed','occupancylane_1','occupancylane_2','occupancylane_3','avg_occupancy']]
        speeds = pd.melt(speeds, id_vars = ['occupancylane_1','occupancylane_2','occupancylane_3'], var_name = 'lane', value_name = 'speed')
        LinePlot= sns.lineplot(x = 'occupancylane_2', y = 'speedlane_2', data = speeds).set_title(pos)
        plt.xlim(0,100)
        plt.subplot(4,4,i)
        i+=1
        del LinePlot   
        del speeds
    plt.show()
'''
#%%
#Speedtime('M42/6190A','M42/6200A')
#print(df[speed_all[0:4]].describe(include=[np.number]))
for LData in lane_data_all:
    a=1
    for i in LData:
        #plt.subplot(1,4,a)
        sns.distplot()
        plt.title('LData')
        plt.legend()
        a+=1
    plt.show()
    del a
#%%
for LData in lane_data_all:
    for i in LData[0:5]:
        print(dframe[i].describe([.99,.95,.75,.5,.25,.05,.01]))
#%%
#dframe = dframe.set_index(pd.DatetimeIndex(dframe['datetime']))
dframe_rush['flow_total'].plot.hist(bins=57,rwidth=0.9)
plt.title('Total Flow')
#%%
dframe1['flow_total'].plot.line()
#%%
var1='flow_total'
varFrame=dframe
Dframe=varFrame[np.isfinite(varFrame[var1])]
sns.distplot(Dframe[var1],kde=False)
plt.title('Flow for all times', len(varFrame[var1]))
len(varFrame[var1])
#%%
sns.lineplot(x='datetime',y=var1,data=dframe['datetime','var1'])
plt.show()
#%%
dframe=dframe.set_index('geographic_address')
Sensors=list(dict.fromkeys(dframe['geographic_address']))
print(Sensors[0])
dframe['M42/6104L']=dframe.loc['M42/6104L']
print(dframe['M42/6104L'])
#%%
dframe[dframe.index.duplicated()]
#%%
dframe.groupby('geographic_address')
dframe['geographic_address']