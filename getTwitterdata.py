from urllib import request as rq
import pandas as pd
import os
from datetime import datetime as dt
import calendar
from bs4 import BeautifulSoup # for web scraping
import requests # for web scraping

year = {2022}

for y in year:
    if y == 2021:
        month = range(1, 13, 1)
    else:
        month = range(1, 12, 1)
       
    for m in month:
        str_Year = str(y)
        if m < 10:
            str_Month = '0' + str(m)
        else:
            str_Month = str(m)

        baseurl = "https://archive.org/download/archiveteam-twitter-stream-" + str_Year + '-' + str_Month

# https://archive.org/download/archiveteam-twitter-stream-2021-06/twitter-stream-2021-06-14.zip
        # resorted to web scraping because there are too many variables to statically code for. 
        r = requests.get(baseurl)
        soup = BeautifulSoup(r.content)
        soup = soup.find('table')
        soup = soup.find_all('a')
        for element in soup:
            dest = 'E:/TwitterStream'
            lnkurl = element.get('href')
            # only download the files that are zip or tar 
            if lnkurl.endswith('.zip') or lnkurl.endswith('.tar'):
                dest =  dest + '/' + lnkurl
                lnkurl = baseurl + '/' + lnkurl
                print('Downloading: ' + lnkurl)
                
                if os.path.exists(dest):
                    print('File exists: ' + dest)
                    continue
                else:
                # download the file
                    try:
                        rq.urlretrieve(lnkurl, dest)
                    except:
                        print('Error: ' + lnkurl)
                        continue
                print('Downloaded: ' + lnkurl)