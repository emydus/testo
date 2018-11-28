"""
Computer program to load in data from MWay Comms database

ELoisa Paver
"""
import pandas as pd 
import seaborn as sns
import matplotlib.pyplot as plt
import datetime
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
	na_values = ['-1', '0.0'])

#change header names to remove white spaces
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')

#calculate average speed across lanes
df['avg_speed'] = df[['speedlane_1', 'speedlane_2', 'speedlane_3',
					'speedlane_4', 'speedlane_5', 'speedlane_6',
					'speedlane_7']].mean(axis=1)

#change time to datetime format
df['time'] = pd.to_datetime(df['time'],format= '%H:%M' ).dt.time

def group(column):
	"""
	group by column and create separate dataframes
	"""
	grouped = df.groupby(column)
	dframe = {}
	for name, group in grouped:
		dframe[name] = group
	return(dframe)

dftime = group('time')
dfgeo_add = group('geographic_address')

Sensors=list(dict.fromkeys(df['geographic_address']))

#Flag sensor areas where there are sliproads 
Sliplist = []
for Sensor in Sensors:
    if "K" in Sensor:
        Sliplist.append(Sensor)
    elif "J" in Sensor:
        Sliplist.append(Sensor)
    
'''Eloisa I leave the commented out code below for you to delete if you deem it fit to go - Titus'''
# =============================================================================
# # select columns from sensor dataset
# M42_6111A_speeds = dframe['M42/6111A'][['time','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
# # put dataframe into a format readable for Seaborn visualisation
# M42_6111A_speeds = pd.melt(M42_6111A_speeds, id_vars = ['time'], var_name = 'lane', value_name = 'speed')
# # plot line graph
# sns.lineplot(x = 'time', y = 'speed', hue = 'lane', data = M42_6111A_speeds)
# plt.show()
# =============================================================================

#create function which outputs speeds for all times dataframe for a single sensor
def sensspeed(sensorname):
    '''Takes the name of a sensor, outputs the speed data for all times, ready for plotting.
    Make sure input is of the from: 'M42/6111A' (ie uses slashes, not underscores).
    Input does not need to be string'''
    SensorSpeeds = dfgeo_add[str(sensorname)][['time','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
    SensorSpeeds = pd.melt(SensorSpeeds, id_vars = ['time'], var_name = 'lane', value_name = 'speed')
    return SensorSpeeds

#sns.lineplot(x = 'time', y = 'speed', hue = 'lane', data = sensspeed('M42/6111A'))
    

'''Eloisa I leave the commented out code below for you to delete if you deem it fit to go... - Titus'''
# =============================================================================
# #select columns from time dataset
# eight_thirty_speeds = dframe[datetime.time(8,30)][['geographic_address', 'speedlane_1', 'speedlane_2', 'avg_speed']]
# 
# 
# #put dataframe into a format readable for Seaborn visualisation
# eight_thirty_speeds = pd.melt(eight_thirty_speeds, id_vars = ['geographic_address'], var_name = 'lane', value_name = 'speed')
# =============================================================================

#create speed-time function that creates plottable data frame
def stdframe(hour,minute):
    '''Function which selects speed columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn'''
    time_speeds = dftime[datetime.time(hour,minute)][['geographic_address', 'speedlane_1', 'speedlane_2', 'avg_speed']]
    time_speeds = pd.melt(time_speeds, id_vars = ['geographic_address'], var_name = 'lane', value_name = 'speed')
    return time_speeds

#plot line graph
sns.lineplot(x = 'geographic_address', y = 'speed', hue = 'lane', data = stdframe(8,30), sort=False)

#show lines at outstations
# On: K, M // Off: J, L
for sensor in Sensors:
    if sensor in Sliplist:
       if "K" in sensor: 
        plt.axvline(sensor, color="b", linewidth=0.4) 
       elif "J" in sensor: 
        plt.axvline(sensor, color="r", linewidth=0.4) 
plt.show()

