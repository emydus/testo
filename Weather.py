"""
Edited by Titus (3/12/2018)
- Changed "dfA" to "dfM" to make it easier to separate motorway (dfM) and weather (dfW)
    dataframes
- Had to revert back to old data import method, as pickler method was giving "Index error: pop from empty list"
    seems to be caused by gaps in weather data file (empty columns). Can maybe iterate through with something to 
    fill the gaps with 0's, or NaN's? 
- Found weather sensors' id's that are closest to M42 based off coordinates: "203800","184250","201180"
    This could be a bit more refined - is only rough.
"""
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import datetime as dt


#Find relative path to data (see pickle_reader.py)
cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
Mdata = cwd.joinpath("data",'40101018.tcd.csv.pkl.gz')
Wdata = cwd.joinpath("data/weather","WH where ob_time between '2018-10-01' and '2018-11-01'.csv.pkl.gz")

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
    df["date"] = pd.to_datetime(df["date"],format="%d/%m/%y %H:%M")
    df = df.drop(columns='time')
    #column_format
    df = df.rename(columns = {"date":"datetime"})
    return df

def Wdata_pdreadin(file):
    df = pd.read_pickle(file)
    # TO-DO : NEED TO IMPLEMENT REPLACEMENT FOR NA_VALUES=["-1","0.0"]

    #datetime_format
    df["date"] = pd.to_datetime(df["ob_time"],format="%Y-%m-%d %H:%M:%S")
    #drop unwanted columns  
    df = df.drop(columns=["ob_time","id","id_type", "met_domain_name","version_num","src_id",
                          "rec_st_ind","wind_speed_unit_id","src_opr_type","wind_direction",
                          "wind_speed","prst_wx_id","past_wx_id_1","past_wx_id_2",
                          "cld_ttl_amt_id","low_cld_type_id","med_cld_type_id","hi_cld_type_id"
                          ,"cld_base_amt_id","cld_base_ht","msl_pressure", "cld_amt_id_1","cloud_type_id_1",
                          "cld_base_ht_id_1","cld_amt_id_2","cloud_type_id_2","cld_base_ht_id_2","cld_amt_id_3",
                          "cloud_type_id_3","cld_base_ht_id_3","cld_amt_id_4","cloud_type_id_4","cld_base_ht_id_4",
                          "vert_vsby","wetb_temp","stn_pres","alt_pres","ground_state_id","q10mnt_mxgst_spd",
                          "cavok_flag","cs_hr_sun_dur","wmo_hr_sun_dur","wind_direction_q","wind_speed_q",
                          "prst_wx_id_q","past_wx_id_1_q","past_wx_id_2_q","cld_ttl_amt_id_q",
                          "low_cld_type_id_q","med_cld_type_id_q","hi_cld_type_id_q","cld_base_amt_id_q",
                          "cld_base_ht_q","visibility_q","msl_pressure_q","air_temperature_q","dewpoint_q",
                          "wetb_temp_q","ground_state_id_q","cld_amt_id_1_q","cloud_type_id_1_q",
                          "cld_base_ht_id_1_q","cld_amt_id_2_q","cloud_type_id_2_q","cld_base_ht_id_2_q",
                          "cld_amt_id_3_q","cloud_type_id_3_q","cld_base_ht_id_3_q","cld_amt_id_4_q",
                          "cloud_type_id_4_q","cld_base_ht_id_4_q","vert_vsby_q","stn_pres_q",
                          "alt_pres_q","q10mnt_mxgst_spd_q","cs_hr_sun_dur_q","wmo_hr_sun_dur_q","meto_stmp_time",
                          "midas_stmp_etime","wind_direction_j","wind_speed_j","prst_wx_id_j","past_wx_id_1_j",
                          "past_wx_id_2_j","cld_amt_id_j","cld_ht_j","visibility_j","msl_pressure_j","air_temperature_j",
                          "dewpoint_j","wetb_temp_j","vert_vsby_j","stn_pres_j","alt_pres_j","q10mnt_mxgst_spd_j",
                          "rltv_hum","rltv_hum_j","snow_depth","snow_depth_q","drv_hr_sun_dur","drv_hr_sun_dur_q"])

    #column_format
    df = df.rename(columns = {"date":"datetime","air_temperature":"air_temp"})
    return df

