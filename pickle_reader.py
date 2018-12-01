#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 07:39:58 2018

@author: yjt_yujie
"""
import glob
import pandas as pd
import os

workdir = os.path.dirname(__file__)
datafolderpath = os.path.join(workdir,"data")
allFiles = glob.glob(datafolderpath + "/*.pkl.gz")

list_ = []

for file in allFiles:
    df = pd.read_pickle(file)
    list_.append(df)
    print(df)