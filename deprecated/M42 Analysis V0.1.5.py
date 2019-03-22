'''
CHANGELOG V0.1.4
- Updated code to be consistent with V0.1.2; inserted dataframe and function 

ISSUES V0.1.4
- May be useful to add further inputs to Speedtime() to take time values between which
    to plot (i.e time_start, time_end).
- Subplot system may need tweaking
- Possible redundancy of the "datetime" module
'''  

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime as date

#import data as a panda dataframe
df = pd.read_csv('M42 A Carriageway 40091017.tcd.csv',
	usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Flow(Category 1)', 
	'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)', 
	'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
	'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)', 
	'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)', 
	'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)', 
	'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)', 
	'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
	na_values = ['-1','0'])
#change header names to remove white spaces
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

#calculate average speed across lanes
df['avg_speed'] = df[['speedlane_1', 'speedlane_2', 'speedlane_3',
					'speedlane_4', 'speedlane_5', 'speedlane_6',
					'speedlane_7']].mean(axis=1)
#All of named var excluding avg
speed_all=['speedlane_1', 'speedlane_2', 'speedlane_3',	'speedlane_4', 'speedlane_5', 'speedlane_6','speedlane_7']
flow_all_lane=['flowlane_1','flowlane_2','flowlane_3','flowlane_4','flowlane_5','flowlane_6','flowlane_7']
flow_all_cats=['flowcategory_1','flowcategory_2','flowcategory_3']
occupancy_all=['occupancylane_1', 'occupancylane_2', 'occupancylane_3','occupancylane_4', 'occupancylane_5', 'occupancylane_6','occupancylane_7']
headway_all=['headwaylane_1','headwaylane_2','headwaylane_3','headwaylane_4','headwaylane_5','headwaylane_6','headwaylane_7']
lane_data_all=[speed_all,flow_all_lane,occupancy_all,headway_all]

#calculate average occupancy accross all lanes
df['avg_occupancy'] = df[['occupancylane_1', 'occupancylane_2', 'occupancylane_3',
					'occupancylane_4', 'occupancylane_5', 'occupancylane_6',
					'occupancylane_7']].mean(axis=1)
#change time to datetime format
df['time'] = pd.to_datetime(df['time'],format= '%H:%M' ).dt.time

def group(column):
	"""
	Group by column and create separate dataframes
	"""
	grouped = df.groupby(column)
	dframe = {}
	for name, group in grouped:
		dframe[name] = group
	return(dframe)
dframe = group('geographic_address')

#Sensors=list(set(df['geographic_address'])) # Dated Below should preserve order
Sensors=list(dict.fromkeys(df['geographic_address']))


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

#SpeedOccupancy('M42/6117','M42/6190A')
#Call function for range at first set of sliproads
#Speedtime('M42/6190A','M42/6200A')
a=0
print(df[speed_all[0:4]].describe(include=[np.number]))
for i in speed_all:
    a+=1
    df[i].plot.hist(bins=120,rwidth=0.9)
    plt.title(i)
    plt.subplot(1,3,a)
plt.show()
del a
