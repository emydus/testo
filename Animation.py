"""
Edited by Jason (30/11/2018)
Verified working
"""

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

#Find relative path to data (see pickle_reader.py)
cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
dataA = cwd.joinpath("data",'M42 A Carriageway 40091017.tcd.csv.pkl.gz')

#import data as a panda dataframe
def data_pdreadin(file):
    df = pd.read_pickle(file)
    # TO-DO : NEED TO IMPLEMENT REPLACEMENT FOR NA_VALUES=["-1","0.0"]
    #change header names to remove white spaces
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.columns = df.columns.str.replace('(', '').str.replace(')', '')
    #drop unwanted columns
    df = df.drop(columns=["co_address","lcc_address","transponder_address",
                          "device_address"])
    #datetime_format
    df["date"] = df["date"].map(str) + " " + df["time"]
    df["date"] = pd.to_datetime(df["date"],format="%d-%m-%y %H:%M")
    df = df.drop(columns='time')
    #column_format
    df = df.rename(columns = {"date":"datetime"})
    return df

dfA = data_pdreadin(dataA)

print(dfA.columns)

def carriage_mean(dataf,column_name):
    dataf['avg_' + column_name] = dataf[[column_name + 'lane_1', column_name + 'lane_2',
         column_name + 'lane_3', column_name + 'lane_4', column_name + 'lane_5',column_name + 'lane_6',
         column_name + 'lane_7']].mean(axis=1)
    return dataf

#calculate average speed across lanes
dfA = carriage_mean(dfA,"speed")
#calculate average occupancy across all lanes:
dfA = carriage_mean(dfA,"occupancy")

#def group(column):
#    """
#    group by column and create separate dataframes
#    """
#    grouped = df.groupby(column)
#    dframe = {}
#    for name, group in grouped:
#        dframe[name] = group
#    return(dframe)

def sensorsD(dataf,column):
    """
    Create dictionary of keys and ids e.g for M42 A Carriageway 40091017,
    (0,1,...189) & (M42/6111A...M42/6738J)
    """
    sensors = list(dict.fromkeys(dataf[column]))
    sensorsD = {}
    index = 0
    for id in sensors:
        sensorsD[index] = id
        index += 1
    return sensorsD

sensorDict_geo = sensorsD(dfA,"geographic_address")
sensorDict_time = sensorsD(dfA,"datetime")

# df_grouped (Create GroupBy object)
geo_grouped = dfA.groupby("geographic_address",sort=False)
time_grouped = dfA.groupby("datetime",sort=False)

def geochoice(index):
    return geo_grouped.get_group(sensorDict_geo[index])

def time_choice(index):
    return time_grouped.get_group(sensorDict_time[index])

#dftime = group('time')
#dfgeo_add = group('geographic_address')

Sensors=list(dict.fromkeys(dfA['geographic_address']))

# =============================================================================
# #Flag sensor areas where there are sliproads
# Sliplist = []
# for Sensor in Sensors:
#     if ("K" or "J") in Sensor:
#         Sliplist.append(Sensor)
# =============================================================================
# Jason: The above section isn't needed for running your sliplist since you iterate through the whole thing
#       again...
# =============================================================================
# '''Eloisa I leave the commented out code below for you to delete if you deem it fit to go - Titus'''
# # select columns from sensor dataset
# M42_6111A_speeds = dfgeo_add['M42/6111A'][['time','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
# # put dataframe into a format readable for Seaborn visualisation
# M42_6111A_speeds = pd.melt(M42_6111A_speeds, id_vars = ['time'], var_name = 'lane', value_name = 'speed')
# # plot line graph
# sns.lineplot(x = 'time', y = 'speed', hue = 'lane', data = M42_6111A_speeds)
# =============================================================================

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

print(sensspeed('M42/6111A'))
#sns.lineplot(x = 'time', y = 'speed', hue = 'lane', data = sensspeed('M42/6111A'))
#plt.show()

#print(time_grouped.get_group("2017-10-09 00:58:00")["datetime"])
'''
Eloisa I leave the commented out code below for you to delete if you deem it fit to go... - Titus
'''
# =============================================================================
# #select columns from time dataset
# eight_thirty_speeds = dframe[datetime.time(8,30)][['geographic_address', 'speedlane_1', 'speedlane_2', 'avg_speed']]
#
#
# #put dataframe into a format readable for Seaborn visualisation
# eight_thirty_speeds = pd.melt(eight_thirty_speeds, id_vars = ['geographic_address'], var_name = 'lane', value_name = 'speed')
# =============================================================================

