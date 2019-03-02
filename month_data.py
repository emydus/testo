
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
# from fbprophet import Prophet
# from fbprophet.diagnostics import cross_validation
# from fbprophet.plot import plot_cross_validation_metric
import seaborn as sns
from scipy import stats

# workdir = os.path.dirname(__file__)
# datafolderpath = os.path.join(workdir,"data")
# allFiles = glob.glob(datafolderpath + "/*.csv")
def loadfiles(allFiles):
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
    # dframe["date"] = dframe["date"].map(str) + " " + dframe["time"]
    # dframe["date"] = pd.to_datetime(dframe["date"],format="%d/%m/%y %H:%M")
    # dframe = dframe.drop(columns='time')
    # dframe = dframe.rename(columns = {'date':'datetime'})
    dframe['date'] = pd.to_datetime(dframe['date'], format='%d/%m/%y')
    return dframe

# path =r'/Users/Eloisa/Google Drive/MWay_Comms/Oct_2018'
path = 'C:/Users/Eloisa/Google Drive/MWay_Comms/Oct_2018' # use your path
allFiles = glob.glob(path + "/*.csv")
dframe = loadfiles(allFiles)


# Mondays = dframe.loc[['2018-10-01', '2018-10-08', '2018-10-15', '2018-10-22', '2018-10-29']]
# Tuesdays = dframe.loc[dframe['date'].isin(['2018-10-02', '2018-10-09', '2018-10-16', '2018-10-23', '2018-10-30'])].index
# Wednesdays = dframe.loc[dframe['date'].isin(['2018-10-03', '2018-10-10', '2018-10-17', '2018-10-24', '2018-10-31'])].index
# Thursdays = dframe.loc[dframe['date'].isin(['2018-10-04', '2018-10-11', '2018-10-18', '2018-10-25'])].index
# Fridays = dframe.loc[dframe['date'].isin(['2018-10-05', '2018-10-12', '2018-10-19', '2018-10-26'])].index
# Saturdays = dframe.loc[dframe['date'].isin(['2018-10-06', '2018-10-13', '2018-10-20', '2018-10-27'])].index
# Sundays = dframe.loc[dframe['date'].isin(['2018-10-07', '2018-10-14', '2018-10-21', '2018-10-28'])].index
# dframe['day'] = np.nan
# dframe['day'].loc[['2018-10-01', '2018-10-08', '2018-10-15', '2018-10-22', '2018-10-29']] = 'monday'
# dframe['day'].loc[['20181001', '20181008', '20181015', '20181022', '20181029']] = 'monday'
# dframe['day'].iloc[Tuesdays] = 'tuesday'
# dframe['day'].iloc[Wednesdays] = 'wednesday'
# dframe['day'].iloc[Thursdays] = 'thursday'
# dframe['day'].iloc[Fridays] = 'friday'
# dframe['day'].iloc[Saturdays] = 'saturday'
# dframe['day'].iloc[Sundays] = 'sunday'


def averagevar(dframe, variable):
    """
    calculates the average of specified variable across lanes and creates column
    at the end of the dataframe
    """
    dframe['avg_'+ variable] = dframe[[variable +'lane_1', variable + 'lane_2', variable + 'lane_3',
                    variable + 'lane_4', variable + 'lane_5', variable + 'lane_6',
                    variable + 'lane_7']].mean(axis=1)
    return dframe['avg_'+ variable]

def occupancy_flow(dframe):
    """plot occupancy and flow against time to observe relationship"""

    #plot avg speed against time
    avg_flow = plt.plot(dframe['datetime'], dframe['avg_flow'])
    avg_occupancy = plt.plot(dframe['datetime'], dframe['avg_occupancy'])
    plt.legend()
    plt.show()

def resample_average(dframe):
    """average speed over 30 min intervals. select several geographic addresses
    and take an average of the speeds across them"""
    #set index to datetime index
    dframe = dframe.set_index(pd.DatetimeIndex(dframe['datetime']))
    #average speed over 30min intervals
    dframe['avg_speed'] = dframe.avg_speed.resample('10min').mean()
    dframe = dframe[np.isfinite(dframe['avg_speed'])]
    #select several geographic addresses and take an average of the speeds across them
    dframe1 = dframe[dframe['geographic_address'].isin(['M42/6292A', 'M42/6293A', 'M42/6294A'])]
    dframe1 = dframe1.groupby(pd.Grouper('datetime')).mean()
    dframe2 = dframe1.reset_index()
    return dframe2

def drop_dates(dframe):
    drop_list = dframe[dframe["datetime"].isin(pd.date_range("2018-10-1", "2018-10-20"))]
    return drop_list

def fb_forecast(dframe2):
    """Uses Facebook prophet API to predict future traffic data"""
    dframe3 = dframe2[['datetime', 'avg_speed']]
    dframe3 = dframe3.rename(columns = {'datetime':'ds', 'avg_speed':'y'})
    m = Prophet(changepoint_prior_scale=0.01).fit(dframe3)
    future = m.make_future_dataframe(periods=300, freq='H')
    fcst = m.predict(future)
    # fig = m.plot(fcst)
    # plt.show()
    return fcst

# def fb_forecast(test)
dframe['avg_speed'] = averagevar(dframe, 'speed')
# dframe_drop = drop_dates(dframe)
# forecast = fb_forecast(dframe)

def forecast_test(forecast, dframe2):
    forecast = forecast.rename(columns = {'ds':'datetime1', 'yhat':'avg_speed1'})
    forecast = forecast[['datetime1', 'avg_speed1']]
    dframe2 = dframe[['datetime', 'avg_speed']]
    merged_df = forecast.merge(dframe2, left_on='datetime1', right_on='datetime', how='inner')
    actual_traffic = merged_df['avg_speed']
    forecasted_traffic = merged_df['avg_speed1']
    merged_df['normalised_residual'] = ((actual_traffic - forecasted_traffic)/actual_traffic) * 100
    sns.distplot(merged_df['normalised_residual'])
    plt.show()


def probability_(dframe):
    mean = dframe['speedlane_1'].mean()
    stdev = dframe['speedlane_1'].std()
    speed = 60
    probability = stats.norm.cdf(speed, mean, stdev)
    print(probability)


def normaldist_test(df):
    """tests if distribution can be considered a normal distribution"""
    k2, p = stats.normaltest(df['speedlane_1'])
    alpha = 1e-3
    print("p = {:g}".format(p))
    if p < alpha:  # null hypothesis: x comes from a normal distribution
        print("The null hypothesis can be rejected")
    else:
        print("The null hypothesis cannot be rejected")

dframe = dframe[np.isfinite(dframe['speedlane_1'])]
# sns.distplot(dframe['speedlane_1'], fit = stats.norm)
# plt.show()


# plt.plot(merged_df['datetime'], actual_traffic, label = 'actual traffic')
# plt.plot(merged_df['datetime'], forecasted_traffic, label = 'forecasted traffic')
# plt.legend()
# plt.xlabel('Time')
# plt.ylabel('Average Speed')
# plt.show()


# df_cv = cross_validation(m, initial='4 days', period='9 days', horizon = '4 days')
# df_cv.head()
# fig = plot_cross_validation_metric(df_cv, metric='mape')

dframe['day'] = dframe['date'].dt.weekday_name

sns.violinplot(x="day", y="avg_speed", data=dframe)
plt.show()
