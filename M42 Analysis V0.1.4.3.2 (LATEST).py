'''
CHANGELOG V0.1.4.3.2 
- Tweaked subplots to dyanmically change dimentions depending on volume of sensors called. 


ISSUES V0.1.4.3.2

[NON-CRITICAL]
- Floats 0.0 should be accepted for some/all variables
- SpeedOccupancy() only plots one lane at a time; may be possible to extend this to multiple lanes



'''  

import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
import datetime as date
import os 
import math

#Find relative path to data (see Misc / yjt_master.py)
gdrive = os.path.dirname(os.path.dirname(__file__))
data = os.path.join(gdrive, 'M42 A Carriageway 40091017.tcd.csv')

# Import data as a panda dataframe (Adjusted to remove empty columns / lanes,
# Added extra identifier columns)
df = pd.read_csv(data,
	usecols = ['Geographic Address','CO Address','LCC Address','Transponder Address',
    'Device Address','Date','Time','Number of Lanes','Flow(Category 1)', 
	'Flow(Category 2)','Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)', 
	'Speed(Lane 2)','Speed(Lane 3)','Speed(Lane 4)','Flow(Lane 1)','Flow(Lane 2)',
    'Flow(Lane 3)','Flow(Lane 4)','Occupancy(Lane 1)','Occupancy(Lane 2)', 
	'Occupancy(Lane 3)','Occupancy(Lane 4)','Headway(Lane 1)','Headway(Lane 2)',
    'Headway(Lane 3)','Headway(Lane 4)'],
    na_values = ['-1','0.0'])

#Change header names to remove white spaces
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

#Combining date and time to a date-time format and removing time column 
df["date"] = df["date"].map(str) + " " + df["time"]
df["date"] = pd.to_datetime(df["date"],format="%d-%m-%y %H:%M")
df = df.drop(columns='time')

# Condensing identifying info into identity column, renaming date to datetime
df["geographic_address"] = (pd.Series(data = df["geographic_address"].map(str)+" "+
  df["co_address"].map(str)+" "+df["lcc_address"].map(str)+" "+
  df["transponder_address"].map(str)+" "+df["device_address"].map(str)))
df = df.drop(columns=["co_address","lcc_address","transponder_address",
                      "device_address"])
df = df.rename(columns = {'geographic_address':'identity',"date":"datetime"})


#Calculate average speed across lanes
df['avg_speed'] = df[['speedlane_1', 'speedlane_2', 'speedlane_3',
					'speedlane_4']].mean(axis=1)

#Calculate average occupancy accross all lanes
df['avg_occupancy'] = df[['occupancylane_1', 'occupancylane_2', 'occupancylane_3',
					'occupancylane_4']].mean(axis=1)



def group(column):
	"""
    Group by column and create separate dataframes
	dframe is a dictionary with the identifiers as keys, values as dataframes
    (Seems to run quite slowly when called D: )
    c. Tom	"""
	grouped = df.groupby(column)
	dframe = {}
	for name, group in grouped:
		dframe[name] = group
	return(dframe)

dframe = group('identity')

#Sensors=list(set(df['geographic_address'])) # Dated Below should preserve order
Sensors=list(dict.fromkeys(df['identity']))
#print(df['datetime'])


#Convert Sensors list into indexed pandas dataframe
SensorFrame = pd.DataFrame(data=Sensors,index=Sensors)

#Place default time range to use in functions
t1 = date.datetime(2017,10,9,8,00)             #time_start
t2 = date.datetime(2017,10,9,10,00)            #time_end

