# -*- coding: utf-8 -*-
"""
Created on Fri May  1 12:41:54 2020

@author: shamid
This code cleans the Daily_OHLC_pair data files that are saved in the directory
"cryptocompare_data" and saves it in the directory "clean_data"
"""

import os
import pandas as pd
import datetime


# Global Variables
saving_directory_name = "pure_stable_crypto"

output_file = open("log.txt","w")


def check_missing_values(raw_data_df):
    """This function checks if there are an NaN vales in the dataset. 
    If there are it raises a ValueError.
    """
    # count the number of nan values
    count_nan = raw_data_df.isnull().sum().sum()
        
    # If there is a NaN value raise a value error exception
    if count_nan != 0:
        raise ValueError("A NaN value found")

def check_start_date(raw_data_df):
    """This function checks if the retrieved data starts from 1st jan 
    2020, 12:00 am. If not, it appends data at the beginning and sets "open" 
    to 0.0
    """
    
    # if does not start from 1st jan 2020, 12:00 am ("1577836800" is unix time)   
    if(raw_data_df.iloc[0]['time'] > 1577836800):

        # get the time from the first row of the dataframe        
        start_date = raw_data_df.iloc[0]['time']
        
        # a dictionary to store new "time" and "open"
        temp_data = {}
        
        # a list that stores new time
        new_time = []
        
        # a list that stores new open (0.0)
        new_open = []
        
        # the time should begin from 1st jan 2020, 12:00 am
        time = 1577836800
        
        # while time is less than start time - 60
        while(time <= start_date - 60):
            
            # append the value in "time" variable to "new_time" list           
            new_time.append(time)
            
            # append 0 to "new_open" list
            new_open.append(0)
            
            # increament time by 60 (secs)
            time = time + 60
        
        
        temp_data["time"] = new_time
        temp_data["open"] = new_open
        
        # a temporary variable to store temp data
        temp_df = pd.DataFrame(temp_data)
        
        # concatenate the new data and the old data
        frames = [temp_df, raw_data_df]
        
        new_df = pd.concat(frames).reset_index(drop = True)
        
        # return the new concatenated data farme        
        return new_df
    
    # if it starts from 1st jan 2020, 12:00 am then return the dataframe 
    return raw_data_df

def check_end_date(start_data_df):
    """This function checks if the retrieved data ends on 31st March 2020, 
     11:59 pm, if not then it appends data at the end and sets "open" to 0.0
    """
    # if does not end on 31st March 2020, 11:59 am ("1585699140" unix time)
    
    if(start_data_df.iloc[start_data_df.shape[0]-1]['time'] < 1585699140):
        
        # get the time from the last row of the dataframe
        end_date = start_data_df.iloc[start_data_df.shape[0]-1]['time']
        
        # a dictionary to store new "time" and "open"
        temp_data = {}
        
        # a list that stores new time
        new_time = []
        
        # a list that stores new open
        new_open = []
        
        # set time to "end_date" + 60
        time = int(end_date) + 60 
        
        # while time is less than 31st March 2020, 11:59 pm 
        while(time <= 1585699140):
            
            # append the value in "time" to "new_time" list
            new_time.append(time)
            
            # append 0 to "new_open" list
            new_open.append(0)
            
            #increament time by 60 (secs)
            time = time + 60
                
        temp_data["time"] = new_time
        temp_data["open"] = new_open
        
        # a temorary variable to store temp data
        temp_df = pd.DataFrame(temp_data)
        
        # concatenated the new data and the old data        
        frames = [start_data_df, temp_df]
        
        new_df = pd.concat(frames).reset_index(drop = True)
        
        # returns the new concatenated data        
        return new_df
    
    # if it ends on 31st March 2020, 11:59 pm then return the dataframe
    return start_data_df

def check_intervals(data_df):
    """this function checks if there is an interval of more than 60 secs 
    between two rows. If there is then it checks if the data is missing for 
    a part of the day. Eg. if the data for 2nd Feb is till "12:36 pm"
    """
    
    # store the difference between two rows in "diff_time"
    diff_time = data_df['time'].rolling(2)\
                .apply(lambda x: x[1] - x[0], raw=True)
                
    # remove duplicates from "diff_time"
    diff_time = diff_time.dropna()
    
    # for each "i" in "diff_time"
    for i in diff_time.drop_duplicates():
        
        # if the difference is other than 60 secs
        if(i != 60):

            # get the index of the difference in "diff_time", index returns a 
            # list
            idx = diff_time[diff_time == i].index
            
            # iterate thorugh the indexes
            for j in range(len(idx)):
                
                # get the time of the row before the index
                gap_start_time = int(data_df.loc[idx[j]-1][0])
                
                # turn the unix time into "%H:%M:%S" format
                gap_start_time2 = datetime.datetime\
                                .utcfromtimestamp(gap_start_time)
                
                # a variable with time set as "23:59:00"
                check_time = datetime.datetime.strptime("23:59:00", "%H:%M:%S")
                
                # if the time is other than 23:59:00 then raise an error
                if(gap_start_time2.time() != check_time.time()):
                    
                    print("start timestamp: {}".format(gap_start_time2.time()))
                    output_file.write("start timestamp: {} \n"\
                                      .format(gap_start_time2.time()))
                    raise ValueError("start timestamp: {} at index: {}"\
                                     .format(gap_start_time2.time(), idx[j]-1))
                
                # get the time of the row at index
                gap_end_time = int(data_df.loc[idx[j]][0])
                
                # turn the unix time into "%H:%M:%S" forma
                gap_end_time2 = datetime.datetime\
                                .utcfromtimestamp(gap_end_time)
                
                # a variable with time set as "00:00:00"
                check_time2 = datetime.datetime.strptime("00:00:00",\
                                                         "%H:%M:%S")
                
                # if the time is other than "00:00:00" then rais an error
                if(gap_end_time2.time() != check_time2.time()):
                    
                    print("end timestamp: {}".format(gap_end_time2.time()))
                    output_file.write("end timestamp: {} \n"\
                                      .format(gap_end_time2.time()))
                    raise ValueError("end timestamp: {} at index: {}"\
                                     .format(gap_end_time2.time(), idx[j]))
               
            
