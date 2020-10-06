# -*- coding: utf-8 -*-
"""
Created on Mon Sep 14 11:21:51 2020

@author: shamid
"""

import pandas as pd
import os

# name of the directory
directory_name = "\CryptoFX_GA-master_Exp_3"

# get the name of all the files in the directory
result_files =  os.scandir(".\experiment_result"+directory_name)

# the window size of the moving average 
window_size = [10080] # {10080, 1440}




    
# read the files in the directory
for file in [entry for entry in result_files if entry.name.endswith('.txt')]:
                    
            
            print(file.name)
            
            for ws in window_size:
    
                print("Calculating moving average for widow size:{}:".format(ws))
    
                # new column name of the moving average
                new_coulmn_name = 'SMA_' + str(ws)
            
                # read the file and skip the top 15 lines 
                dataframe = pd.read_csv(".\experiment_result" +\
                                    directory_name+"\\"+\
                                    file.name, sep="\t", skiprows=15)
            
                # calculate the moving average for the window size
                for i in range(0, dataframe.shape[0] - (ws - 1)): 
                 
                    dataframe[new_coulmn_name] = dataframe.iloc[:,2].\
                                                rolling(window= ws).mean()
            
                # the headers for the dataframe to be written in the file
                header = ["Minute", "Fitness", new_coulmn_name]
            
                # write it to the file
                dataframe.to_csv(r".\experiment_result" + directory_name +\
                                 "\\" +"moving_average_" + str(ws) + ".csv",\
                                 index = False, columns = header)
        

# plot the graph        
#import matplotlib.pyplot as plt
#
#plt.figure(figsize=[15,10])
#plt.grid(True)
##plt.plot(dataframe['Fitness'],label='data')
#plt.plot(dataframe[new_coulmn_name],label='SMA')
#plt.legend(loc=2)    
