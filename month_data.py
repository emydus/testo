
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
#convert to datetime
dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
dframe["date"] = pd.to_datetime(dframe["date"],format="%d/%m/%y %H:%M")
dframe = dframe.drop(columns='time')
dframe = dframe.rename(columns = {'date':'datetime'})
#create an average speed column
dframe['avg_speed'] = dframe[['speedlane_1', 'speedlane_2', 'speedlane_3',
					'speedlane_4', 'speedlane_5', 'speedlane_6',
					'speedlane_7']].mean(axis=1)
#set index to datetime index
dframe = dframe.set_index(pd.DatetimeIndex(dframe['datetime']))
#average speed over 30min intervals
dframe['avg_speed'] = dframe.avg_speed.resample('30min').mean()
dframe = dframe[np.isfinite(dframe['avg_speed'])]
#select several geographic addresses and take an average of the speeds across them
dframe1 = dframe[dframe['geographic_address'].isin(['M42/6292A', 'M42/6293A', 'M42/6294A'])]
dframe1 = dframe1.groupby(pd.Grouper('datetime')).mean()
dframe2 = dframe1.reset_index()
#plot avg speed against time
plt.plot(dframe2['datetime'], dframe2['avg_speed'])
plt.show()

# dframe3 = dframe2[['datetime', 'avg_speed']]
# m = Prophet()
# m.fit(dframe3)

# future = m.make_future_dataframe(periods=24)
# future.tail()
# forecast = m.predict(future)
# forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail()
# fig1 = m.plot(forecast)
# plt.show()