#Plots speeds against time for all (selected) Sensor locations
def Speedtime(sensor1,sensor2,time_start,time_end):
    """
    Plot sensors' speed-time data from lanes 1-3 and avg. speed, 
    ranging from sensor1 to sensor2
    """
    i=1
    depth=1
    sub_dimen = len(SensorFrame.loc[sensor1:sensor2,0])
    depth = int(math.sqrt(sub_dimen))+1
    for pos in SensorFrame.loc[sensor1:sensor2,0]:
        speeds= dframe[pos][['datetime','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
        speeds = pd.melt(speeds, id_vars = ['datetime'], var_name = 'lane', value_name = 'speed')
        LinePlot= sns.lineplot(x = 'datetime', y = 'speed', hue = 'lane', data = speeds).set_title(pos)
        plt.xlim(time_start,time_end)
        plt.subplot(depth,depth,i)
        i+=1
        del LinePlot   
        del speeds
    plt.show()

    
    
###Function only plots one lane. Possible to extend to multiple lanes?
# =============================================================================
# def SpeedOccupancy(sensor1,sensor2):
#     """
#     Plot sensors' speed-Occupancy data from lanes 1-3 and avg. speed, 
#     ranging from sensor1 to sensor2
#     """
# 	
#     i=1
#     for pos in SensorFrame.loc[sensor1:sensor2,0]:
#         speeds= dframe[pos][['speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed','occupancylane_1','occupancylane_2','occupancylane_3','avg_occupancy']]
#         LinePlot= sns.lineplot(x = 'occupancylane_2', y = 'speedlane_2', data = speeds).set_title(pos)
#         plt.xlim(0,100)
#         plt.subplot(4,4,i)
#         i+=1
#         del LinePlot   
#         del speeds
#     plt.show()
# 
# =============================================================================
 
 
def OccupancyTime(sensor1,sensor2,time_start,time_end):
    """
    Plot sensors' speed-time data from lanes 1-3 and avg. speed, 
    ranging from sensor1 to sensor2
    """
    i=1
    depth=1
    sub_dimen = len(SensorFrame.loc[sensor1:sensor2,0])
    depth = int(math.sqrt(sub_dimen))+1
    for pos in SensorFrame.loc[sensor1:sensor2,0]:
        Occupancys= dframe[pos][['datetime','occupancylane_1', 'occupancylane_2', 'occupancylane_3', 'avg_occupancy']]
        Occupancys = pd.melt(Occupancys, id_vars = ['datetime'], var_name = 'lane', value_name = 'occupancy')
        LinePlot= sns.lineplot(x = 'datetime', y = 'occupancy', hue = 'lane', data = Occupancys).set_title(pos)
        plt.xlim(time_start,time_end)
        plt.subplot(depth,depth,i)
        i+=1
        del LinePlot   
        del Occupancys
    plt.show()

def OccupancySpeedTime(sensor1,sensor2,time_start,time_end):
    """
    Plot sensors' speed-time data from lanes 1-3 and avg. speed, 
    ranging from sensor1 to sensor2
    """
    i=1
    depth=1
    sub_dimen = len(SensorFrame.loc[sensor1:sensor2,0])
    depth = int(math.sqrt(sub_dimen))+1
    for pos in SensorFrame.loc[sensor1:sensor2,0]:
        Occupancys= dframe[pos][['datetime','occupancylane_1', 'occupancylane_2', 'occupancylane_3', 'avg_occupancy']]
        Occupancys = pd.melt(Occupancys, id_vars = ['datetime'], var_name = 'lane', value_name = 'occupancy')
        speeds= dframe[pos][['datetime','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
        speeds = pd.melt(speeds, id_vars = ['datetime'], var_name = 'lane', value_name = 'speed')
        sns.lineplot(x = 'datetime', y = 'speed', hue = 'lane', data = speeds,).set_title(pos)
        ax2 = plt.twinx()
        sns.lineplot(x = 'datetime', y = 'occupancy', hue = 'lane', data = Occupancys,ax=ax2,).set_title(pos)
        plt.xlim(time_start,time_end)
        plt.subplot(depth,depth,i)
        i+=1  
        del Occupancys
    plt.show()


###Test functions (giving error - see priority in changelog)
#OccupancySpeedTime(Sensors[0],Sensors[3],t1,t2)
#OccupancyTime('M42/6117A','M42/6190A',t1,t2)
#SpeedOccupancy('M42/6190A','M42/6200A',t1,t2)

#Call function for range at first set of sliproads
#Speedtime('M42/6117A','M42/6190A',t1,t2)


