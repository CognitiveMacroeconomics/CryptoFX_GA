# -*- coding: utf-8 -*-
"""
Created on Wed Jul 29 11:01:35 2020

@author: shamid
"""

import os
import pandas as pd
from datetime import datetime
import numpy as np

#output_file = open("end_dates.txt","w")

def extract_dates(file_name,data_df):
    print("In extract dates")
    start_time_unix = 1589068800        #2020-05-10 00:00:00
    end_time_unix = 1589673540          #2020-05-16 23:59:00
    #print(datetime.utcfromtimestamp(1589068800).strftime('%Y-%m-%d %H:%M:%S'))
    #print(datetime.utcfromtimestamp(1589673540).strftime('%Y-%m-%d %H:%M:%S'))
    #diff = int(end_time_unix - start_time_unix)+1
    print("Number of minutes are:{}".format(diff))
    data_df['time'] = pd.to_numeric(data_df["time"])
    filtered_df = data_df[data_df['time'].between(1589068800,1589673540)]
    filtered_df.reset_index(drop=True, inplace=True)
#    print(filtered_df.head())
#    print(filtered_df.tail())
    filtered_df.to_csv(".\data\kraken\kraken_7_days_data\\"+file_name, sep=',', index=False)
    return 0

def read_data(directory_name):
    
    print("In read data")
    
    # Get the name of all the files in the directory
    data_files =  os.scandir(".\data"+directory_name)
    
    count = 0
    
    #end_date_list = []
    
    for file in [entry for entry in data_files if entry.name != ".gitkeep" and entry.name != "kraken_7_days_data"] :
        
        print(file.name)
        #output_file.write(file.name+",")
        data_df = pd.read_csv(".\data"+directory_name+"\\"+file.name, usecols = ['time','open'])
        
#        print(data_df.head())
#        print(data_df.tail())
        
#        print(data_df.iloc[-1]['time'])
#        print(datetime.utcfromtimestamp(int(data_df.iloc[-1]['time'])).strftime('%Y-%m-%d %H:%M:%S'))
#        
#        end_date = int(data_df.iloc[-1]['time'])
#        end_date = datetime.utcfromtimestamp(int(data_df.iloc[-1]['time'])).strftime('%Y-%m-%d %H:%M:%S')
        
#        output_file.write(str(end_date)+",")
#        output_file.write(str(datetime.utcfromtimestamp(
#                int(data_df.iloc[-1]['time'])).strftime('%Y-%m-%d %H:%M:%S'))+"\n")
        
        #end_date_list.append(end_date)
        
        extract_dates(file.name,data_df)
        
#        count += 1
#        if count == 1:
#            break
    
#    end_date_list = np.asarray(end_date_list)    
#    print("End date list is:{}".format(end_date_list))
#    min_date_unix = np.amin(end_date_list)
#    min_date =  datetime.utcfromtimestamp(min_date_unix).strftime('%Y-%m-%d %H:%M:%S')
#    min_date_index = np.argmin(end_date_list)
#    print("Minium date is:{} \t {}".format(min_date_unix, min_date))
#    print("Minium date index is:{}".format(min_date_index))
    return 0

if __name__ == "__main__":
    
    # Name of the directory where the files are stored
    directory_name = "\kraken"
    
    read_data(directory_name)
    
    #output_file.close()
    