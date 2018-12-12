import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import bokeh

cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
dataA = cwd.joinpath("data", 'M42 A Carriageway 40091017.tcd.csv')
dataB = cwd.joinpath("data", 'M42 B Carriageway 40091017.tcd.csv')

def data_pdreadin(data):
    dataf = pd.read_csv(data,
	usecols = ['Geographic Address','CO Address','LCC Address','Transponder Address',
    'Device Address','Date','Time','Number of Lanes','Flow(Category 1)',
	'Flow(Category 2)','Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
	'Speed(Lane 2)','Speed(Lane 3)','Speed(Lane 4)','Flow(Lane 1)','Flow(Lane 2)',
    'Flow(Lane 3)','Flow(Lane 4)','Occupancy(Lane 1)','Occupancy(Lane 2)',
	'Occupancy(Lane 3)','Occupancy(Lane 4)','Headway(Lane 1)','Headway(Lane 2)',
    'Headway(Lane 3)','Headway(Lane 4)'],
    na_values = ['-1','0.0'])
    # Change header names to remove white spaces
    dataf.columns = dataf.columns.str.strip().str.lower().str.replace(' ', '_')
    dataf.columns = dataf.columns.str.replace('(', '').str.replace(')', '')
    # Combine "date" & "time" into datetime
    dataf["date"] = dataf["date"].map(str) + " " + dataf["time"]
    dataf["date"] = pd.to_datetime(dataf["date"], format="%d-%m-%y %H:%M")
    dataf = dataf.drop(columns='time')
    dataf = dataf.rename(columns={"date":"datetime"})
    # Drop unneeded columns
#    df["geographic_address"] = (pd.Series(data = df["geographic_address"].map(str)+" "+
#    df["co_address"].map(str)+" "+df["lcc_address"].map(str)+" "+
#    df["transponder_address"].map(str)+" "+df["device_address"].map(str)))
    dataf = dataf.drop(columns=["co_address", "lcc_address", "transponder_address",
                                "device_address"])
    return dataf

dfA = data_pdreadin(dataA)
dfB = data_pdreadin(dataB)

def sensorsD(dataf):
    """
    Create dictionary of keys and ids e.g for M42 A Carriageway 40091017,
    (0,1,...189) & (M42/6111A...M42/6738J)
    """
    sensors = list(dict.fromkeys(dataf["geographic_address"]))
    sensorsD = {}
    index = 0
    for i in sensors:
        sensorsD[index] = i
        index += 1
    return sensorsD

sensorDictA = sensorsD(dfA)
sensorDictB = sensorsD(dfB)

# df_grouped (Create GroupBy object)
geo_groupedA = dfA.groupby("geographic_address", sort=False)
geo_groupedB = dfB.groupby("geographic_address", sort=False)

def groupchoiceA(index):
    return geo_groupedA.get_group(sensorDictA[index])

def groupchoiceB(index):
    return geo_groupedB.get_group(sensorDictB[index])

def carriage_mean(dataf, column_name):
    dataf['avg_' + column_name] = dataf[[column_name + 'lane_1', column_name + 'lane_2',
         column_name + 'lane_3', column_name + 'lane_4']].mean(axis=1)
    return dataf

dfA = carriage_mean(dfA, 'speed')
dfA = carriage_mean(dfA, 'flow')
dfA = carriage_mean(dfA, 'occupancy')
dfA = carriage_mean(dfA, 'headway')

dfB = carriage_mean(dfB, 'speed')
dfB = carriage_mean(dfB, 'flow')
dfB = carriage_mean(dfB, 'occupancy')
dfB = carriage_mean(dfB, 'headway')

plt.matshow(dfA.corr(method='pearson'))
