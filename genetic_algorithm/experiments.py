# -*- coding: utf-8 -*-
"""
Created on Fri Nov  6 08:07:11 2020

@author: shamid
"""

import source
from ga import Chromosomes, Population
from datetime import datetime
import sys
import traceback

def run(f, directory_name, minute,pop_size, intermediate_currency,
        transaction_cost, max_generations, chunk_size, flag):
    
    """A function that starts the optimization process.
    """
    
    print("Optimizing for minute: {}".format(minute))
    # Call main() from source.py to read the files an extarct the exchnage
    # rates. 
    # source.main() returns the exchange rate matrix and the the index of the
    # crypto currencies. 
    exchange_rate_matrix, Chromosomes.crypto_index =\
                                                        source.main(
                                                        directory_name,
                                                        intermediate_currency,
                                                        minute,
                                                        chunk_size,
                                                        transaction_cost)
    # wirte the index of the currencies to the file
    if flag[0] == True:
        f.write("{}\n".format(Chromosomes.crypto_index))
        f.write("########################################\n")
        f.write("Minute|Arbitrage|Fitness\n")
        flag[0] = [False]
    
    for t in range(chunk_size):
                
        print("########################################")
        print("Optimizing for minute: {}".format(minute+t))
        print("########################################\n")
        
        # Set the exchnage rate matrix
        Chromosomes.exchange_rate_matrix = exchange_rate_matrix[t]
                
        # Create the Population object
        # Set the population size
        # Set the probability of crossover
        # Set the probability of mutation
        pop = Population(size = pop_size, crossover = 0.8, mutation = 0.3)
            
        # Run the optimization procedure for max_generations number of generations
        for i in range(1, max_generations + 1):
            
            print("Generation: {}".format(i))
            
            # Print the top most chromosome in the population
            print("{}\t{}".format(pop.entire_population[0].chromosome,
                                      pop.entire_population[0].fitness))
                
            # Start evolving the population
            pop.evolve()
        
        # Write to file        
        f.write("{}|".format(minute+t))
        for j in (pop.entire_population[0].chromosome):
            f.write("{} ".format(j))
        f.write("|{}\n".format(pop.entire_population[0].fitness))
            

        
def experiment_1():
    
    """
    A function to set the parameters of of the experiment
    """
    
    # Get current date time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")
    
    # a file to write the output logs
    f = open('./log/pure_crypto_BTC_7chromo'+dt_string+".txt", 'w')
    
    # Name of the directory where the files are stored
    # {"\pure_crypto", "\stable_crypto", "\pure_stable_crypto"}
    directory_name = "\pure_crypto" 
        
    # Set the start exchange currency
    Chromosomes.start_exchange_currency = "USD"
    f.write("Start Currency:{}\n".format(Chromosomes.start_exchnage_currency))
    
    # Set the end exchange currency
    Chromosomes.end_exchange_currency = "USD"
    f.write("End Currency:{}\n".format(Chromosomes.end_exchnage_currency))
    
    # Set the Intermediate Crypto Currency
    # DnB set this to a fiat currency
    intermediate_currency = "BTC"
    f.write("Intermediate Currency: {}\n".format(intermediate_currency))
    
    # Set the transaction cost
    transaction_cost =  0.5 * 0.01 # values in {0, 0.04, 0.2, 0.5, 5.9}
    f.write("Transaction Cost: {}\n".format(transaction_cost))
    
    # Set the mintue you want to start at
    start_min = 1
    f.write("Start Minute: {}\n".format(start_min))
    
    # Set the minute you want to end at
    end_min = 131040 # integer between [1, 131040]
    f.write("End Minute: {}\n".format(end_min))
    
    # Chunk size
    chunk_size = 1000
    
    # Set the num of crypto currencies:
    # Pure Crypto: 34
    # Stable Crypto: 23
    # Pure-Stable Crypto: 56m
    # you can also set the number of unique currencies in the dataset
    Chromosomes.num_crypto = 34
    f.write("Number of currencies: {}\n".format(Chromosomes.num_crypto))
    
    f.write("############# GA Parameters #############\n")
            
    # Set the number of generations to run the GA
    max_generations = 50
    f.write("Number of Generations: {}\n".format(max_generations))
    
    pop_size = 500
    f.write("Population Size: {}\n".format(pop_size))
        
    # Set the length of the chromosome
    Chromosomes.chromosome_length = 7 # [5, 7, 10]
    f.write("Chromosome length: {}\n".format(Chromosomes.chromosome_length))
    
    # Set the number of offsprings to be generated
    Population.num_offsprings = 250
    f.write("Number of offsprings: {}\n".format(Population.num_offsprings))
    
    # Set the tournament size for parent selection
    Population.tournamnet_size = 10
    f.write("Tournament size: {}\n".format(Population.tournamnet_size))
    
    f.write("Crossover Probability: {}\n".format(0.8))    
    f.write("Mutation Probability: {}\n".format(0.3)) 
    
            
    # Set the minute to start minute
    minute = start_min
    
    
    flag = [True]
    while minute <= end_min:
        
        if end_min - minute + 1 < chunk_size:
                chunk_size = end_min - minute + 1
        
        run(f, directory_name, minute, pop_size, intermediate_currency,
            transaction_cost, max_generations, chunk_size, flag)

        # Increase the minute by one
        minute += chunk_size                                       
    
    f.close()
    
    return 0


if __name__ == "__main__":
       
    
    try:
        experiment_1()
        
    except Exception as e:
        e = sys.exc_info()
        print('Error Return Type: ', type(e))
        print('Error Class: ', e[0])
        print('Error Message: ', e[1])
        print('Error Traceback: ', traceback.format_tb(e[2]))

    