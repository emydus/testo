#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 05:02:55 2018

@author: yjt_yujie
"""
import glob
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
import dask.dataframe as dd

workdir = os.path.dirname(__file__)
datafolderpath = os.path.join(workdir,"data")

df = dd.read_csv(datafolderpath + '/*.csv',  # normal Pandas code
                 blocksize=64000000)  # break text into 64MB chunks

dd.compute(df)
print(df.shape)

# =============================================================================
# """
# yjt: Finding relative paths to data
# 'workdir' is the relative path to our working directory, 'PHY346_MWayComms'
# __file__ gives the absolute path to the script file.
# Each os.path.dirname() call gives the directory above it.
# os.path.join() searches for the file in subdirectories, like so:
#     filename = os.path.join(absdirname, 'relative', 'path', 'to', 'file', 'you' , 'want')
# So you can customise this code to find your data :)
# """
# 
# workdir = os.path.dirname(__file__)
# dataA = os.path.join(workdir,"data", 'M42 A Carriageway 40091017.tcd.csv')
# dataB = os.path.join(workdir,"data", 'M42 B Carriageway 40091017.tcd.csv')
# print(gdrive,'\n',data) # FOR DEMONSTRATION
# """
# c. Eloisa Paver
# """
# 
# # Import data as a panda dataframe (ADJUSTED TO REMOVE EMPTY COLUMNS / LANES,
# # ADDED EXTRA IDENTIFIER COLUMNS)
# 
# def data_pdreadin(data):
#     dataf = pd.read_csv(data,
# 	usecols = ['Geographic Address','CO Address','LCC Address','Transponder Address',
#     'Device Address','Date','Time','Number of Lanes','Flow(Category 1)',
# 	'Flow(Category 2)','Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)',
# 	'Speed(Lane 2)','Speed(Lane 3)','Speed(Lane 4)','Flow(Lane 1)','Flow(Lane 2)',
#     'Flow(Lane 3)','Flow(Lane 4)','Occupancy(Lane 1)','Occupancy(Lane 2)',
# 	'Occupancy(Lane 3)','Occupancy(Lane 4)','Headway(Lane 1)','Headway(Lane 2)',
#     'Headway(Lane 3)','Headway(Lane 4)'],
#     na_values = ['-1','0.0'])
#     
#     dataf.columns = dataf.columns.str.strip().str.lower().str.replace(' ', '_')
#     dataf.columns = dataf.columns.str.replace('(', '').str.replace(')', '')
#     
#     dataf = dataf.drop(columns=["co_address","lcc_address","transponder_address",
#                       "device_address"])
#     
#     return dataf
# 
# dfA = data_pdreadin(dataA)
# #dfB = data_pdreadin(dataB)
# 
# def datetime_format(dataf):
#     dataf["date"] = dataf["date"].map(str) + " " + dataf["time"]
#     dataf["date"] = pd.to_datetime(dataf["date"],format="%d-%m-%y %H:%M")
#     dataf = dataf.drop(columns='time')
#     dataf = dataf.rename(columns = {'geographic_address':'identity',"date":"datetime"})
#     return dataf
# 
# dfA = datetime_format(dfA)
# 
# print(dfA["datetime"])
# =============================================================================
# =============================================================================
# workdir = os.path.dirname(__file__)
# datafolderpath = os.path.join(workdir,"data")
# allFiles = glob.glob(datafolderpath + "/*.csv")
# 
# frame = pd.DataFrame()
# list_ = []
# 
# #loop through all csv files and concatenate into a dataframe
# for file in allFiles:
#     df = pd.read_csv(file, usecols = ['Geographic Address', 'Date', 'Time', 'Number of Lanes', 'Flow(Category 1)', 
# 	'Flow(Category 2)', 'Flow(Category 3)', 'Flow(Category 4)', 'Speed(Lane 1)', 
# 	'Speed(Lane 2)', 'Speed(Lane 3)', 'Speed(Lane 4)', 'Speed(Lane 5)', 'Speed(Lane 6)',
# 	'Speed(Lane 7)', 'Flow(Lane 1)', 'Flow(Lane 2)', 'Flow(Lane 3)', 'Flow(Lane 4)', 
# 	'Flow(Lane 5)', 'Flow(Lane 6)', 'Flow(Lane 7)', 'Occupancy(Lane 1)', 'Occupancy(Lane 2)', 
# 	'Occupancy(Lane 3)', 'Occupancy(Lane 4)', 'Occupancy(Lane 5)', 'Occupancy(Lane 6)', 
# 	'Occupancy(Lane 7)', 'Headway(Lane 1)', 'Headway(Lane 2)', 'Headway(Lane 3)', 
# 	'Headway(Lane 4)', 'Headway(Lane 5)', 'Headway(Lane 6)', 'Headway(Lane 7)',],
#     blocksize=64000000, na_values = ['-1'])
#     list_.append(df)
# dframe = pd.concat(list_)
# =============================================================================

# =============================================================================
# from multiprocessing import Pool
# 
# def f(x):
#     return x*x
# 
# if __name__ == '__main__':
#     with Pool(5) as p:
#         print(p.map(f, [1, 2, 3]))
# =============================================================================

# =============================================================================
# from multiprocessing import Process
# import os
# 
# def info(title):
#     print(title)
#     print('module name:', __name__)
#     print('parent process:', os.getppid())
#     print('process id:', os.getpid())
# 
# def f(name):
#     info('function f')
#     print('hello', name)
# 
# if __name__ == '__main__':
#     info('main line')
#     p = Process(target=f, args=('bob',))
#     p.start()
#     p.join()
# =============================================================================
