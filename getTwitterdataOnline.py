from urllib import request as rq
import pandas as pd
import os
from datetime import datetime as dt
import calendar
from bs4 import BeautifulSoup # for web scraping
import requests # for url manipulation
from azure.storage.blob import BlobServiceClient, PublicAccess
from azure.core.exceptions import HttpResponseError, ResourceExistsError

connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name ='twitterstream'
container_client = blob_service_client.get_container_client(container_name)
year = {2020}

for y in year:
    if y == 2020:
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
                copied_blob = blob_service_client.get_blob_client(container_name, lnkurl)
                source_blob = baseurl + '/' + lnkurl
                response = requests.head(source_blob, allow_redirects=True)
                print(response.url)
                source_blob = response.url
                
                print('Downloading: ' + lnkurl)
                
                # download the file
                try:
                    copy = copied_blob.start_copy_from_url(source_blob)
                    props = copied_blob.get_blob_properties()
                    print(props.copy.status)
                except:
                    print('Error: ' + lnkurl)
                    continue
                print('Downloaded: ' + lnkurl)