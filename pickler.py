#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 06:50:34 2018

@author: yjt_yujie
"""
import glob
import pandas as pd
import os

workdir = os.path.dirname(__file__)
datafolderpath = os.path.join(workdir,"data")
allFiles = glob.glob(datafolderpath + "/*.csv")

for file in allFiles:
    df = pd.read_csv(file)
    df.to_pickle("%s.pkl.gz" % (file))