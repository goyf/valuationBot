#Gets the most recent 10-Q file from SEC Edgar

import requests
from bs4 import BeautifulSoup
import urllib
import xlrd

def get_10_Q_K(ticker):
	results_per_page = 100
	current_page = 0
	gotLine = 0

	#Finds parses the website and finds the line with 10-Q
	#The url has a certain format, so I am taking advantage of that

	while(gotLine == 0):
	    url = 'https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK=' + ticker + '&type=&dateb=&owner=exclude&start=' \
	    + str(current_page*results_per_page) + '&count=' + str(results_per_page)
	    r = requests.get(url)    

	    html_content = r.text
	    soup = BeautifulSoup(html_content, 'lxml')

	    file = open("html.txt", 'w')
	    file.write(html_content)
	    file = open('html.txt', 'r')

	    lookup = '10-Q'
	    for i, line in enumerate(file, 1):
	        if gotLine == 1:
	            searchLine = line
	            gotLine += 1
	        if lookup in line:
	            foundLine = i + 1
	            gotLine += 1
	    
	    current_page +=1

    #Extracts a link for the 10-Q or K Interactive data

	soup = BeautifulSoup(searchLine, 'lxml')
	all_links = []

	testFind = soup.find('a', {'id' : 'interactiveDataBtn'})

	#Opens a 10-Q link and saves it

	url = 'https://www.sec.gov'
	url = url + testFind['href']
	r = requests.get(url)
	html_content = r.text

	soup = BeautifulSoup(html_content, 'lxml')

	file = open("html.txt", 'w')
	file.write(html_content)
	file = open('html.txt', 'r')

	#Finds the Excel file and downloads it

	soup = BeautifulSoup(html_content, 'lxml')
	all_links = []
	findA = soup.find_all('a')
	for link in findA:
	    if 'View Excel Document' in link.text:
	        all_links.append(link['href'])

	url = 'https://www.sec.gov'
	url = url + all_links[0]
	urllib.urlretrieve(url, '10Q'+ticker+'.xlsx')
