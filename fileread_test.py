#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 16:11:24 2018

@author: yjt_yujie
"""
import os
from pathlib import Path

print(__file__)
print(os.path.abspath(__file__))
p = Path("yjt_master.py")
p = p.resolve(strict=True)
print(p)
