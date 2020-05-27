# -*- coding: utf-8 -*-
"""
Created on Wed May 27 09:21:02 2020

@author: shamid
This code separates pure crypto and stable crypto pairs that are stored in 
"clean_data/pure_stable_crypto" and copies them to "clean_data/pure_crypto" and
"clean_data/stable_crypto" respectively.  

"""
import os
import shutil

# Names of pure crypto-currency
pure_crypto_names = [
        'ADA', 'ALGO','BCD', 'BCH', 'BCN', 'BSV', 'BTC', 'BTG', 'DASH', 'DCR',
        'DGB', 'DOGE', 'ETC', 'ETH', 'HC', 'HOT', 'IOST', 'LSK', 'LTC',
        'MIOTA', 'NANO', 'NEO', 'NPXS', 'QTUM', 'QNT', 'RVN', 'THETA',
        'TRX', 'USD', 'XMR', 'XVG', 'ZEC'
        ]

# Names of stable coin crypto-currency 
stable_crypto_names = [
        'ABBC', 'AOA', 'ATOM', 'BGBP', 'BITUSD', 'BTS', 'BUSD', 'DAI', 'DENT',
        'DRG', 'EURS', 'GUSD', 'MKR', 'OMG', 'PAX', 'RSV', 'STEEM', 'TUSD', 
        'USD', 'USDC', 'USDT', 'VET', 'XEM', 'XLM', 'XRP', 'XTZ'
        ]

# Names of pure and stable coin crypto-currency 
pure_stable_crypto_names = [
        'ABBC', 'ADA', 'ALGO', 'AOA', 'ATOM', 'BCD', 'BCH', 'BCN', 'BGBP',
        'BITUSD', 'BSV', 'BTC', 'BTG', 'BTS', 'BUSD', 'DAI', 'DASH', 'DENT', 
        'DCR', 'DGB', 'DOGE', 'DRG', 'ETC', 'ETH', 'EURS', 'GUSD', 'HC', 'HOT',
        'IOST', 'LSK', 'LTC', 'MIOTA', 'MKR', 'NANO', 'NEO', 'NPXS', 'OMG',
        'PAX', 'QTUM', 'QNT', 'RSV', 'RVN', 'STEEM', 'THETA','TRX', 'TUSD', 
        'USD', 'USDC', 'USDT', 'VET', 'XEM', 'XLM', 'XMR', 'XRP', 'XTZ','XVG',
        'ZEC'
        ]

crypto_names = stable_crypto_names
directory_name = "stable_crypto"

def main():
    try:
        # Get the current working directory
        current_working_dir = os.getcwd()
        
        print("current working directory:{}".format(current_working_dir))
        
        # Change directory to "crypto_raw_data" direcotry
        data_files =  os.scandir(current_working_dir
                                     + "\\clean_data\\pure_stable_crypto")\
                                   
        
    except IOError as e:
        
        print("Incorrect path: {}".format(e))
               
    for entry in data_files:
        #print(entry.name)
        for name_begin in crypto_names:
            if entry.name.startswith(name_begin):
                for name_end in crypto_names:
                    if entry.name.endswith("_"+name_end+".csv"):
                        print(entry.name)
                        
                        src = current_working_dir + "\\clean_data\\pure_stable_crypto\\"+entry.name
                        dst = current_working_dir + "\\clean_data\\"+directory_name
                        shutil.copy2(src,dst)
        
        
if __name__ == '__main__':
    main()
    
