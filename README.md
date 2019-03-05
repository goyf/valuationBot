# ValuationBOT project

* Python 2.7
* doomberg_terminal.py is the main file to run
* terminal.py and get_10_Q_K.py files are required

## Version 1.0

### Simple feature list
* Pull SEC links of companies from a list
* Download the latest 10-Q filing using handmade script in an Excel format
* Search for stocks graph using Alpha Vantage

### Library list
* Requests
* Beautiful Soup
* urllib
* xlrd
* datapackage
* Tkinter
* alpha_vantage
* matplotlib
* numpy (formerly used pandas as well)

### Things to do
* Fix the numpy magic number (see terminal.py)
* Add Legend for the plots
* Create a strategy based on moon cycles
* Research and add an oscillator, e.g. Klinger oscillator
  * Some stocks stagnate in the long-term and fluctuate in the short term and this needs to be addressed
* Add the feature decide whether to download a 10-Q or a 10-K

### Brief history
This bot started purely as a bot where it would extract info from 10-Q files but since there is no unified way of expressing profits, revenues, etc., I would just end up in with a long list of phrases that mean the same thing. Moreover, this is generally useless because the fillings need to be studied in detail [Graham, Buffet, Shkreli] and this project is meant to be only an adhoc tool.

I used to use pandas but since numpy does the job, there's no need for them anymore.

Suggestions welcome

There is no licence yet

Also, if you ever use this, you are responsible for your money and well-being, not me.
