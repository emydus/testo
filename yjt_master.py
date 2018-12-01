import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os
import bokeh
import glob

"""
yjt: Finding relative paths to data
'workdir' is the relative path to our working directory, 'PHY346_MWayComms'
__file__ gives the absolute path to the script file.
Each os.path.dirname() call gives the directory above it.
os.path.join() searches for the file in subdirectories, like so:
    filename = os.path.join(absdirname, 'relative', 'path', 'to', 'file', 'you' , 'want')
So you can customise this code to find your data :)
"""
workdir = os.path.dirname(__file__)
dataA = os.path.join(workdir,"data", 'M42 A Carriageway 40091017.tcd.csv.pkl.gz')
dataB = os.path.join(workdir,"data", 'M42 B Carriageway 40091017.tcd.csv.pkl.gz')
#print(gdrive,'\n',data) # FOR DEMONSTRATION

"""
c. Eloisa Paver
"""

# Import data as a panda dataframe (ADJUSTED TO REMOVE EMPTY COLUMNS / LANES,
# ADDED EXTRA IDENTIFIER COLUMNS)

def data_pdreadin(data):
    df = pd.read_pickle(data)
    return df

dfA = data_pdreadin(dataA)
dfB = data_pdreadin(dataB)

# Change header names to remove white spaces
def varname_format(dataf):
    dataf.columns = dataf.columns.str.strip().str.lower().str.replace(' ', '_')
    dataf.columns = dataf.columns.str.replace('(', '').str.replace(')', '')
    return dataf

# combining date and time to a date-time format and removing time column
# =============================================================================
# df['date'] = df[['date','time']].apply(lambda x: ' '.join(x), axis=1)
# =============================================================================
# inefficient code above

def datetime_format(dataf):
    dataf["date"] = dataf["date"].map(str) + " " + dataf["time"]
    dataf["date"] = pd.to_datetime(dataf["date"],format="%d-%m-%y %H:%M")
    dataf = dataf.drop(columns='time')
    return dataf

# Condensing identifying info into identifier column, renaming to datetime
def column_format(dataf):
#    df["geographic_address"] = (pd.Series(data = df["geographic_address"].map(str)+" "+
#    df["co_address"].map(str)+" "+df["lcc_address"].map(str)+" "+
#    df["transponder_address"].map(str)+" "+df["device_address"].map(str)))
    dataf = dataf.drop(columns=["co_address","lcc_address","transponder_address",
                      "device_address"])
    dataf = dataf.rename(columns = {'geographic_address':'identity',"date":"datetime"})
    return dataf

def data_cleanse(dataf):
    dataf = varname_format(dataf)
    dataf = datetime_format(dataf)
    dataf = column_format(dataf)
    return dataf

dfA = data_cleanse(dfA)
dfB = data_cleanse(dfB)

print(dfA.columns)

#def group(column):
#	"""
#    Group by column and create separate dataframes
#	dframe is a dictionary with the identifiers as keys, values as dataframes
#    Seems to run quite slowly when called D:
#    c. Tom
#    """
#	grouped = df.groupby(column)
#	dframe = {}
#	for name, group in grouped:
#		dframe[name] = group
#	return(dframe)

# =============================================================================
# """
# Replacement code for the above. grouped is a GroupBy object that isn't computed until
# operated on. It should be better to operate on the separate groups through groupby
# functions.
# """
# def sensorsD(dataf):
#     """
#     Create dictionary of keys and ids e.g for M42 A Carriageway 40091017,
#     (0,1,...189) & (M42/6111A...M42/6738J)
#     """
#     sensors = list(dict.fromkeys(dataf["identity"]))
#     sensorsD = {}
#     index = 0
#     for id in sensors:
#         sensorsD[index] = id
#         index += 1
#     return sensorsD
# 
# sensorDictA = sensorsD(dfA)
# sensorDictB = sensorsD(dfB)
# 
# # df_grouped (Create GroupBy object)
# id_groupedA = dfA.groupby("identity",sort=False)
# id_groupedB = dfB.groupby("identity",sort=False)
# 
# def groupchoiceA(index):
#     return id_groupedA.get_group(sensorDictA[index])
# 
# def groupchoiceB(index):
#     return id_groupedB.get_group(sensorDictB[index])
# 
# #print(groupchoiceA(36))
# 
# # Choosing groups by sensorsD[0,1,2...189] # DEMONSTRATION
# #print(id_groupedA.size())
# """
# Task 2: Functions to define plotting everything against everything else
# (given) columns -> (sensor) identity, datetime, no. of lanes, flow by category(averaged
# across lanes, 4 categories), (speed, flow, occupancy, headway) x 4 = 16
# 23 initial columns
# """
# 
# def carriage_mean(dataf,column_name):
#     dataf['avg_' + column_name] = dataf[[column_name + 'lane_1', column_name + 'lane_2',
#          column_name + 'lane_3', column_name + 'lane_4']].mean(axis=1)
#     return dataf
# 
# dfA = carriage_mean(dfA,'speed')
# dfA = carriage_mean(dfA,'flow')
# dfA = carriage_mean(dfA,'occupancy')
# dfA = carriage_mean(dfA,'headway')
# 
# dfB = carriage_mean(dfB,'speed')
# dfB = carriage_mean(dfB,'flow')
# dfB = carriage_mean(dfB,'occupancy')
# dfB = carriage_mean(dfB,'headway')
# 
# plt.matshow(dfA.corr(method='pearson'))
# =============================================================================