def fill_intervals(data_df):
    """this function checks if there is difference of time interval other than 
    60 and if there is then it appends new rows with new "time" and "open"
    """
    
    i = 0
    while i < data_df.shape[0]-1:
         
        # Calculate the difference in interval
        interval_diffrence = data_df.loc[i+1][0] - data_df.loc[i][0]
        
        # If interval if between 0 and 60 then increase the time interval to 
        # 60 secs and keep the "open" value the same
        if interval_diffrence < 60 and interval_diffrence > 0:
            print("Interval is less than 60")
            output_file.write("Interval is less than 60")
            data_df.loc[i+1, 'time'] = data_df.loc[i+1][0] \
                                            + (60 - interval_diffrence)
        
        # if the interval is greater than 60 the add new time and set open = 0
        # TODO: improve the efficiency the logic                                    
        elif interval_diffrence > 60:
              
            temp_df1 = data_df[0:i+1]           
            temp_df2 = data_df[i+1:] 
            insert = pd.DataFrame({"time": data_df.loc[i][0] + 60, 
                                   "open": 0}, index=[i+1])
            data_df =  pd.concat([temp_df1,insert,temp_df2])\
                            .reset_index(drop=True)
                            
            
            
        # If the interval is less than 0 secs then raise a ValueError
        elif interval_diffrence < 0:
            print(("Interval is negative at index {}:".format(i)))
            output_file.write(("Interval is negative at index {}: \n"\
                               .format(i)))
            raise ValueError("Interval is negative at index {}:".format(i))
        
        i += 1
        
        
    # Check again to make sure that there are no more time intervals in the 
    # dataset which are other than 60 sces
    diff_time = data_df['time'].rolling(2)\
                .apply(lambda x: x[1] - x[0], raw=True)
    diff_time = diff_time.dropna()
    
    
    for i in diff_time.drop_duplicates():
        if(i != 60):
            print()
            print("difference is at {} secs at {}"\
                  .format(i, diff_time[diff_time == i].index))
            output_file.write("difference is at {} secs at {} \n"\
                  .format(i, diff_time[diff_time == i].index))
            # If there is any such record then return a value error
            raise ValueError("Interval other than 60 found")
            
    # Save the edited data to clean_data_df        
    crypto_data_df = data_df

    # return clean_data_df
    return crypto_data_df
                           

def main():
    
    try:
        # Get the current working directory
        current_working_dir = os.getcwd()
        
        print("current working directory:{}".format(current_working_dir))
        output_file.write("current working directory:{} \n"\
                          .format(current_working_dir))
        
        # Change directory to "crypto_raw_data" direcotry
        raw_data_files =  os.scandir(current_working_dir
                                     + "\\cryptocompare_data_new")
        
        
    except IOError as e:
        output_file.write("Incorrect path: {} \n".format(e))
        print("Incorrect path: {}".format(e))
    
    
    # iterate over all files in the directory "cryptocompare_data"
    for entry in raw_data_files:
        
        try:
        
            print(entry.name)
            output_file.write("{}\n".format(entry.name))
            
            # The data frame will only contain the "time" and "open" columns
            raw_data_df = pd.read_csv(".\\cryptocompare_data\\"
                                     + entry.name, sep=',', header=None,
                                     usecols = [0,4], names=['time', 'open'])

            
            # Call the function to check for NaN values
            check_missing_values(raw_data_df)
            
            # Call the function check intervals for a part of a day
            check_intervals(raw_data_df)
            
            # Call the function to fill intervals
            crypto_data_df = fill_intervals(raw_data_df)
            
            # Call the function to add data from start date 1st jan, 2020 
            start_data_df = check_start_date(crypto_data_df)
            
            # Call the function to add data till end data 31st March 2020
            clean_data_df = check_end_date(start_data_df)

            # Number of dauys of data for each pair should be 91
            print("Number of days: {}".format(((clean_data_df\
                                              .shape[0])/60)/24))
            output_file.write("Number of days: {} \n"\
                              .format(((clean_data_df.shape[0])/60)/24))
            
            # Change directories to save the file
            os.chdir(os.path.abspath(os.curdir+"\\clean_data"))
            # Create the directory to store the clean files
            if not os.path.exists(saving_directory_name):
                os.mkdir(saving_directory_name)
            saving_directory_path = os.path.abspath(os.curdir+"\\" 
                                                    + saving_directory_name)
            os.chdir(saving_directory_path)
            
            clean_data_df.to_csv(entry.name+".csv", mode = 'w',\
                                 columns=["time", "open"], index=False)
            
            # going back to the "preprocessing" directory            
            os.chdir("..")
            os.chdir("..")
                                      
        except FileNotFoundError as e:
            output_file.write("File not found: {} \n".format(e))
            print("File not found: {}".format(e))
            print("Next")
            
        except ValueError as e:
            output_file.write("{}\n".format(e))
            print(e)
            print("Next")
    
    
if __name__ == '__main__':
    main()
    output_file.close()