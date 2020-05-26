# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:14:33 2020

@author: shamid
"""

import os
#import re
import numpy as np
import pandas as pd

# Global variables
num_mins = 3

# Name of the directory where the files are stored
directory_name = "\stable_crypto_minutes_1440"


def read_data(start_exchange_currency, end_exchange_currency):
    """
    A function that reads the files and stores the exchange rate in a 3-D
    matrix. The first dimensionality of the matrix stores the time by minute. 
    The second and third dimensionality of the matrix stores the exchange rates
    The second dimensionality is the "from" cryptocurrency. The third 
    dimensionality is the "to" currency.
    
    It takes in as parametes:
        - start_exchange_currency : The value of the starting currency
        - end_exchange_currency : The value of the ending currency
    
    E.g. If we want to extract exchange rates for 10 minutes then the shape of
    the matrix will be [time] X [number of crypto] X [number of crypto]
    """
    
    # Get the name of all the files in the directory
    data_files =  os.scandir(".\data"+directory_name)
    
    # A list that stores the name of data files
    data_files_list = []
    
    # A dictonary to store the index values of the crypto-currencies
    crypto_dict = {}
    
    # The starting crypo-currency is indexed as 0
    crypto_dict[start_exchange_currency] = 0
    
    index = 1
    
    for entry in data_files:
        
        # Append the name of all the file in "data_files_list"
        data_files_list.append(entry.name)
        
        # Stores the crypto names in two variables        
        crypto_1, crypto_2, _ = entry.name.replace(".csv","_").split("_")

        # Populate the "crypto_dict" to store the index of the 
        # crypto-currencies
        if (crypto_1 not in crypto_dict and crypto_1 != start_exchange_currency
            and crypto_1 != end_exchange_currency):
            
            crypto_dict[crypto_1] = index
            index += 1
            
        if (crypto_2 not in crypto_dict and crypto_2 != start_exchange_currency
            and crypto_2 != end_exchange_currency):
            
            crypto_dict[crypto_2] = index
            index += 1
    
    # The ending crypto-currency is indexed as the last one
    crypto_dict[end_exchange_currency] = len(crypto_dict)
    
    #print("crypto_dict:\n{}".format(crypto_dict))
    #print("Length is:{}".format(len(crypto_dict)))

    # The exchange-rate matrix is the an nXn matrix
    # where n = number of crypto-currency
    num_rows = num_columns = len(crypto_dict) 
    
    # initialize them temp_matrix to 0    
    temp_matrix = np.zeros((num_mins, num_rows, num_columns))

    print("Shape of x is:{}".format(temp_matrix.shape))
    
    # Get the exchange rates of the crypto-currencies and store them in the 
    # 3-D matrix
    for entry in data_files_list:
        
        # Read the csv file and store it in the data frame "data_df"
        data_df = pd.read_csv(".\data"+directory_name+"\\"+entry, 
                              usecols = [1,2])
        
        #print("File name is: {}".format(entry))
        #print("The sahpe of the data frame is: {}".format(data_df.shape))
        
        # Get the exchange rates by minutes.
        start_index = data_df.shape[0]
        end_index = data_df.shape[0] - num_mins + 1
        index_range = -np.sort(-(np.arange(end_index-1, start_index)))
        #index_range = -np.sort(-index_range)

        """ Get the names of the crypto-currencies
         "crypto_1" stores "from" currency which will be the row value of the
         matrix. "crypto_2" stores the "to" currency which will be the column 
         value of the matrix.
        """
        crypto_1, crypto_2, _ = entry.replace(".csv","_").split("_")
        row_num = crypto_dict[crypto_1]
        column_num = crypto_dict[crypto_2]

        # The depth of the matrix depends on the number of minutes we want to
        # extract the exchange rates for
        
        #print("Index range is: \n{}".format(index_range))
        
        time = 0
        for i in index_range:
            temp_matrix[time][row_num][column_num] = data_df.loc[i][1]
            time += 1
    
    
    for time in range(num_mins):
        for j in range(0, num_rows):
            temp_matrix[time][j][j] = 1
            

    # Return the currency index list and the exchange rate 3-D matrix
    return crypto_dict, temp_matrix


def main(start_exchange_currency, end_exchange_currency):
    """
    A function that calls the read_data function.
    """
    crypto_index, exchange_rate_matrix = read_data(start_exchange_currency, 
                                                   end_exchange_currency)
    return exchange_rate_matrix, crypto_index

if __name__ == "__main__":
    
    start_exchange_currency = "USDT" #"ADA"
    end_exchange_currency = "ATOM" #"ZEC"
    
    exchange_rate_matrix, crypto_index = read_data(start_exchange_currency, 
                                              end_exchange_currency)
    
     
    
    