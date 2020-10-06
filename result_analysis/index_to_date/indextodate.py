# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 12:02:47 2020

@author: shamid
"""

from datetime import datetime

output_file = open("index_to_dates.txt","w")

start_index = 1
end_index = 131040 # {131040,}

start_time_unix = 1577836800        #2020-01-01 00:00:00
end_time_unix = 1585699140          #2020-03-31 23:59:00

for i in range(0, end_index):
    
    index = start_index + i
    time_unix = start_time_unix + i*60
    date = datetime.utcfromtimestamp(int(time_unix)).strftime('%Y-%m-%d %H:%M:%S')
    
    print("{}\t{}\t{}".format(index, time_unix, date))
    output_file.write("{}\t{}\t{}\n".format(index, time_unix, date))
    
output_file.close()