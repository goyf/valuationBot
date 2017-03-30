#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 16:42:46 2017

@author: goyf
"""

import numpy as np
import pandas as pd

comps = pd.read_csv('/media/goyf/Data2/skola/Programovani/Python/valuationBot/comps2.csv')
comps = comps.ix[:,1:4]