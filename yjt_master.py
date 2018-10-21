import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

"""
yjt: Finding relative paths to data
'gdrive' is the relative path to our working directory, 'MWay Comms Project Group'
__file__ gives the absolute path to the script file.
Each os.path.dirname() call gives the directory above it.
os.path.join() searches for the file in subdirectories, like so:
    filename = os.path.join(absdirname, 'relative', 'path', 'to', 'file', 'you' , 'want')
So you can customise this code to find your data :)
"""

gdrive = os.path.dirname(os.path.dirname(__file__))
data = os.path.join(gdrive, 'M42 A Carriageway 40091017.tcd.csv')
#print(gdrive,'\n',data) # FOR DEMONSTRATION

"""
c. Eloisa Paver
"""

# Import data as a panda dataframe (ADJUSTED TO REMOVE EMPTY COLUMNS / LANES,
# ADDED EXTRA IDENTIFIER COLUMNS)
df = pd.read_csv(data,
	usecols = ['Geographic Address','CO Address','LCC Address','Transponder Address',
    'Device Address','Date','Time','Number of Lanes','Flow(Category 1)', 
	'Flow(Category 2)','Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)', 
	'Speed(Lane 2)','Speed(Lane 3)','Speed(Lane 4)','Flow(Lane 1)','Flow(Lane 2)',
    'Flow(Lane 3)','Flow(Lane 4)','Occupancy(Lane 1)','Occupancy(Lane 2)', 
	'Occupancy(Lane 3)','Occupancy(Lane 4)','Headway(Lane 1)','Headway(Lane 2)',
    'Headway(Lane 3)','Headway(Lane 4)'],
    na_values = ['-1','0.0'])

# Change header names to remove white spaces
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')
df.columns = df.columns.str.replace('(', '').str.replace(')', '')

#print(df.columns)

# combining date and time to a date-time format and removing time column
# =============================================================================
# df['date'] = df[['date','time']].apply(lambda x: ' '.join(x), axis=1)
# =============================================================================
# inefficient code above

df["date"] = df["date"].map(str) + " " + df["time"]
df["date"] = pd.to_datetime(df["date"],format="%d-%m-%y %H:%M")
df = df.drop(columns='time')

# Condensing identifying info into identifier column, renaming to datetime

df["geographic_address"] = (pd.Series(data = df["geographic_address"].map(str)+" "+
  df["co_address"].map(str)+" "+df["lcc_address"].map(str)+" "+
  df["transponder_address"].map(str)+" "+df["device_address"].map(str)))
df = df.drop(columns=["co_address","lcc_address","transponder_address",
                      "device_address"])
df = df.rename(columns = {'geographic_address':'identity',"date":"datetime"})

def group(column):
	"""
    Group by column and create separate dataframes
	dframe is a dictionary with the identifiers as keys, values as dataframes
    Seems to run quite slowly when called D:
    c. Tom
    """
	grouped = df.groupby(column)
	dframe = {}
	for name, group in grouped:
		dframe[name] = group
	return(dframe)

dframe = group('identity')

print(dframe)

sensors = list(dict.fromkeys(df["identity"]))

#for i in df:
    

#SensorFrame = pd.DataFrame(data=Sensors,index=Sensors)
#print(SensorFrame)

# Using .describe to get basic analysis (mean of all variables)
# =============================================================================
# data_a = pd.DataFrame(df.describe(include='float'))
# print(data_a.loc["min"])
# =============================================================================

"""
Task 2: Functions to define plotting everything against everything else
"""



# =============================================================================
# """
# DONE BY TOM
# Task 1: Comparing Tom's speed-time graphs vs occupancy-time graphs (16/10)
# c. Tom's code w. modifications follows:
# """
# 
# #calculate average speed across lanes
# df['avg_speed'] = df[['speedlane_1', 'speedlane_2', 'speedlane_3',
# 					'speedlane_4', 'speedlane_5', 'speedlane_6',
# 					'speedlane_7']].mean(axis=1)
# 
# #change time to datetime format
# df['time'] = pd.to_datetime(df['time'],format= '%H:%M' ).dt.time
# def group(column):
# 	"""
# 	group by column and create separate dataframes
# 	"""
# 	grouped = df.groupby(column)
# 	dframe = {}
# 	for name, group in grouped:
# 		dframe[name] = group
# 	return(dframe)
# dframe = group('geographic_address')
# 
# #Sensors=list(set(df['geographic_address'])) # Dated Below should preserve order
# Sensors=list(dict.fromkeys(df['geographic_address']))
# print(len(Sensors))
# 
# #Plots speeds against time
# for pos in Sensors[:]:
#     speeds= dframe[pos][['time','speedlane_1', 'speedlane_2', 'speedlane_3', 'avg_speed']]
#     speeds = pd.melt(speeds, id_vars = ['time'], var_name = 'lane', value_name = 'speed')
#     sns.lineplot(x = 'time', y = 'speed', hue = 'lane', data = speeds).set_title(pos)
#     plt.show()
#     del speeds
# =============================================================================

