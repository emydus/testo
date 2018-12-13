#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 16:11:24 2018

@author: yjt_yujie
"""
import pandas as pd
from pathlib import Path
import dask.dataframe as dd
import matplotlib.pyplot as plt

cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
data = cwd.joinpath("data","*.tcd.csv")
dateparse = lambda x : dd.to_datetime(x, format="%d/%m/%y %H:%M", cache=True)

df = dd.read_csv(data, usecols=['Geographic Address', 'Date', 'Time', 'Number of Lanes',
        'Flow(Category 1)', 'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
        'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
        'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)',
        'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)',
        'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)',
        'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)',
        'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)'],
        na_values=['-1'], parse_dates={'datetime': ['Date', 'Time']}, date_parser=dateparse)

def corr1(dataf, cmethod):
    plt.figure()
    plt.matshow(dataf.corr(method=cmethod))
    locs, labels = plt.yticks()
    labels = ["no. of lanes", "flow_cat1", "speed", "flow", "occupancy", "headway"]
    locs = [0,1,5,9,13,17]
    plt.yticks(locs, labels)
    plt.xticks(locs, labels, rotation="vertical")
    plt.colorbar(spacing="uniform")
    plt.show()
    #plt.savefig(cwd.joinpath("results", 'linearcorr_A_0'))
    plt.close()

corr1(df,"pearson")

dd.compute()

#for file in allfiles:
#    file = file.resolve(strict=True)
#    print(file)
#    df = dd.read_csv(file)
#    df_list.append(df)
#    df_all = pd.concat(df_list)