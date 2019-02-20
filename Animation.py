'''
Edited by Titus 15/02/19:
Added local edits of this file to master file
Cleaned up some of the code and added a function to plot headway and flow.
'''
import pandas as pd
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import datetime
from pathlib import Path
import numpy as np
import os

# OLD VERSION
# =============================================================================
# #Find relative path to data (see Misc / yjt_master.py)
# gdrive = os.path.dirname(os.path.dirname(__file__))
# data = os.path.join(gdrive, 'M42 B Carriageway 40091017.tcd.csv')
#
# #import data as a panda dataframe
# df = pd.read_csv(data, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Flow(Category 1)',
# 	'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
# 	'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
# 	'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
# 	'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
# 	'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
# 	'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
# 	'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
# 	na_values = ['-1', '0.0'])
#
# #change header names to remove white spaces
# df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
#
# #calculate average speed across lanes
# df['avg_speed'] = df[['speedlane_1', 'speedlane_2', 'speedlane_3',
# 					'speedlane_4', 'speedlane_5', 'speedlane_6',
# 					'speedlane_7']].mean(axis=1)
#
# #change time to datetime format
# df['time'] = pd.to_datetime(df['time'],format= '%H:%M' ).dt.time
# =============================================================================

#Find relative path to data (see pickle_reader.py)
cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
dataA = cwd.joinpath("data",'M42 A Carriageway 40091017.tcd.csv')

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
        na_values = ['-1', '0.0'])
    #change header names to remove white spaces
    df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
    df.columns = df.columns.str.replace('(', '').str.replace(')', '')
    #datetime_format
    df["date"] = df["date"].map(str) + " " + df["time"]
    df["date"] = pd.to_datetime(df["date"],format="%d-%m-%y %H:%M")
    df = df.drop(columns='time')
    #column_format
    df = df.rename(columns = {"date":"datetime"})
    return df


dfA = data_pdreadin(dataA)


def carriage_mean(dataf,column_name):
    dataf['avg_' + column_name] = dataf[[column_name + 'lane_1', column_name + 'lane_2',
         column_name + 'lane_3', column_name + 'lane_4', column_name + 'lane_5',column_name + 'lane_6',
         column_name + 'lane_7']].mean(axis=1)
    return dataf

#calculate average speed across lanes
dfA = carriage_mean(dfA,"speed")
#calculate average occupancy across all lanes:
dfA = carriage_mean(dfA,"occupancy")
#calculate average flow across all lanes:
dfA = carriage_mean(dfA,"flow")
#calculate average headway across all lanes:
dfA = carriage_mean(dfA,"headway")

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



Sensors=list(dict.fromkeys(dfA['geographic_address']))


