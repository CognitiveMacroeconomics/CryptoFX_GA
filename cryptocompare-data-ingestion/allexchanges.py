# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 16:22:38 2020

@author: shamid

This code gets data on all the exchnages that CryptoCompare has integrated
with. The results are saved in a CSV file named "exchnages_all.csv" the columns
are:
Exchange : name of the exchange
"""

import requests
import json
import pandas as pd
import numpy as np

def jprint(obj):
    """
        This function converts the data retrieved by the url in a json format
        and write it to a .txt file
    """
    
    # create a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent = 4)
    
    # create a file and write to it
    exchanges_file = open("exchanges.txt", "w+")
    exchanges_file.write(text)
    
    # close the file after writing
    exchanges_file.close()
    
# API Key
apiKey = "0f8ad005e8b9a37df28be1500f445dad477f38e8b558bae04d0e04b89ca2e2cc"

# URL to get all the exchanges
url = "https://min-api.cryptocompare.com/data/v4/all/exchanges"

# Header, it contains the API key
headers = {
    "authorization": "Apikey " + apiKey
}

# send a get request to the url
result = requests.get(url, headers=headers)

# call the function jprint() 
jprint(result.json())

# convert the data received in a json format
text = result.json()

# a numpy array to store exchange data
# it stores the Exchange, From currency, To currency, Start Date, End Date 
data = []

# In the first column of data[] store all the exchanges retrieved by the API
for i in text["Data"]["exchanges"].keys():
    exchange = str(i)
    data.append(exchange)

# convert data into a numpy array    
data = np.array(data)

# a row of ones
row_ones = np.ones((1, len(data)))

# vertically stack 4 more rows to data[]
data = np.vstack((data, row_ones))
data = np.vstack((data, row_ones))
data = np.vstack((data, row_ones))
data = np.vstack((data, row_ones))

# transpose the 2-D matrix
data_matrix = data.transpose()

j = 0

# add Excahnge, From Crypto, To Crypto, Start Date, End Date data to 
# data_matrix 
while j < len(data_matrix):
    
    index = j+1
    ex = data_matrix[j][0]
    
    # if exchnage pairs dont exist
    if len(text['Data']['exchanges'][ex]["pairs"].keys()) == 0:
        print(text['Data']['exchanges'][ex])
        
    # if exchange pairs exist
    else : 
        data_matrix[j][1] = 3 
        data_matrix[j][2] = 3

    # print the exchange
    print(ex)
    
    # a list that contains all the "From currency" for every exchange     
    f_syms = list(text['Data']['exchanges'][ex]["pairs"].keys())
    
    # for every "From currency" get the "To currency"    
    for fs in f_syms:
        
        # for every "To Currency", if it exists then add it to data_matrix
        for lts in list(text["Data"]["exchanges"][ex]["pairs"][fs]["tsyms"] \
                        .keys()):
            
            # store all the required data if it exists
            if  len(list(text["Data"]["exchanges"][ex]["pairs"][fs]["tsyms"] \
                    [lts].keys())) != 0:
                
                start_date = text["Data"]["exchanges"][ex]["pairs"][fs] \
                                ["tsyms"][lts]["histo_minute_start"]
                end_date = text["Data"]["exchanges"][ex]["pairs"][fs] \
                                ["tsyms"][lts]["histo_minute_end"]  
                data_matrix = np.insert(data_matrix, index, 
                                        [ex, fs, lts, start_date, end_date], 
                                        axis = 0)
                index += 1
                j += 1
    j += 1
    
#data_matrix_temp = data_matrix

# delete the rows that have dummy value
index = 0
for item in data_matrix:
    
    if (item[1] == str(3) and item[2] == str(3)):
        data_matrix = np.delete(data_matrix, index, axis = 0)
        #print(item)
    elif (item[1] == str(1.0) and item[2] == str(1.0)):
        data_matrix = np.delete(data_matrix, index, axis = 0)
        #print(item)
    else:
        index += 1

# convert data_matrix into a pandas dataframe
excall_df = pd.DataFrame(data_matrix , columns=["Exchange", "From", "To", 
                                                "Start_Date","End_Date"])
# write the data frame to a numpy file
excall_df.to_csv (r'exchange_all.csv', index = False, header=True)