#create speed-time function that creates plottable data frame (melting disabled for easier plotting)
def stdframe(hour,minute):
    '''
    Function which selects speed columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib
    '''
    particular_df = time_grouped.get_group("2017-10-09 %s:%s:00" % (hour,minute))
    time_speeds = particular_df[['geographic_address', 'speedlane_1', 'speedlane_2', 'avg_speed']]
    #time_speeds = pd.melt(time_speeds, id_vars = ['geographic_address'], var_name = 'lane', value_name = 'speed')
    return time_speeds

#print(stdframe(8,30))

#create speed-time function that creates plottable data frame (melting disabled for easier plotting)
def otdframe(hour,minute):
    '''Function which selects speed columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib'''
    particular_df = time_grouped.get_group("2017-10-09 %s:%s:00" % (hour,minute))
    time_occupancy = particular_df[['geographic_address', 'occupancylane_1', 'occupancylane_2', 'avg_occupancy']]
    #time_speeds = pd.melt(time_speeds, id_vars = ['geographic_address'], var_name = 'lane', value_name = 'speed')
    return time_occupancy


#create function which saves figures of speed data for all sensors at an instant in time
def speedtimeslice(hour, minute, n):
    '''Input a time, output is a graph of the speed data at that instant across all sensors
    saves the figure as a .png image. Input "n" will be the name of the created figure.
    CAUTION: This function is dependant on stdframe().'''
    plt.figure(figsize=(10,3))
    plt.plot(stdframe(hour, minute)['geographic_address'], stdframe(hour, minute)['avg_speed'])
    plt.plot(stdframe(hour, minute)['geographic_address'], stdframe(hour, minute)['speedlane_1'])
    plt.plot(stdframe(hour, minute)['geographic_address'], stdframe(hour, minute)['speedlane_2'])
    axes = plt.gca()
    axes.set_ylim([0,170])
    axes.set_xlim(stdframe(hour,minute).iloc[0,0],stdframe(hour,minute).iloc[-1,0])
    axes.set_title('%s:%s'%(hour,minute))

    plt.legend(loc=3, fontsize='x-small')


    #plot vertical lines at sliproad sensors
    # On: K, M // Off: J, L
    for sensor in Sensors:
        if "K" in sensor:
            plt.axvline(sensor, color="b", linewidth=0.4)
        elif "J" in sensor:
            plt.axvline(sensor, color="r", linewidth=0.4)
    plt.savefig(cwd.joinpath("results",'%s.png' % (n)), dpi=300)
    plt.clf()

def occutimeslice(hour, minute, n):
    '''Input a time, output is a graph of the speed data at that instant across all sensors
    saves the figure as a .png image. Input "n" will be the name of the created figure.
    CAUTION: This function is dependant on stdframe().'''
    plt.figure(figsize=(10,3))
    plt.plot(otdframe(hour, minute)['geographic_address'], otdframe(hour, minute)['avg_occupancy'])
    plt.plot(otdframe(hour, minute)['geographic_address'], otdframe(hour, minute)['occupancylane_1'])
    plt.plot(otdframe(hour, minute)['geographic_address'], otdframe(hour, minute)['occupancylane_2'])
    axes = plt.gca()
    axes.set_ylim([0,110])
    axes.set_xlim(stdframe(hour,minute).iloc[0,0],stdframe(hour,minute).iloc[-1,0])
    axes.set_title('%s:%s'%(hour,minute))

    plt.legend(loc=3, fontsize='x-small')


    #plot vertical lines at sliproad sensors
    # On: K, M (Blue)// Off: J, L(Red)
    for sensor in Sensors:
        if "K" in sensor:
            plt.axvline(sensor, color="b", linewidth=0.4)
        elif "J" in sensor:
            plt.axvline(sensor, color="r", linewidth=0.4)
    plt.savefig(cwd.joinpath("results",'%s.png' % (n)), dpi=300)
    plt.clf()

def exportallslices(function):
    '''Export an image of a timeslice() graph for every minute in a day'''
    n=0
    for hour in list(range(0,24)):
        for minute in list(range(60)):
            n+=1
            function(hour,minute,n)

exportallslices(occutimeslice)