dfM = data_pdreadin(Mdata)
dfW = Wdata_pdreadin(Wdata)


def carriage_mean(dataf,column_name):
    dataf['avg_' + column_name] = dataf[[column_name + 'lane_1', column_name + 'lane_2',
         column_name + 'lane_3', column_name + 'lane_4', column_name + 'lane_5',column_name + 'lane_6',
         column_name + 'lane_7']].mean(axis=1)
    return dataf

#calculate average speed across lanes
dfM = carriage_mean(dfM,"speed")
#calculate average occupancy across all lanes:
dfM = carriage_mean(dfM,"occupancy")

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

sensorDict_geo = sensorsD(dfM,"geographic_address")
sensorDict_time = sensorsD(dfM,"datetime")
uidDict_uid = sensorsD(dfW,"uid")
uidDict_time = sensorsD(dfW,"datetime")

#print(uidDict_uid)
# df_grouped (Create GroupBy object)
geo_grouped = dfM.groupby("geographic_address",sort=False)
time_grouped = dfM.groupby("datetime",sort=False)
# weather variants
uid_grouped = dfW.groupby("uid",sort=False)
w_time_grouped = dfW.groupby("datetime",sort=False)

def geochoice(index):
    return geo_grouped.get_group(sensorDict_geo[index])

def time_choice(index):
    return time_grouped.get_group(sensorDict_time[index])

def uidchoice(index):
    return uid_grouped.get_group(uidDict_uid[index])
    
def W_time_choice(index):
    return w_time_grouped.get_group(uidDict_time[index])

def W_time_uid_choice(index,hour):
    uidchoice = uid_grouped.get_group(uidDict_uid[index])
    return uidchoice.groupby("datetime",sort=False)
#    return senstime.get_group(uidDict_time[hour])




thechoice = uidchoice(2).reset_index().drop(columns=['index'])

iwant = thechoice["datetime"]
#print(iwant[1])
 
startdate = iwant[0]
enddate = iwant[iwant.index[-1]]
print(thechoice.between_time(startdate,enddate))

# =============================================================================
# hours24 = list(range(24))
# todaysweather = pd.DataFrame()
# for hour in hours24:
#     todaysweather = todaysweather.append(W_time_uid_choice(2,hour))
# print(todaysweather)
# =============================================================================
#print(uidchoice(2))
#print(W_time_choice(2))






#dftime = group('time')
#dfgeo_add = group('geographic_address')

Sensors=list(dict.fromkeys(dfM['geographic_address']))


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

#create function which outputs visibilities from a given sensor for all times 
def uidvis(uid):
    '''
    Takes the name of a sensor id, outputs the visibility data for all times.
    '''
    particular_df = uid_grouped.get_group(uid)
    idviss = particular_df[['datetime','visibility']]
    #idviss = pd.melt(idviss, id_vars = ['datetime'], var_name = 'lane', value_name = 'speed')
    return idviss

#print(uidvis(203800))

#sns.lineplot(x = 'time', y = 'speed', hue = 'lane', data = sensspeed('M42/6111A'))
#plt.show()

#print(time_grouped.get_group("2017-10-09 00:58:00")["datetime"])

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

#create visibility-time function that creates plottable data frame
def vistdframe(hour,minute):
    '''
    Function which selects visibility at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib
    '''
    particular_df = w_time_grouped.get_group("2018-10-10 %s:%s:00" % (hour,minute))
    time_viss = particular_df[['uid', 'visibility']]
    return time_viss

#print(vistdframe(7,0))

#create speed-time function that creates plottable data frame (melting disabled for easier plotting)
def otdframe(hour,minute):
    '''Function which selects speed columns at a specific time in the dataset, and creates a dataframe
    readable by seaborn/matplotlib'''
    particular_df = time_grouped.get_group("2017-10-09 %s:%s:00" % (hour,minute))
    time_occupancy = particular_df[['geographic_address', 'occupancylane_1', 'occupancylane_2', 'avg_occupancy']]
    #time_speeds = pd.melt(time_speeds, id_vars = ['geographic_address'], var_name = 'lane', value_name = 'speed')
    return time_occupancy


