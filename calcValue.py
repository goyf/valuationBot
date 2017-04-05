#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 09:35:26 2017

@author: goyf
"""

import pandas_datareader as pdr
from datetime import datetime
import time

year = int(time.strftime("%Y"))
month = int(time.strftime("%m"))
today = int(time.strftime("%d"))
yday = int(time.strftime("%d")) - 1
stockPrice = pdr.get_data_yahoo(symbols='ABT', start=datetime(year, month, yday), end=datetime(year, month, today))
#print(stockPrice['Adj Close'])

shares = 1000000
marketCap = shares * float(stockPrice['Adj Close'])
enterpriseValue = marketCap + cash - debt