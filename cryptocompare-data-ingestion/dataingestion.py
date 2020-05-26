# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 13:37:39 2020

@author: shamid

This scrip retrieves data from 
https://min-api.cryptocompare.com/data/histo/minute/daily 
It generates a log file named "output_log.txt" 
All the exchange data is stores in the folder "MinutePairs"
The data is stored in the form of a CSV file where the first name of the file
is the "From crypto" name and the last name of the file is the "To crypto"
name, i.e. "FromCrtpyo_ToCrypto.csv"


"""

import requests
import pandas as pd
import numpy as np 
from itertools import combinations
from datetime import datetime
from datetime import timedelta
import time
import csv
import sys
import traceback

# a file to write the output logs
f = open('output_log.txt', 'w')

# the API key
apiKey = "0f8ad005e8b9a37df28be1500f445dad477f38e8b558bae04d0e04b89ca2e2cc"

# endpoint url to retrieve the data from
url = "https://min-api.cryptocompare.com/data/histo/minute/daily"

# header for the get request
# Header, it contains the API key  
headers = {
    "authorization": "Apikey " + apiKey
}

# payload for the get request initialized with random variables
payload = { 
        "e" : "CCCAGG",
        "fsym" : "ETH",
        "tsym" : "USD",
        "date" : "2019-07-21"
        }

# the start date from when the data is to be gathered %Y-%m-%d
start_date = "2020-01-01" 
# the end date till when the data is to be gathered %Y-%m-%d
stop_date = "2020-03-31"

# creating a pandas datafram from a  file where the name of all the exchnages
# (except CCCAGG) are stored. The datafarme has columns "Exchnage", "From",
# "To", "Start_Date", "End_Date"
exchanges_df = pd.read_csv("exchange_all.csv")

# changing the "Start_Date" and "End_Date" column from a string to a datetime
# object
exchanges_df['Start_Date'] = pd.to_datetime(exchanges_df["Start_Date"],
                                            format='%Y-%m-%d', errors='raise',
                                            infer_datetime_format=False,
                                            exact=True)

exchanges_df['End_Date'] = pd.to_datetime(exchanges_df["End_Date"],
                                            format='%Y-%m-%d', errors='raise',
                                            infer_datetime_format=False,
                                            exact=True)


# Create a new dataframe that only Exchanges that have data available between 
# 1st January 2020 to 31st March 2020
#temp_exchnages_df = exchanges_df.query("Start_Date >= '2020-01-01'")
#new_exchnages_df = temp_exchnages_df.query("End_Date > '2020-03-31'")


# Names of pure and stable coin crypto-currency 
pure_stable_crypto_names =[
        'ABBC', 'ADA', 'ALGO', 'AOA', 'ATOM', 'BCD', 'BCH', 'BCN', 'BGBP',
        'BITUSD', 'BSV', 'BTC', 'BTG', 'BTS', 'BUSD', 'DAI', 'DASH', 'DENT', 
        'DCR', 'DGB', 'DOGE', 'DRG', 'ETC', 'ETH', 'EURS', 'GUSD', 'HC', 'HOT',
        'IOST', 'LSK', 'LTC', 'MIOTA', 'MKR', 'NANO', 'NEO', 'NPXS', 'OMG',
        'PAX', 'QTUM', 'QNT', 'RSV', 'RVN', 'STEEM', 'THETA','TRX', 'TUSD', 
        'USD', 'USDC', 'USDT', 'VET', 'XEM', 'XLM', 'XMR', 'XRP', 'XTZ','XVG',
        'ZEC'
        ]
# generate pairs of crypto currencies
comb_pure_stable_crypto = combinations(pure_stable_crypto_names, 2)

# an array to store the pairs
pure_stable_crypto_pairs = []

# append the pairs to "pure_stable_crypto_pairs" array
for i in list(comb_pure_stable_crypto):
    pure_stable_crypto_pairs.append([i[0], i[1]])

# convert "pure_stable_crypto_pairs" to a numpy array    
pure_stable_crypto_pairs = np.asarray(pure_stable_crypto_pairs)


def write_to_file(result, fcryp, tcryp):
    """This function writes the data retrieved from the API to a ".csv" file
    The name of the file starts with the "From Crypto" currency and ends with
    the "To Crypto" currency i.e. "FromCrtpyo_ToCrypto.csv"
    """
    
    # Create a file in "MinutePairs" to store the retrieved data
    csvFile = open('./MinutePairs/' + fcryp + '_' + tcryp + '.csv', 'a+',
                   newline='')
    writer = csv.writer(csvFile, delimiter = ",")
    
    # write to the file one line at a time from the result ontained
    for line in result.text.strip('\"').split("\n"):        
        if (line.startswith("time") == False and line != ""):
            writer.writerow(line.split(","))
            

def getCCCAGG(fcryp, tcryp, date):
    """This function calls the url to check if the data for the "From Crypto"
    and "To Crypto" pair exists for the CCCAGG exchange.
    """
    from_crypto = fcryp
    to_crypto = tcryp
    
    # update the payload variables 
    payload["e"] = "CCCAGG"
    payload["fsym"] = from_crypto
    payload["tsym"] = to_crypto
    payload["date"] = date

    # send the get request to the url
    result = requests.get(url, headers=headers, params=payload)
    
    # if there is an Error message in the response the return 0    
    if (result.text.startswith("{\"Response\":\"Error\"")) == True:
        return 0
    
    # if the response id successfull then write the data to the file
    else:
        write_to_file(result, from_crypto, to_crypto)
        print("Exchange: CCCAGG")
        f.write("Exchnage: CCCAGG\n")
        return 1
        
def get_otherexchnages(fcryp, tcryp, date):
    """This function calls the url to check if the data for the "From Crypto"
    and "To Crypto" pair exists for any exchange the is listed in 
    "new_exchnages_df" dataframe for the given date. 
    """
    pair_found_flag = 0
    
    # for each row in the "new_exchnages_df" check if the pair exists for any
    # exchange for the given date. 
    for index, row in exchanges_df.iterrows():
        
        # check if the pair exists in the "new_exchnages_df" for the given date
        if(row["From"] == fcryp and row["To"] == tcryp) and (row["Start_Date"]
        <= datetime.strptime(date, "%Y-%m-%d") and row["End_Date"]
        >= datetime.strptime(date, "%Y-%m-%d")):
            
            from_crypto = fcryp
            to_crypto = tcryp
            

            
            # set the payload variables
            payload["e"] = row["Exchange"]
            payload["fsym"] = from_crypto
            payload["tsym"] = to_crypto
            payload["date"] = date
            
            pair_found_flag = 1
            print("Exchnage: {}".format(row["Exchange"]))
            f.write("Exchnage: {}\n".format(row["Exchange"]))
            break
        
        # if it does not exist then swap the pairs and check again
        elif(row["From"] == tcryp and row["To"] == fcryp) \
        and (row["Start_Date"] <= datetime.strptime(date, "%Y-%m-%d")
        and row["End_Date"] >= datetime.strptime(date, "%Y-%m-%d")):
            
            from_crypto = tcryp
            to_crypto = fcryp
            
#            print("The values were Swapped!")
#            print("Exchange \t From \t To \n {} \t {} \t {}".format(row["Exchange"], row["From"], row["To"]))
            
            # set the payload variables
            payload["e"] = row["Exchange"]
            payload["fsym"] = from_crypto
            payload["tsym"] = to_crypto
            payload["date"] = date
            
            pair_found_flag = 1
            print("Exchange: {}".format(row["Exchange"]))
            f.write("Exchnage: {}\n".format(row["Exchange"]))
            break
    
    # if the pair is found in "new_exchanges_df" then send the request to the
    # API
    if(pair_found_flag == 1):
        result = requests.get(url, headers=headers, params=payload)
        
        # Check if there is an error message in the response
        if (result.text.startswith("{\"Response\":\"Error\"")) == True:
            print("Error in response!")
            f.write("Error in response!\n")
            return 0
        
        # If there is no erro message in the response then write to a .csv file        
        else:
            print("No error in response!")
            f.write("No error in response!\n")
            write_to_file(result, from_crypto, to_crypto)
            return 1
                       
    return 0


# for every pair in the crypto-currency list 
for pair in pure_stable_crypto_pairs:
    
    # try-except block to catch any unexpected error           
    try:
        
        print("Pairs are {} and {}".format(pair[0], pair[1]))
        f.write("Pairs are {} and {}\n".format(pair[0], pair[1]))
    
        # start date in the correct format
        start = datetime.strptime(start_date, "%Y-%m-%d")
        # stop date in the correct format
        stop = datetime.strptime(stop_date, "%Y-%m-%d")
    
        print("Start date:{} \nStop date:{}".format(start, stop))
        f.write("Start date:{} \nStop date:{}\n".format(start, stop))
        
        # while start date is less than equal to stop date
        while start <= stop:
            
            data_retrieved_flag = 0
        
            date = datetime.strftime(start, "%Y-%m-%d")
            print("Date is : {}".format(date))
            f.write("Date is : {}\n".format(date))
            
            #check is the data is avaiable in CCCAGG exchnge
            data_retrieved = getCCCAGG(pair[0], pair[1], date)
            
            # if the data is successfully received increase the date and stop
            # the current execution of the loop
            if(data_retrieved == 1):
                
                data_retrieved_flag = 1
                print("Data retieved!")
                f.write("Data retieved!\n")
                start = start + timedelta(days=1)
                continue
        
            # if the data is not retrieved thebn then swap the pairs and check 
            # if the data is present in CCCAGG
            data_retrieved = getCCCAGG(pair[1], pair[0], date)
            
            # if the data is successfully received increase the date and stop
            # the current execution of the loop
            if(data_retrieved == 1):
                data_retrieved_flag = 1
                print("Data retieved!")
                f.write("Data retieved!\n")
                start = start + timedelta(days=1)
                continue
            
            # check of the pair is available in any other exchange
            data_retrieved = get_otherexchnages(pair[0], pair[1], date)
            
            # if the data is successfully received increase the date and stop
            # the current execution of the loop
            if(data_retrieved == 1):
                data_retrieved_flag = 1
                print("Data retieved!")
                f.write("Data retieved!\n")
                start = start + timedelta(days=1)
                continue
        
            # if the data is not available in any of the exchange then increase
            # the date
            if(data_retrieved_flag == 0):
                print("Data not retrieved!")
                f.write("Data not retrieved!\n")
                start = start + timedelta(days=1)
        
            # stop execution for sometime
            time.sleep(1)
            
    #catch any exception if raised
    except KeyboardInterrupt:
        sys.exit(1)
    
    # handling any unexpected Exceptions    
    except Exception as e:
        e = sys.exc_info()
        print('Error Return Type: ', type(e))
        print('Error Class: ', e[0])
        print('Error Message: ', e[1])
        print('Error Traceback: ', traceback.format_tb(e[2]))
        f.write('Error Return Type:{}\n'.format(type(e)))
        f.write('Error Class::{}\n'.format(e[0]))
        f.write('Error Message::{}\n'.format(e[0]))
        f.write('Error Traceback::{}\n'.format(traceback.format_tb(e[2])))
        
# close the log file        
f.close()