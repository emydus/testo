#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 06:50:34 2018

@author: yjt_yujie
"""
import pandas as pd
from pathlib import Path

cwd = Path.cwd()
cwd = cwd.resolve(strict=True)
datafolderpath = cwd.joinpath("data")
allfiles = list(datafolderpath.glob("**/*.csv"))

for file in allfiles:
    df = pd.read_csv(file)
    df.to_pickle("%s.pkl.gz" % (file))