# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 14:24:03 2020

@author: shamid
"""
import requests
import json
import time
import pandas as pd
from IPython.core.display import clear_output
import requests_cache

requests_cache.install_cache()

API_KEY = '51d67c344b63aee3f0972526d14cc951'
USER_AGENT = 'Dataquest'

responses = []

page = 1
total_pages = 10

def lastfm_get(payload):
    # define headers and URL
    headers = {'user-agent': USER_AGENT}
    url = 'http://ws.audioscrobbler.com/2.0/'

    # Add API key and format to the payload
    payload['api_key'] = API_KEY
    payload['format'] = 'json'

    response = requests.get(url, headers=headers, params=payload)
    return response

def jprint(obj):
    # create a formatted sting of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent = 4)
    print(text)

#r = lastfm_get({
#        'method':'chart.gettopartists'
#        })
 
    
print(r.status_code)
#jprint(r.json())
jprint(r.json()['artists']['@attr'])

while page <= total_pages:
    payload = {
            'method' : 'chart.gettopartists',
            'limit' : 500,
            'page' : page
            }
    print("Requesting page {}/{}".format(page, total_pages))
    clear_output(wait=True)
    
    response = lastfm_get(payload)
    
    if response.status_code != 200:
        print(response.text)
        break
    
    page = int(response.json()['artists']['@attr']['page']) 
    total_pages = 10 #int(response.json()['artists']['@attr']['totalPages'])
    responses.append(response)
    
    if not getattr(response, 'from_cache', False):
        time.sleep(0.25)
       
    page += 1
    