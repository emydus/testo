#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 06:50:34 2018

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
allfiles = list(datafolderpath.glob("**/*.csv"))

for file in allfiles:
    print("Loading %s" % (file))
    df = pd.read_csv(file)
    print("Compressing %s" % (file))
    df.to_pickle("%s.pkl.gz" % (file))