#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr  4 13:52:58 2017

@author: goyf
"""

import xlrd
path = '/media/goyf/Data2/skola/Programovani/Python/valuationBot/'

book = xlrd.open_workbook(path + 'Financial_ReportAdobe.xlsx')

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
while z < bookLength:
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
        
cash = sheetCash.cell(row, 1).value
print (cash)

x = 0
z = 0
foundRow = False
row = 0
bookLength = book.nsheets
while z < bookLength:
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
    
y = 1
foundCol = False
while y < sheetIncome.ncols:
    if foundCol == True:
        break
    if sheetIncome.cell(row,y).value != '':
        col = y
        foundCol = True
    y = y + 1
    
income = sheetIncome.cell(row,col).value
print (income)

x = 0
z = 0
foundRow = False
row = 0
while z < bookLength:
    sheetDebt = book.sheet_by_index(z)
    while x < sheetDebt.nrows:
        if foundRow == True:
            break
        if sheetDebt.cell(x,0).value == 'Long-term debt' :
            row = x
            foundRow = True
        if sheetDebt.cell(x,0).value == 'LONG-TERM DEBT':
            row = x
            foundRow = True
        if sheetDebt.cell(x,0).value == 'Debt':
            row = x
            foundRow = True        
        x = x+1
        
    if foundRow == True:
        break
    x = 0
    z = z + 1
    
debt = sheetDebt.cell(row,1).value
print (debt)

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

y = 1
foundCol = False
while y < sheetShares.ncols:
    if foundCol == True:
        break
    if sheetShares.cell(row,y).value != '':
        col = y
        foundCol = True
    y = y + 1

shares = sheetShares.cell(row, col).value
print (shares)