# -*- coding: utf-8 -*-
"""
Created on Tue Mar  3 08:55:42 2020

@author: shamid
"""

import requests
import json

API_KEY = '51d67c344b63aee3f0972526d14cc951'
USER_AGENT = 'Dataquest'

response = requests.get("http://api.open-notify.org/astros.json")
print(response.status_code)
print(response.json())

def jprint(obj):
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

jprint(response.json())

parameters = {
    "lat": 40.71,
    "lon": -74
}

response = requests.get("http://api.open-notify.org/iss-pass.json", params=parameters)

jprint(response.json())
