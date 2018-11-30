import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from fbprophet import Prophet
path =r'/Users/Eloisa/Google_Drive/MWay_Comms/subset' # use your path
allFiles = glob.glob(path + "/*.csv")
frame = pd.DataFrame()
list_ = []
#loop through all csv files and concatenate into a dataframe
for file in allFiles:
    df = pd.read_csv(file, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Flow(Category 1)', 
	'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)', 
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

def averagevar(variable):
	"""
	calculates the average of specified variable across lanes and creates column
	at the end of the dataframe
	"""
	dframe['avg_'+ variable] = dframe[[variable +'lane_1', variable + 'lane_2', variable + 'lane_3',
					variable + 'lane_4', variable + 'lane_5', variable + 'lane_6',
					variable + 'lane_7']].mean(axis=1)
	return dframe['avg_'+variable]
averagevar('speed')
averagevar('occupancy')
averagevar('flow')

#plot average speed across all days for each time
dframe["time"] = pd.to_datetime(dframe["time"],format="%H:%M")
dframe = dframe.groupby(pd.Grouper('time')).mean()
print(dframe)
dframe2 = dframe.reset_index()
plt.plot(dframe2['time'], dframe2['avg_speed'])
plt.show()


