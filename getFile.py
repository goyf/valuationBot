#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 30 20:42:05 2017

@author: goyf
"""

import requests
from bs4 import BeautifulSoup
import urllib.request

url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=0000001800&type=&dateb=&owner=include&start=80&count=40'
r = requests.get(url)
html_content = r.text

soup = BeautifulSoup(html_content, 'lxml')

file = open("html.txt", 'w')
file.write(html_content)
file = open('html.txt', 'r')

lookup = '10-Q'

gotLine = False
for i, line in enumerate(file, 1):
    if gotLine == True:
        searchLine = line
        break #Superbad, this is here so that I get only one 10-Q
    if lookup in line:
        foundLine = i + 1
        gotLine = True
        

soup = BeautifulSoup(searchLine, 'lxml')
all_links = []
findA = soup.find_all('a')
for link in findA:
            if 'Documents' in link.text:
                all_links.append(link['href'])
                
url = 'https://www.sec.gov/'
url = url + all_links[0]
r = requests.get(url)
html_content = r.text

soup = BeautifulSoup(html_content, 'lxml')

file = open("html.txt", 'w')
file.write(html_content)
file = open('html.txt', 'r')

lookup = '<td scope="row">10-Q</td>'
gotLine = False
for i, line in enumerate(file, 1):
    if gotLine == True:
        searchLine = line
        break #Superbad, this is here so that I get only one 10-Q
    if lookup in line:
        foundLine = i + 1
        gotLine = True

soup = BeautifulSoup(searchLine, 'lxml')
all_links = []
findA = soup.find_all('a')
for link in findA:
    all_links.append(link['href'])
                
url = 'https://www.sec.gov/'
url = url + all_links[0]
urllib.request.urlretrieve(url, '10Q.htm')