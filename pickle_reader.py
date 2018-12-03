#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 07:39:58 2018

@author: yjt_yujie
"""
import pandas as pd
from pathlib import Path

cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
datafolderpath = cwd.joinpath("data")
allfiles = list(datafolderpath.glob("**/*.pkl.gz"))
df_list = []

for file in allfiles:
    file = file.resolve(strict=True)
    print("Loading %s" % (file))
    df = pd.read_pickle(file)
    df_list.append(df)
    df_all = pd.concat(df_list)