# Create function which outputs speeds for all times dataframe for a single sensor
def sensspeed(sensorname):
    '''Takes the name of a sensor, outputs the speed data for all times, ready for plotting.
    Make sure input is of the from: 'M42/6111A' (ie uses slashes, not underscores).'''
    particular_df = geo_grouped.get_group(sensorname)
    SensorSpeeds = particular_df[['datetime','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
    SensorSpeeds = pd.melt(SensorSpeeds, id_vars = ['time'], var_name = 'lane', value_name = 'speed')
    return SensorSpeeds

############################################################################

#create speed-time function that creates plottable data frame (melting disabled for easier plotting)
def stdframe(hour,minute):
    '''
    Function which selects speed columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib
    '''
    particular_df = time_grouped.get_group("2017-10-09 %s:%s:00" % (hour,minute))
    time_speeds = particular_df[['geographic_address', 'speedlane_1', 'speedlane_2', 'avg_speed']]

    return time_speeds

#create occupancy-time function that creates plottable data frame (melting disabled for easier plotting)
def otdframe(hour,minute):
    '''Function which selects occupancy columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib'''
    particular_df = time_grouped.get_group("2017-10-09 %s:%s:00" % (hour,minute))
    time_occupancies = particular_df[['geographic_address', 'occupancylane_1', 'occupancylane_2', 'avg_occupancy']]

    return time_occupancies

#create flow-time function that creates plottable data frame (melting disabled for easier plotting)
def ftdframe(hour,minute):
    '''Function which selects flow columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib'''
    particular_df = time_grouped.get_group("2017-10-09 %s:%s:00" % (hour,minute))
    time_flows = particular_df[['geographic_address', 'flowlane_1', 'flowlane_2', 'avg_flow']]

    return time_flows


#create headway-time function that creates plottable data frame (melting disabled for easier plotting)
def htdframe(hour,minute):
    '''Function which selects headway columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib'''
    particular_df = time_grouped.get_group("2017-10-09 %s:%s:00" % (hour,minute))
    time_headways = particular_df[['geographic_address', 'headwaylane_1', 'headwaylane_2', 'avg_headway']]

    return time_headways


############################################################################

#create function which saves figures of speed data for all sensors at an instant in time
def speedtimeslice(hour, minute, n):
    '''Input a time, output is a graph of the speed data at that instant across all sensors
    saves the figure as a .png image. Input "n" will be the name of the created figure.
    CAUTION: This function is dependant on stdframe().'''
    plt.figure(figsize=(10,3))
    plt.plot(stdframe(hour, minute)['geographic_address'], stdframe(hour, minute)['avg_speed'], label='Average')
    plt.plot(stdframe(hour, minute)['geographic_address'], stdframe(hour, minute)['speedlane_1'], label='Lane 1')
    plt.plot(stdframe(hour, minute)['geographic_address'], stdframe(hour, minute)['speedlane_2'], label='Lane 2')
    axes = plt.gca()
    axes.set_ylim([0,170])
    axes.set_xlim(stdframe(hour,minute).iloc[0,0],stdframe(hour,minute).iloc[-1,0])
    axes.get_xaxis().set_ticks([])
    axes.set_title('%s:%s'%(hour,minute))

    # Set hlines for conjestion judgement
    Speedlines = [30,40,50,60]
    plt.hlines(Speedlines,xmin = stdframe(hour,minute).iloc[0,0],xmax = stdframe(hour,minute).iloc[-1,0], linestyles='dashed', linewidth = 0.7)
    plt.ylabel("Speed (km/h)")
    plt.xlabel("Sensors")
    plt.legend(loc=4, fontsize='x-small')



    # Plot vertical lines at sliproad sensors
    # On: K, M // Off: J, L
    # A Carriage
    for sensor in Sensors:
            if "K" in sensor:
                plt.axvline(sensor, color="b", linewidth=0.4)
            elif "J" in sensor:
                plt.axvline(sensor, color="r", linewidth=0.4)
# =============================================================================
#     # B Carriage
#     for sensor in Sensors:
#         if sensor in Sliplist:
#             if "L" in sensor:
#                 plt.axvline(sensor, color="r", linewidth=0.4)
#             else:
#                 plt.axvline(sensor, color="b", linewidth=0.4)
# =============================================================================
    plt.savefig('%s.png'%(n), dpi=300)
    plt.clf()
    plt.close('all')


def occutimeslice(hour, minute, n):
    '''Input a time, output is a graph of the occupancy data at that instant across all sensors
    saves the figure as a .png image. Input "n" will be the name of the created figure.
    CAUTION: This function is dependant on otdframe().'''
    plt.figure(figsize=(10,3))
    plt.plot(otdframe(hour, minute)['geographic_address'], otdframe(hour, minute)['avg_occ'], label='Average')
    plt.plot(otdframe(hour, minute)['geographic_address'], otdframe(hour, minute)['occupancylane_1'], label='Lane 1')
    plt.plot(otdframe(hour, minute)['geographic_address'], otdframe(hour, minute)['occupancylane_2'], label='Lane 2')
    axes = plt.gca()
    axes.set_ylim([0,110])
    axes.set_xlim(stdframe(hour,minute).iloc[0,0],stdframe(hour,minute).iloc[-1,0])
    axes.get_xaxis().set_ticks([])
    axes.set_title('%s:%s'%(hour,minute))

    # Set hlines for conjestion judgement
    Occulines = [50,60,70,100]
    plt.hlines(Occulines,xmin = otdframe(hour,minute).iloc[0,0],xmax = otdframe(hour,minute).iloc[-1,0], linestyles='dashed', linewidth = 0.7)
    plt.ylabel("Occupancy")
    plt.xlabel("Sensors")
    plt.legend(loc=1, fontsize='x-small')


    #plot vertical lines at sliproad sensors
    # On: K, M (Blue)// Off: J, L(Red)
    #A Carriage
    for sensor in Sensors:
        if "K" in sensor:
            plt.axvline(sensor, color="b", linewidth=0.4)
        elif "J" in sensor:
            plt.axvline(sensor, color="r", linewidth=0.4)
# =============================================================================
#     #B Carriage
#     for sensor in Sensors:
#         if sensor in Sliplist:
#             if "L" in sensor:
#                 plt.axvline(sensor, color="r", linewidth=0.4)
#             else:
#                 plt.axvline(sensor, color="b", linewidth=0.4)
# =============================================================================
    plt.savefig('%s.png'%(n), dpi=300)
    plt.clf()
    plt.close('all')

def flowtimeslice(hour, minute, n):
    '''Input a time, output is a graph of the flow data at that instant across all sensors
    saves the figure as a .png image. Input "n" will be the name of the created figure.
    CAUTION: This function is dependant on ftdframe().'''
    plt.figure(figsize=(10,3))
    plt.plot(ftdframe(hour, minute)['geographic_address'], ftdframe(hour, minute)['avg_flow'], label='Average')
    plt.plot(ftdframe(hour, minute)['geographic_address'], ftdframe(hour, minute)['flowlane_1'], label='Lane 1')
    plt.plot(ftdframe(hour, minute)['geographic_address'], ftdframe(hour, minute)['flowlane_2'], label='Lane 2')
    axes = plt.gca()
    axes.set_ylim([0,110])
    axes.set_xlim(stdframe(hour,minute).iloc[0,0],stdframe(hour,minute).iloc[-1,0])
    axes.get_xaxis().set_ticks([])
    axes.set_title('%s:%s'%(hour,minute))
    plt.ylabel("Flow")
    plt.xlabel("Sensors")
    plt.legend(loc=1, fontsize='x-small')


    #plot vertical lines at sliproad sensors
    # On: K, M (Blue)// Off: J, L(Red)
    #A Carriage
    for sensor in Sensors:
        if "K" in sensor:
            plt.axvline(sensor, color="b", linewidth=0.4)
        elif "J" in sensor:
            plt.axvline(sensor, color="r", linewidth=0.4)
# =============================================================================
#     #B Carriage
#     for sensor in Sensors:
#         if sensor in Sliplist:
#             if "L" in sensor:
#                 plt.axvline(sensor, color="r", linewidth=0.4)
#             else:
#                 plt.axvline(sensor, color="b", linewidth=0.4)
# =============================================================================
    plt.savefig('%s.png'%(n), dpi=300)
    plt.clf()
    plt.close('all')


def headtimeslice(hour, minute, n):
    '''Input a time, output is a graph of the headway data at that instant across all sensors
    saves the figure as a .png image. Input "n" will be the name of the created figure.
    CAUTION: This function is dependant on htdframe().'''
    plt.figure(figsize=(10,3))
    plt.plot(htdframe(hour, minute)['geographic_address'], htdframe(hour, minute)['avg_headway'], label='Average')
    plt.plot(htdframe(hour, minute)['geographic_address'], htdframe(hour, minute)['headwaylane_1'], label='Lane 1')
    plt.plot(htdframe(hour, minute)['geographic_address'], htdframe(hour, minute)['headwaylane_2'], label='Lane 2')
    axes = plt.gca()
    axes.set_ylim([0,300])
    axes.set_xlim(stdframe(hour,minute).iloc[0,0],stdframe(hour,minute).iloc[-1,0])
    axes.get_xaxis().set_ticks([])
    axes.set_title('%s:%s'%(hour,minute))
    plt.ylabel("Headway")
    plt.xlabel("Sensors")
    plt.legend(loc=1, fontsize='x-small')


    #plot vertical lines at sliproad sensors
    # On: K, M (Blue)// Off: J, L(Red)
    #A Carriage
    for sensor in Sensors:
        if "K" in sensor:
            plt.axvline(sensor, color="b", linewidth=0.4)
        elif "J" in sensor:
            plt.axvline(sensor, color="r", linewidth=0.4)
# =============================================================================
#     #B Carriage
#     for sensor in Sensors:
#         if sensor in Sliplist:
#             if "L" in sensor:
#                 plt.axvline(sensor, color="r", linewidth=0.4)
#             else:
#                 plt.axvline(sensor, color="b", linewidth=0.4)
# =============================================================================
    plt.savefig('%s.png'%(n), dpi=300)
    plt.clf()
    plt.close('all')


############################################################################

def exportallslices(function):
    '''Export an image of a timeslice() graph for every minute in a day'''
    n=0
    for hour in list(range(0,24)):
        for minute in list(range(60)):
            n+=1
            function(hour,minute,n)

exportallslices(headtimeslice)
