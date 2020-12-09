# -*- coding: utf-8 -*-
"""
Created on Tue Feb 18 10:14:33 2020

@author: shamid
"""

import os
import numpy as np
import pandas as pd
from datetime import datetime


def read_data(directory_name, intermediate_currency, minute, chunk_size, transaction_cost):
    """
    This function reads the files and stores the exchange rate in a 2-D
    matrix. The first dimensionality is the "from" cryptocurrency. The second 
    dimensionality is the "to" currency.
    
    Parameters: 
        - directory_names : the name of the directory where all the exchange
            rate files are stored
        - intermediate_currency : The intermediate currency used to fill the
            cells of the matrix that dont have any data
        - minute : The minute for which the exchange rates are needed for
        - transaction_cost: The transaction cost incurred for each exchange
        
    It returns the exchnage rate matrix and the index of the crypto currencies
    in the matrix.
    """
    
    print("Reading data")
    
    # Get the name of all the files in the directory
    data_files =  os.scandir(".\data"+directory_name)
    
    # A list that stores the name of data files
    data_files_list = []
    
    # A dictonary to store the index values of the crypto-currencies
    crypto_dict = {}
       
    idx = 0
    
    for file in [entry for entry in data_files if entry.name != ".gitkeep"]:
                
        # Append the name of all the file in "data_files_list"
        data_files_list.append(file.name)
               
        # Store the crypto names in two variables        
        crypto_1, crypto_2, _ = file.name.replace(".csv","_").split("_")

        # Populate the "crypto_dict" to store the index of the 
        # crypto-currencies
        if (crypto_1 not in crypto_dict):
            
            crypto_dict[crypto_1] = idx
            idx += 1
            
        if (crypto_2 not in crypto_dict):
            
            crypto_dict[crypto_2] = idx
            idx += 1
               
    # The exchange-rate matrix is the an nXn matrix
    # where n = number of crypto-currency
    num_rows = num_columns = len(crypto_dict) 
    
        
    # Initialize the temp_matrix to 0    
    temp_matrix = np.zeros((chunk_size, num_rows, num_columns))


            
    # Get the exchange rates of the crypto-currencies and store them in the 
    # a matrix

    for file in [entry for entry in data_files_list if entry != ".gitkeep"]:
        
        # Read the csv file and store it in the data frame "data_df"
        # column 0 stores "time" and column 1 store "open"
        data_df = pd.read_csv(".\data"+directory_name+"\\"+file, 
                              usecols = [0,1])
        time = 0
        index = minute - 1
        while time < chunk_size:
            
            """ Get the names of the crypto-currencies
            "crypto_1" stores "from" currency which will be the row value of the
            matrix. "crypto_2" stores the "to" currency which will be the column 
            value of the matrix.
            """
            crypto_1, crypto_2, _ = file.replace(".csv","_").split("_")
      
            row_num = crypto_dict[crypto_1]
            column_num = crypto_dict[crypto_2]
        
            # Fill the cell of the matrix with exchange data and apply the
            # transaction cost
            value = data_df.loc[index][1]
            temp_matrix[time][row_num][column_num] = (value - (value * transaction_cost))
        
#           value = data_df.loc[index][1]
#           temp_matrix[row_num][column_num] = value
        
            # Interchange the column_num and row_um of the matrix and fill the cell
            # with the reciprocal of the exchnage rate after applying trasaction 
            # cost
            if(data_df.loc[index][1] != 0):
                value = 1 / data_df.loc[index][1]
                temp_matrix[time][column_num][row_num] = (value - (value * transaction_cost))
#               temp_matrix[column_num][row_num] = value
            # If the exchnage rate if 0 then the cell with the inverted row_num and
            # column_num will also have the exchange rate as 0
            else:
                temp_matrix[time][column_num][row_num] = data_df.loc[index][1] # 0
                
            time += 1
            index += 1
        
    # The exchange rate between the same crypto currency will be 1
    for t in range(0, chunk_size):    
        for j in range(0, num_rows):
            temp_matrix[t][j][j] = 1
    
    ###########################################################################
    # COMMENT OUT THIS PIECE OF CODE IF THERE IS NO INTERMEDIATE CURRENCY
    ###########################################################################
    # An intermediate currency is applied for exchnage paris which do not have
    # direct exchange rate data       
    intrd_currency_index = crypto_dict[intermediate_currency]
    print("Intermediate currency is: {} at index {}".format(\
                                                      intermediate_currency,
                                                      intrd_currency_index))     
    for t in range(0, chunk_size):
        for j in range(0, num_rows):
            for k in range(0, num_columns):
                if j!=intrd_currency_index:
                    if k!=intrd_currency_index:
                        if(temp_matrix[t][j][k] == 0):
                        
                            temp_matrix[t][j][k] = -1
                        
                            #value1 = temp_matrix[t][j][intrd_currency_index]
                            # Applying the transaction cost
                            #value2 = (value1 - (value1 * transaction_cost))
                        
                            #value3 = temp_matrix[t][intrd_currency_index][k]
                        
                            # Applying the transaction cost
                            #value4 = (value3 - (value3 * transaction_cost))
                        
                            #temp_matrix[t][j][k] = value2 * value4
    ###########################################################################
            
    # reverse the dictionary            
    crypto_index = {value : key for (key, value) in crypto_dict.items()}
                   

    #Return the currency index list and the exchange rate 3-D matrix  
    return crypto_index, temp_matrix

def main(directory_name, intermediate_currency, minute, transaction_cost):
    """
    A function that calls the read_data function.
    
    Parameters:
        directory_name (String): name of the directory where the files are 
                                stored
        intermediate_currency (String): the intermediate currency
        minute (int): the minute for which the data is needed
        transaction_cost (int):                
    """
    
    crypto_index, exchange_rate_matrix = read_data(directory_name,
                                                   intermediate_currency, 
                                                   minute,
                                                   transaction_cost)
    return exchange_rate_matrix, crypto_index

if __name__ == "__main__":
    
    # Name of the directory where the files are stored
    directory_name = "\pure_crypto"
    
    intermediate_currency = "BTC"
    
    transaction_cost =  0 # values in {0.04, 0.2, 0.5, 5.9}
    

    start_minute = 1
    end_minute = 1 # 131040
    chunk_size = 1
    
    count = 0
    minute = start_minute
    while minute <= end_minute:
    
        if end_minute - minute + 1 < chunk_size:
            chunk_size = end_minute - minute + 1
            
            
        crypto_index, exchange_rate_matrix = read_data(directory_name, 
                                                       intermediate_currency, 
                                                       minute,
                                                       chunk_size,
                                                       transaction_cost)
    
        # get current date time
        now = datetime.now()
        dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

        if chunk_size == 1:
            writer = pd.ExcelWriter('pure_crypto_exchanges_' + dt_string + '.xlsx',\
                                engine='xlsxwriter')
    
            for t in range (chunk_size):
                df = pd.DataFrame(exchange_rate_matrix[t])
                df.to_excel(writer, sheet_name= 'Time_'+str(minute))
     
                writer.save()
        
        #if count == 0:
            #exchange_rate_matrix1 = exchange_rate_matrix
            
        #elif count == 1:
            #exchange_rate_matrix2 = exchange_rate_matrix
            
        #count += 1
        
        minute += chunk_size
    