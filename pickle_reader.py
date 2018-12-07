#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 07:39:58 2018

@author: yjt_yujie
"""
import pandas as pd
from pathlib import Path

# Gives relative path to current working directory
cwd = Path.cwd()
# Turns the relative path into an absolute one for your OS
cwd = cwd.resolve(strict=True)
# Navigates to the "data folder"
datafolderpath = cwd.joinpath("data")
# Creates a list for all files ending in .csv in the "data" folder
allfiles = list(datafolderpath.glob("**/*.pkl.gz"))
df_list = []

for file in allfiles:
    file = file.resolve(strict=True)
    print("Loading %s" % (file.name))
    df = pd.read_pickle(file)
    df_list.append(df)
    df_all = pd.concat(df_list)