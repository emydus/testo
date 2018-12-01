#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec  1 16:11:24 2018

@author: yjt_yujie
"""
import os
from pathlib import Path

# Should print a relative path to file
print(__file__)

# Should ALSO print a relative path to file
p = Path(__file__)
p = p.resolve(strict=True)
print(p)

# Should give the current working directory
cwd = os.path.dirname(__file__)

# Should ALSO give the current working directory
q = Path.cwd()
print(q)
q = q.resolve(strict=True)
print(q)

#print(sorted(Path(".").glob("*.py")))
#print(os.path.basename(__file__))