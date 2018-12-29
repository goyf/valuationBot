from datapackage import Package
from Tkinter import *
from math import *

from alpha_vantage.timeseries import TimeSeries

import matplotlib
import numpy as np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import matplotlib.pyplot
from matplotlib.ticker import MaxNLocator


import get_10_Q_K


packageNYSE = Package('https://datahub.io/core/nyse-other-listings/datapackage.json')
packageNASDAQ = Package('https://datahub.io/core/nasdaq-listings/datapackage.json')

class stockClass:
    def __init__(self,  window):
        self.window = window
        self.box = Entry()
        self.button = Button(self.window, text="Search", command=self.plotGraph)
        self.box.grid(row=0,column=1, sticky="NW")
        self.button.grid(row=0,column=2, sticky="NW")
        self.outx = np.array([0])
        
        self.comp_name = ""
        self.buttonEdgar = Button(self.window, text="get a report", command = lambda : get_10_Q_K.get_10_Q_K(self.comp_name))
        self.buttonEdgar.grid(row=4, column=4, sticky="NE")
        
        
        self.title = Label(self.window, text="Company ticker", relief=FLAT).grid(row=0,column=0, sticky="NW")
        
    def findComp(self, name):   
        for resource in packageNYSE.resources:
    #if resource.descriptor['datahub']['type'] == 'derived/csv':
            if resource.tabular:
                listNYSE = resource.read()

        for resource in packageNASDAQ.resources:
            #if resource.descriptor['datahub']['type'] == 'derived/csv':
            if resource.tabular:
                listNASDAQ = resource.read()


        found = False
        company = ""
        for companyNames in listNYSE:
            if companyNames[0] == name:
                found = True
                company = companyNames[0] + ", " + companyNames[1]

        if found == False:
            for companyNames in listNASDAQ:
                if companyNames[0] == name:
                    found = True
                    company = companyNames[0] + ", " + companyNames[1]
            if found == False:
                return 'Could not find the company'
            
        return company

    
    def plotGraph(self):
        
        self.comp_name = self.box.get().upper()
        
        info_label = self.findComp(self.comp_name)      
        
        ts = TimeSeries(key='Z4GYC8KFAQZCUZ51', output_format='pandas')
        data, meta_data = ts.get_weekly_adjusted(symbol=self.comp_name)
        price_values = np.array(data['4. close'])
        time_values = np.array(list(data.index))
        
        short_mva = (data['4. close']).rolling(window=20).mean()
        short_mva = np.array(short_mva)
        
        long_mva = (data['4. close']).rolling(window=50).mean()
        long_mva = np.array(long_mva)

        time_ratio = 2.1 #This magic number is for time range. I should use ['date'] instead
        fig = Figure(figsize=(10,6))
        main_window = fig.add_subplot(111)
        main_window.plot(time_values[int(len(time_values)/time_ratio):len(time_values)],price_values[int(len(price_values)/time_ratio):len(price_values)],color='red')
        main_window.plot(time_values[int(len(time_values)/time_ratio):len(time_values)],short_mva[int(len(short_mva)/time_ratio):len(short_mva)],color='blue')
        main_window.plot(time_values[int(len(time_values)/time_ratio):len(time_values)],long_mva[int(len(long_mva)/time_ratio):len(long_mva)], color = 'green')

        main_window.set_title (info_label, fontsize=16)
        main_window.set_ylabel("Price", fontsize=14)
        main_window.set_xlabel("Date", fontsize=14)
        main_window.xaxis.set_major_locator(MaxNLocator(6))

        canvas = FigureCanvasTkAgg(fig, master=self.window)
        canvas.get_tk_widget().grid(row=3,column=0, rowspan=4, columnspan=3)
        canvas.draw()        
        
        Label(self.window, text="Current Price:", relief=GROOVE).grid(row=3, column=3, sticky="NW")
        Label(self.window, text=str(price_values[len(price_values)-1]) + '$', relief=GROOVE).grid(row=3, column=4, sticky='NE')
