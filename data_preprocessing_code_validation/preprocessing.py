# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:01:35 2020

@author: shamid
"""

import os
import pandas as pd
from datetime import datetime
import numpy as np

output_file = open("binance_end_dates.txt","w")

def extract_dates(directory_path,file_name,data_df):
    
#    print("In extract dates")
    
#    print(directory_path)
#    print(file_name)
#    print(data_df.head())
    
    start_time_unix = 1589068800        #2020-05-10 00:00:00
    end_time_unix = 1589673540          #2020-05-16 23:59:00
    
#    start_time_unix = 1577836800        #2020-01-01 00:00:00
#    end_time_unix = 1585699140          #2020-03-31 23:59:00
          
#    print(datetime.utcfromtimestamp(start_time_unix).strftime('%Y-%m-%d %H:%M:%S'))
#    print(datetime.utcfromtimestamp(end_time_unix).strftime('%Y-%m-%d %H:%M:%S'))
    
#    diff = int(end_time_unix - start_time_unix)
#    print("Number of minutes are:{}".format(diff))

    data_df['time'] = pd.to_numeric(data_df["time"])
    filtered_df = data_df[data_df['time'].between(start_time_unix,end_time_unix)]
    
    filtered_df.reset_index(drop=True, inplace=True)

#    print(filtered_df.head())
#    print(filtered_df.tail())

    filtered_df.to_csv(directory_path+"\\"+file_name, sep=',', index=False)
    
    return 0

def read_data(file_path, file_name):
    
    #print("In read data")
    #print(file_name)    
    data_df = pd.read_csv(file_path+file_name, usecols = ['time','open'])
        
    #print(data_df.head())
    #print(data_df.tail())
        
#    print(data_df.iloc[-1]['time'])
#    print(datetime.utcfromtimestamp(int(data_df.iloc[-1]['time'])).strftime('%Y-%m-%d %H:%M:%S'))
        
    end_date_unix = int(data_df.iloc[-1]['time'])
    end_date = datetime.utcfromtimestamp(int(data_df.iloc[-1]['time'])).strftime('%Y-%m-%d %H:%M:%S')
    
    
    output_file.write(str(end_date_unix)+",")
    output_file.write(str(end_date)+"\n")
        
    return data_df

if __name__ == "__main__":
    
    # Name of the directory where the files are stored
    directory_name = "\\binance"
    
    saving_directory_name = "\\binance_7_days_data"
    
    # Get the name of all the files in the directory
    data_files =  os.scandir(".\data"+directory_name)
    
#    count = 0
        
    for file in [entry for entry in data_files if entry.name != ".gitkeep"] :
        
        print(file.name)
        output_file.write(file.name+",")
        
        crypto_df = read_data(".\data"+directory_name+"\\",file.name)
        
        extract_dates(".\data"+saving_directory_name+"\\",file.name,crypto_df)
        
#        count += 1
#        if count == 1:
#            break
    
    output_file.close()
    