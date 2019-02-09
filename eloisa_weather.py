"""
Edited by Eloisa 12/12
Thought I'd start my own program to analyse the weather data so I didn't
mess with Titus' code
"""
import pandas as pd
import os
import glob
import matplotlib.pyplot as plt
import numpy as np

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
    #change header names to remove white spaces
    dframe.columns = dframe.columns.str.strip().str.lower().str.replace(' ', '_')
    dframe.columns = dframe.columns.str.replace('(', '').str.replace(')', '').str.replace('/', '-')
    #convert to datetime
    dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
    dframe["date"] = pd.to_datetime(dframe["date"],format="%d/%m/%y %H:%M")
    dframe = dframe.drop(columns='time')
    dframe = dframe.rename(columns = {'date':'datetime'})
    return dframe

def loadweather(file):
    dframe = pd.read_csv(file, usecols=['src_id','ob_time', 'prst_wx_id', 'visibility'], na_values=['0'])
    dframe = dframe.rename(columns = {'ob_time':'datetime', 'src_id' : 'sensor', 'prst_wx_id':'weather_code'})
    dframe["datetime"] = pd.to_datetime(dframe["datetime"],format="%Y-%m-%d %H:%M:%S")
    return dframe

# path =r'/Users/Eloisa/Google Drive/MWay_Comms/Oct_2018'
t_path = 'C:/Users/Eloisa/Google Drive/MWay_Comms/Oct_2018' # use your path
allFiles = glob.glob(t_path + "/*.csv")
w_path = 'C:/Users/Eloisa/Google Drive/MWay_Comms'
w_csv = 'weather_data.csv'
w_file = os.path.join(w_path, w_csv)
t_dframe = loadtraffic(allFiles)
w_dframe = loadweather(w_file)
#select several geographic addresses/IDs in close proximity
t_dframe = t_dframe[t_dframe['geographic_address'].isin(['M42/6467A', 'M42/6451A', 'M42/6472A', 'M42/6477A', 'M42/6461A', 'M42/6458A'])]
w_dframe = w_dframe[w_dframe['sensor'].isin(['19187', '593'])]
def group(df, column):
   """
   group by column and create separate dataframes
   """
   grouped = df.groupby(column)
   dframe = {}
   for name, group in grouped:
       dframe[name] = group
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

averagevar(t_dframe, 'speed')
def resample_average(dframe):
    """average speed over 30 min intervals. select several geographic addresses
    and take an average of the speeds across them"""
    #set index to datetime index
    dframe = dframe.set_index(pd.DatetimeIndex(dframe['datetime']))
    #average speed over 30min intervals
    dframe['avg_speed'] = dframe.avg_speed.resample('60min').mean()
    dframe = dframe[np.isfinite(dframe['avg_speed'])]
    #average over selected sensors
    dframe1 = dframe.groupby(pd.Grouper('datetime')).mean()
    dframe2 = dframe1.reset_index()
    return dframe2

t_dframe = resample_average(t_dframe)
#average weather over selected sensors
w_dframe = w_dframe.groupby(pd.Grouper('datetime')).mean()

merged_df = t_dframe.merge(w_dframe, left_on='datetime', right_on='datetime', how='inner')
merged_df['visibility_km'] = merged_df['visibility']/ 100
visibility = plt.plot(merged_df['datetime'], merged_df['visibility_km'])
avg_speed =plt.plot(merged_df['datetime'], merged_df['avg_speed'])
plt.xlabel('datetime')
plt.legend()
plt.show()