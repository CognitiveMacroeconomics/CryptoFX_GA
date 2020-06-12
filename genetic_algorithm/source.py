# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:14:33 2020

@author: shamid
"""

import os
#import re
import numpy as np
import pandas as pd
#import xlsxwriter

# Global variables
num_mins = 1

# Name of the directory where the files are stored
directory_name = "\pure_crypto"

intermediate_currency = "BTC"


def read_data(start_exchange_currency, end_exchange_currency):
    """
    this function reads the files and stores the exchange rate in a 3-D
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
    
    print("In read data")
    
    # Get the name of all the files in the directory
    data_files =  os.scandir(".\data"+directory_name)
    
    # A list that stores the name of data files
    data_files_list = []
    
    # A dictonary to store the index values of the crypto-currencies
    crypto_dict = {}
    
    # The starting crypo-currency is indexed as 0
    crypto_dict[start_exchange_currency] = 0
    
    index = 1
    
    for file in [entry for entry in data_files if entry.name != ".gitkeep"]:
                
        # Append the name of all the file in "data_files_list"
        data_files_list.append(file.name)
       
        #print(file.name.replace(".csv","_").split("_"))
        
        # Stores the crypto names in two variables        
        crypto_1, crypto_2, _ = file.name.replace(".csv","_").split("_")
        #print("{}\t{}".format(crypto_1,crypto_2))

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
            
    
    #print(data_files_list)
    
    # The ending crypto-currency is indexed as the last one
    crypto_dict[end_exchange_currency] = len(crypto_dict)

    # The exchange-rate matrix is the an nXn matrix
    # where n = number of crypto-currency
    num_rows = num_columns = len(crypto_dict) 
    
    # initialize them temp_matrix to 0    
    temp_matrix = np.zeros((num_mins, num_rows, num_columns))
        
    # Get the exchange rates of the crypto-currencies and store them in the 
    # 3-D matrix
    count = 0
    for file in [entry for entry in data_files_list if entry != ".gitkeep"]:
         #print(file)   
        # Read the csv file and store it in the data frame "data_df"
        data_df = pd.read_csv(".\data"+directory_name+"\\"+file, 
                              usecols = [0,1])

        
        #print("File name is: {}".format(file))

#        # Get the exchange rates by minutes.
#        start_index = data_df.shape[0]
#        end_index = data_df.shape[0] - num_mins + 1
#        
#        print("End index is:{}".format(end_index))
#        
#
#        index_range = -np.sort(-(np.arange(end_index-1, start_index)))
        
        start_index = 0
        end_index = num_mins
        index_range = np.arange(start_index, end_index)
        #index_range = -np.sort(-(np.arange(start_index, end_index)))        

        """ Get the names of the crypto-currencies
         "crypto_1" stores "from" currency which will be the row value of the
         matrix. "crypto_2" stores the "to" currency which will be the column 
         value of the matrix.
        """
        crypto_1, crypto_2, _ = file.replace(".csv","_").split("_")
      
        row_num = crypto_dict[crypto_1]
        column_num = crypto_dict[crypto_2]
        
         
        # The depth of the matrix depends on the number of minutes we want to
        # extract the exchange rates for
       
        time = 0
        for i in index_range:
            temp_matrix[time][row_num][column_num] = data_df.loc[i][1]
            
            if(data_df.loc[i][1] != 0):
                temp_matrix[time][column_num][row_num] = 1 / data_df.loc[i][1]
            else:
                temp_matrix[time][column_num][row_num] = data_df.loc[i][1] # 0
            time += 1
        
#        count += 1
#        if count == 1:
#            break
            
    
    for time in range(num_mins):
        for j in range(0, num_rows):
            temp_matrix[time][j][j] = 1
            
    intrd_currency_index = crypto_dict[intermediate_currency]
    print("Intermediate currency is: {} at index {}".format(intermediate_currency, intrd_currency_index))     
    
    for time in range(num_mins):
        for j in range(0, num_rows):
            for k in range(0, num_columns):
                if j!=intrd_currency_index:
                    if k!=intrd_currency_index:
                        if(temp_matrix[time][j][k] == 0):
                            #temp_matrix[time][j][k] = -1
                            temp_matrix[time][j][k] = temp_matrix[time][j][intrd_currency_index] * temp_matrix[time][intrd_currency_index][k]
                
    # reverse the dictionary            
    crypto_index = {value : key for (key, value) in crypto_dict.items()}
                   

    #Return the currency index list and the exchange rate 3-D matrix  
    return crypto_index, temp_matrix

def main(start_exchange_currency, end_exchange_currency):
    """
    A function that calls the read_data function.
    """
    crypto_index, exchange_rate_matrix = read_data(start_exchange_currency, 
                                                   end_exchange_currency)
    return exchange_rate_matrix, crypto_index

#if __name__ == "__main__":
#    
#    start_exchange_currency =  "ADA"
#    end_exchange_currency = "ZEC"
#    
##    exchange_rate_matrix, crypto_index = read_data(start_exchange_currency, 
##                                              end_exchange_currency)
#    crypto_index, exchange_rate_matrix = read_data(start_exchange_currency, end_exchange_currency)
#    
#    writer = pd.ExcelWriter('pure_crypto_exchnages_temp.xlsx', engine='xlsxwriter')
#    
#    for i in range(exchange_rate_matrix.shape[0]):
#        df = pd.DataFrame(exchange_rate_matrix[i])
#        df.to_excel(writer, sheet_name= 'Time_'+str(i))
#     
#    writer.save()
    