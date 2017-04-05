#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 10:24:15 2017

@author: goyf
"""
from datetime import datetime
import time
import pandas_datareader as pdr
import pandas as pd
import requests
from bs4 import BeautifulSoup
import urllib.request
import xlrd
import os
path = '/media/goyf/Data2/skola/Programovani/Python/valuationBot/New Folder/'

#Open up a file with links to companies
comps = pd.read_csv('/media/goyf/Data2/skola/Programovani/Python/valuationBot/compsShort.csv')
comps = comps.ix[:,1:4]
enterpriseValue = pd.DataFrame([], columns=['Ticker', 'EV', 'Leverage'])

for index, row in comps.iterrows():
    #Finding the 10-Q link
    
    
    url = comps.ix[index][2]
#    Check whether the current row isn't missing the URL
    if type(url) != type('string'):
        continue
    r = requests.get(url)
    html_content = r.text
    
    soup = BeautifulSoup(html_content, 'lxml')
    
    file = open("html.txt", 'w') #We need line numbers
    file.write(html_content)
    file = open('html.txt', 'r')
    
    lookup = '10-Q'
    
    gotLine = False
    for i, line in enumerate(file, 1):
        if gotLine == True:
            searchLine = line
            break
        if lookup in line:
            foundLine = i + 1
            gotLine = True
            
    if gotLine == False:
        continue
            
    r = requests.get(url)
    html_content = r.text
    
    soup = BeautifulSoup(html_content, 'lxml')
    all_links = []
    findA = soup.find_all('a')
    for link in findA:
                if 'Interactive Data' in link.text:
                    all_links.append(link['href'])
                    
    url = 'https://www.sec.gov'
    url = url + all_links[0]
    
    #Getting the Excel File
    
    r = requests.get(url)
    html_content = r.text
    
    soup = BeautifulSoup(html_content, 'lxml')
    all_links = []
    findA = soup.find_all('a')
    for link in findA:
        if 'View Excel Document' in link.text:
            all_links.append(link['href'])
    
    url = 'https://www.sec.gov'
    url = url + all_links[0]
    filename = os.path.join(path, 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
    urllib.request.urlretrieve(url, filename)
    
    book = xlrd.open_workbook(path + 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
    
    #Some filings are in Thousands and some in Millions
    multiplier = 0
    secondSheet = book.sheet_by_index(1)
    firstLine = str(secondSheet.cell(0,0))
    if '$ in Millions' in firstLine:
        multiplier = 1000000
    elif '$ in Thousands' in firstLine:
        multiplier = 1000
    
    
    x = 0
    z = 0
    foundRow = False
    row = 0
    bookLength = book.nsheets
    while z < 5:
        sheetCash = book.sheet_by_index(z)
        while x < sheetCash.nrows:
            if foundRow == True:
                break
            if sheetCash.cell(x,0).value == 'Cash and cash equivalents':
                row = x
                foundRow = True
            x = x+1
        
            
        if foundRow == True:
            break
        x = 0
        z = z + 1
    
    if foundRow == False:
        os.remove(path + 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
        continue
            
    cash = sheetCash.cell(row, 1).value
    
    x = 0
    z = 0
    foundRow = False
    row = 0
    bookLength = book.nsheets
    while z < 5:
        sheetIncome = book.sheet_by_index(z)
        while x < sheetIncome.nrows:
            if foundRow == True:
                break
            if sheetIncome.cell(x,0).value == 'Net income' :
                row = x
                foundRow = True
            if sheetIncome.cell(x,0).value == 'Net earnings (loss)':
                row = x
                foundRow = True
            if sheetIncome.cell(x,0).value == 'CONSOLIDATED NET INCOME':
                row = x
                foundRow = True        
            x = x+1
        
            
        if foundRow == True:
            break
        x = 0
        z = z + 1
    
    if foundRow == False:
        os.remove(path + 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
        continue
        
    y = 1
    foundCol = False
    while y < sheetIncome.ncols:
        if foundCol == True:
            break
        if sheetIncome.cell(row,y).value != '':
            col = y
            foundCol = True
        y = y + 1
    
    if foundCol == False:
        os.remove(path + 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
        continue    
    income = sheetIncome.cell(row,col).value
    
    x = 0
    z = 0
    foundRow = False
    row = 0
    while z < 5:
        sheetDebt = book.sheet_by_index(z)
        while x < sheetDebt.nrows:
            if foundRow == True:
                break
            if sheetDebt.cell(x,0).value == 'Long-term debt':
                row = x
                foundRow = True
            if sheetDebt.cell(x,0).value == 'LONG-TERM DEBT':
                row = x
                foundRow = True
            if sheetDebt.cell(x,0).value == 'Debt':
                row = x
                foundRow = True
            if sheetDebt.cell(x,0).value == 'Long-term debt, net':
                row = x
                foundRow = True
            x = x+1
            
        if foundRow == True:
            break
        x = 0
        z = z + 1
        
    if foundRow == False:
        os.remove(path + 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
        continue    
    debt = sheetDebt.cell(row,1).value
    
    x = 0
    foundRow = False
    row = 0
    sheetShares = book.sheet_by_index(0)
    while x < sheetShares.nrows:
        if foundRow == True:
            break
        if sheetShares.cell(x,0).value == 'Entity Common Stock, Shares Outstanding':
            row = x
            foundRow = True
        x = x+1
    
    if foundRow == False:
        os.remove(path + 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
        continue   
    
    y = 1
    foundCol = False
    while y < sheetShares.ncols:
        if foundCol == True:
            break
        if sheetShares.cell(row,y).value != '':
            col = y
            foundCol = True
        y = y + 1
    
    if foundCol == False:
        os.remove(path + 'FinReport' + str(comps.iloc[index][0]) + '.xlsx')
        continue
    shares = sheetShares.cell(row, col).value
    
    year = int(time.strftime("%Y"))
    month = int(time.strftime("%m"))
    today = int(time.strftime("%d"))
    yday = int(time.strftime("%d")) - 1
    stockPrice = pdr.get_data_yahoo(symbols=comps.iloc[index][0],
                                    start=datetime(year, month, yday),
                                                  end=datetime(year, month, today))
    
    #Calculation of debt-to-cash ratio and enterpriseValue
    marketCap = shares * float(stockPrice['Adj Close'])
    EV = marketCap + float(cash)*multiplier - float(debt)*multiplier
    leverage = debt/cash
    enterpriseValue = enterpriseValue.append({'Ticker':comps.iloc[index][0],
                                              'EV':EV, 'Leverage':leverage},ignore_index = True)
    print ('done')
    
enterpriseValue = enterpriseValue.sort_values(['Leverage'])