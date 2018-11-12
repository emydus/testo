from matplotlib.widgets import Slider  # import the Slider widget
import numpy as np
import matplotlib.pyplot as plt
from math import pi
import pandas as pd 
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
	na_values = ['-1'])
#change header names to remove white spaces
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_').str.replace('(', '').str.replace(')', '')
#calculate average speed across lanes
df['avg_speed'] = df[['speedlane_1', 'speedlane_2', 'speedlane_3',
					'speedlane_4', 'speedlane_5', 'speedlane_6',
					'speedlane_7']].mean(axis=1)
#change time to datetime format
df['time'] = pd.to_datetime(df['time'],format= '%H:%M' ).dt.time

def group(column1):
	"""
	group by column and create separate dataframes
	"""
	i = 0 
	grouped = df.groupby(column1)
	dframe = {}
	timedic = {}
	for name, group in grouped:
		dframe[i] = group
		i = i+1
		timedic[name] = i
	return dframe, timedic
 
dframe, timedic = group('time')
a_min = timedic[datetime.time(int(input('minimum hour?')), int(input('minimum minute?')))]  # the minimial value of the parameter a
a_max = timedic[datetime.time(int(input('maximum hour?')), int(input('maximum minute?')))]  # the maximal value of the parameter a
a_init = a_min  # the value of the parameter a to be used initially, when the graph is created
fig = plt.figure(figsize=(8,3))
plot_ax = plt.axes([0.1, 0.2, 0.8, 0.65])
slider_ax = plt.axes([0.1, 0.05, 0.8, 0.05])
# in plot_ax, plot the function with the initial value of the parameter a
plt.axes(plot_ax) # select plot_ax
wid_plot, = plt.plot(dframe[a_init]['geographic_address'], dframe[a_init]['avg_speed'], 'r')
plt.xlim(0, len(dframe[1]))
plt.ylim(0, 200)
#create the slider
a_slider = Slider(slider_ax,      # the axes object containing the slider
                  'a',            # the name of the slider parameter
                  (a_min/60)*100,          # converts minutes to hours
                  (a_max/60)*100,          # maximal value of the parameter
                  valinit=a_init  # initial value of the parameter
                  )
# Ddefine a function that will be executed each time the value
# indicated by the slider changes. The variable of this function will
# be assigned the value of the slider.
def update(a):
    wid_plot.set_ydata(dframe[round(a)]['avg_speed']) 
    wid_plot.set_xdata(dframe[round(a)]['geographic_address'])# set new y-coordinates of the plotted points
    fig.canvas.draw_idle()          # redraw the plot
# specify that the slider needs to
# execute the above function when its value changes
a_slider.on_changed(update)
plt.show()