# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:45:03 2020

@author: shamid
"""
from random import randint, random, choice, sample
import source
from datetime import datetime
import sys
import traceback

__all__ = ['Chromosomes','Population']


class Chromosomes:
    """
    This class is used to define a chromosome for the genetic algorithm
    simulation.
    
    This class is essentially nothing more than a container for the details of 
    the chromosome, namely the gene (the string that represents our target 
    string) and the fitness (how close the gene is to the target string).
    
    Note that this class is immutable. Calling mate() or mutate() will result 
    in a new chromosome instance being created.
    """
    # The exchange rate matrix for fitness calculation
    exchange_rate_matrix = []
    
    # Number of crypto currencies
    num_crypto = 0
    
    # Index of crypto currencies
    crypto_index = {}
    
    # Length of each chromosome 
    chromosome_length = 0

    # Start exchange currency
    start_exchnage_currency = "USD"
    
    # End exchange currency
    end_exchnage_currency = "USD"
        
    def __init__(self, chromosome):
        """
        Constructor to initialize the chromosome and its fitness
        
        Parameter:
        chromosome (list): chromosome of the population
        """

        self.chromosome = chromosome
        self.fitness = Chromosomes.calculate_fitnesss(chromosome)
        
    
    def crossover_onepoint(self, mate):
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        One Point Crossover
        
        Parameter:
        mate (Chromosome): the chromosome to required to mate with
        """
        
        # Select a pivot point
        pivot = randint(0, len(self.chromosome) - 1)
        
        # Select genes from the first parent uptil the pivot and from the 
        # second parent from the pivot till the end 
        offspring1_temp = self.chromosome[:pivot] + mate.chromosome[pivot:]
        
        offspring1 = []
        
        # Iterate through offspring1_temp and remove duplicates after the pivot
        for i in range(len(offspring1_temp)):
            
            # While there are duplicates in genes after the pivot
            while offspring1_temp.count(offspring1_temp[i])>1 and i >= pivot:
                
                # Generate a random gene
                gene = randint(0, Chromosomes.num_crypto - 1)
                
                # Remove the duplicate by updating it with the new gene
                offspring1_temp[i] = gene
                
            # Append to offspring1
            offspring1.append(offspring1_temp[i])
        
        # Select genes from the second parent uptil the pivot and from the 
        # first parent from the pivot till the end
        offspring2_temp = mate.chromosome[:pivot] + self.chromosome[pivot:]
        
        offspring2 = []
        
        # Iterate through offspring2_temp and remove duplicates after the pivot
        for i in range(len(offspring2_temp)):
            
            # While there are duplicates in genes after the pivot
            while offspring2_temp.count(offspring2_temp[i])>1 and i >= pivot:
                
                # Generate a random gene
                gene = randint(0, Chromosomes.num_crypto - 1)
                
                # Remove the duplicate by updating it with the new gene    
                offspring2_temp[i] = gene
                
            # Append to offspring2
            offspring2.append(offspring2_temp[i])
        
        return Chromosomes(offspring1), Chromosomes(offspring2)
    
    
    def crossover_ord1(self, mate):
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        Order One Crossover
        
        Parameter:
        mate (Chromosome): the chromosome to required to mate with
        """
        
        # Set the first parent
        p1 = self.chromosome
        
        # Set the second parent
        p2 = mate.chromosome
        
        # Get the length of the parent
        size = len(p1)
        
        # Generate 2 pivots as random numbers such that 0 < r1 < r2 < size-1
        r1, r2 = sample(range(size-1), 2)
        if r1 > r2:
            r1, r2 = r2, r1

        # Initialize offspring1 with -1, its length is the same as that of the 
        # parent 
        offspring1 = [-1] * size
        
        # Copy the genes in parent1 between the two pivots to the same
        # position(s) in offspring1
        for i in range(r1 ,r2+1):
            offspring1[i] = p1[i]
            
        # Rotate parent2 to the left by moving the gene after the pivot to the 
        # begining of the list
        p2_rotate = p2[r2+1:]+p2[:r2+1]

        # Set temp1 list to 0, the length of which is the number of elements 
        # not lying between the pivot position        
        temp1 = [0] * (size-(r2-r1)-1) 

        j = 0
        
        # Add to temp1 genes from p2_rotate that are not in offsrping1
        for i in range(size):
            
            if p2_rotate[i] not in offspring1:
                temp1[j] = p2_rotate[i]
                j += 1
                
            if j == len(temp1):
                break
        
        # Add the genes from temp1 to offspring1 starting from the position
        # after the second pivot and wrapping around offspring1
        for i in range(len(temp1)):
            idx = (r2 + i + 1) % size
            offspring1[idx] = temp1[i]
            
        
        # Initialize offspring2 with -1, its length is the same as that of the 
        # parent         
        offspring2 = [-1] * size
        
        # Copy the genes in parent2 between the two pivots to the same
        # position(s) in offspring2
        for i in range(r1, r2+1):
            offspring2[i] = p2[i]
            
        # Rotate parent1 to the left by moving the gene after the pivot to the 
        # begining of the list        
        p1_rotate = p1[r2+1:]+p1[:r2+1]
        
        # Set temp2 list to 0, the length of which is the number of elements 
        # not lying between the pivot position
        temp2 = [0] * (size-(r2-r1)-1)
        
        j = 0
        
        # Add to temp2 genes from p1_rotate that are not in offsrping2
        for i in range(size):
            
            if p1_rotate[i] not in offspring2:
                temp2[j] = p1_rotate[i]
                j += 1
            
            if j == len(temp2):
                break
        
        # Add the genes from temp1 to offspring1 starting from the position
        # after the second pivot and wrapping around offspring1        
        for i in range(len(temp2)):
            idx = (r2 + i + 1) % size
            offspring2[idx] = temp2[i]
        
        # Return the two offsprings as Chromosomes object
        return Chromosomes(offspring1), Chromosomes(offspring2)
    
    def mutate(self):
        """
        Method used to generate a new chromosome based on a change in a random
        character in the geene of this chromosome.
        """

        # Get the list of genes in the chromosome
        genes = list(self.chromosome)

        # Select a random index
        idx = randint(0, len(genes) - 1)
        
        # Generate a random gene
        new_gene = randint(0, Chromosomes.num_crypto - 1)
        
        for key, value in Chromosomes.crypto_index.items():
            # Get the index of the start_exchnage currency
            if value == Chromosomes.start_exchange_currency:
                start_ex_idx = key
                
            # Get the index of the end_exchnage currency    
            if value == Chromosomes.end_exchange_currency:
                end_ex_idx = key
        
        # While the new_gene is tha same as the gene at idx and same as the
        # start and end currency keep generating new genes
        while (new_gene in genes) or (new_gene in [start_ex_idx, end_ex_idx]):\
            new_gene = randint(0, Chromosomes.num_crypto - 1)
                
        # Update the gene at idx to new_gene
        genes[idx] = new_gene
                
        return Chromosomes(genes)
        
    
    @staticmethod
    def calculate_fitnesss(chromosome):
        """
        Helper method used to return the fitness for the chromosome based on
        its genes.
        
        Parameter:
        chromosome (Chromosome): chromosome whoes fitness needs to be 
                                calculated
        """
        
        for key, value in Chromosomes.crypto_index.items():
            
            # Get the index of the start_exchnage currency
            if value == Chromosomes.start_exchange_currency:
                start_ex_idx = key
                
            # Get the index of the end_exchnage currency    
            if value == Chromosomes.end_exchange_currency:
                end_ex_idx = key
                   
        cost = 1
        
        # Iterate over the chromosome and get the exchange rate values from the
        # exchange_rate_matrix
        # E.g. USD -> BTC -> ZEC -> ETH -> USD
        for i in range(len(chromosome)+1):
            
            value = 0

            if i == 0:
                
#                print("{} to {} is: {}".format(Chromosomes\
#                                  .start_exchange_currency,\
#                                  Chromosomes.crypto_index[chromosome[i]],\
#                                  Chromosomes.exchange_rate_matrix\
#                                  [start_ex_idx][chromosome[i]]))
                
                value = Chromosomes.exchange_rate_matrix[start_ex_idx]\
                                                        [chromosome[i]]
                
            elif i == len(chromosome):
                
#                print("{} to {} is : {}".format(Chromosomes
#                                      .crypto_index[chromosome[i-1]],\
#                                      Chromosomes.end_exchange_currency,\
#                                      Chromosomes.exchange_rate_matrix\
#                                      [chromosome[i-1]][end_ex_idx]))
                
                value = Chromosomes.exchange_rate_matrix[chromosome[i-1]]\
                                                        [end_ex_idx]
                
            else:
                
#                 print("{} to {} is : {}".format(Chromosomes\
#                                      .crypto_index[chromosome[i-1]],\
#                                     Chromosomes.crypto_index[chromosome[i]],\
#                                     Chromosomes.exchange_rate_matrix\
#                                     [chromosome[i-1]][chromosome[i]]))
                 
                 value = Chromosomes.exchange_rate_matrix[chromosome[i-1]]\
                                                         [chromosome[i]]
            
            # Calculate fitness                       
            cost *= value
            
        fitness = cost # cost, max(cost - 1, 0)

        return fitness
    
    @staticmethod
    def gen_random():
        """
        A convenience mehtod for generating a random chromosome with a random
        gene.
        """

        chromosome = []
        
        for key, value in Chromosomes.crypto_index.items():
            # Get the index of the start_exchnage currency
            if value == Chromosomes.start_exchange_currency:
                start_ex_idx = key
                
            # Get the index of the end_exchnage currency    
            if value == Chromosomes.end_exchange_currency:
                end_ex_idx = key
        
        # Generate random genes and append it to chromosome 
        while len(chromosome) < (Chromosomes.chromosome_length):
            
            gene = randint(0, Chromosomes.num_crypto - 1)
            
            # Make sure that the gene is already not present in the chromosome
            if (gene not in chromosome)\
                and (gene != start_ex_idx and gene != end_ex_idx):
                chromosome.append(gene)
                     
        return Chromosomes(chromosome)
    
    

class Population:
    """
    A class representing a population for a genetic algorithm simulation.
    
    A population is simply a sorted collection of chromosomes (sorted by 
    fitness) that has a convenience method for evolution. This implementation
    of a population uses a tournamnet selection algorithm for selecting parents
    for crossover during each generation's evolution.
    
    Note that this object is mutable, and calls to the evolve() method will 
    generate a new collection of chromosome objects.      
    """
    # The tournament size for parent selection
    tournamnet_size = 0
    
    # Number of offsprings to be generated
    num_offsprings = 0
    
    def __init__(self, size=10, crossover=0.8, mutation=0.3):
        """
        Constructor to initializes the probabbility of crossover and the
        probablility of mutation and the size of the population
        
        Parameters:
        size (int): size of the population
        crossover (float): crossover probablity
        mutation (float): mutation probability
        """
        
        self.crossover = crossover
        self.mutation = mutation
        self.size = size
        
        buf = []
        
        for i in range(self.size):
            
            # Call gen_random() and append the randomly initialized chromosome 
            # to the buf
             buf.append(Chromosomes.gen_random())
            
        # Sort the chormosomes in buf based on their fitness, convert it into a
        # list it to the instance variable entire_population
        self.entire_population = list(sorted(buf[:size],
                                             key=lambda x: x.fitness,
                                             reverse=True))
        
        # Print the entire population
#        print("The entire population is:")
#        for chromo in self.entire_population:
#            print("{}\t{}".format(chromo.chromosome,
#                                  chromo.fitness))
        
    
    def tournament_selection(self):
        """
        A helper method used to select a random chromosome from the population
        using a tournament selection algorithm.
        
        """
        # Select a random chromosome form entire_population
        best = choice(self.entire_population)
        
       # choose the best chromosome from the tournament
        for i in range(Population.tournamnet_size):
            
            cont = choice(self.entire_population)
            
            if(cont.fitness > best.fitness):
                best = cont
        
        # Return the selected chromosome
        return best 
    
    def select_parents(self):
        """
        A helper method used to select two parents from the population using a
        tournament selection algorithm
        """
        # Return the two selected parents
        return (self.tournament_selection(), self.tournament_selection())
    
    
    def evolve(self):
        """
        Method to evolve the population of chromosomes.
        """
        # Store the population in old_population before evolving it.
        # Exclude the tail of the population equal to the amount of number of
        # offsprings to be generated
        old_population = self.entire_population[:len(self.entire_population)\
                                                    - self.num_offsprings]
        
        buf = []
        
        # Iterate this loop until i less than or equal to the num_offspring/2
        # Every iteration generates two offsprings
        i = 0
        while i < self.num_offsprings/2:
            
            # Generate a random number and check if it is less than the 
            # probability of crossover
            if random() <= self.crossover:
                
                # call select_parents(), it returns two parents
                (parent1, parent2) = self.select_parents()
                
                # Call crossover_ord1 it returns a tuple of two offsprings 
                # after applying the crossover operation
                offspring_crossover = parent1.crossover_ord1(parent2)
                
                # Mutate the offsprings in offspring_crossover
                for offspring in offspring_crossover:
                    
                    # Generate a random number and check if it is less than the 
                    # probability of mutation
                    if random() <= self.mutation:
                        
                        # Call mutate() to mutate the offspring
                        mutated_offspring = offspring.mutate()
                        
                        # Append the mutated offspring to buf
                        buf.append(mutated_offspring)

                    else:
                        
                        # If the random number generated is greater then 
                        # append to buf without mutation
                        buf.append(offspring)

                i += 1
                
        # Old Population and buf are combined to generate the new population
        new_population = old_population + buf
        
        # Sort the new population based on the fitness of each chromosome and
        # update the instance variable entire_population
        self.entire_population = list(sorted(new_population[:],
                                             key=lambda x: x.fitness,
                                             reverse = True))
        # Print the new population
#        print("New Population")
#        for pop in self.entire_population:
#            print("{}\t{}".format(pop.chromosome, pop.fitness))


if __name__ == "__main__":
    
    # Get current date time
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y_%H-%M-%S")

    # a file to write the output logs
    f = open('./log/pure_crypto_BTC_7chromo'+dt_string+".txt", 'w')
    
    # Pure Crypto: 
    #   Intermerdiate Currency: BTC, ETH, BCH
    
    # Stable Crypto:
    #   Intermerdiate Currency: USDT, XRP      
    
    # Pure-Stable Crypto:
    #   Intermerdiate Currency: BTC, XRP, ETH, USDT    
    
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
    intermediate_currency = "BTC"
    f.write("Intermediate Currency: {}\n".format(intermediate_currency))
    
    # Set the transaction cost
    transaction_cost =  0.5 * 0.01 # values in {0.04, 0.2, 0.5, 5.9}
    f.write("Transaction Cost: {}\n".format(transaction_cost))
    
    # Set the mintue you want to start at
    start_min = 1
    f.write("Start Minute: {}\n".format(start_min))
    
    # Set the minute you want to end at
    end_min = 10000 # integer between [1, 131040]
    f.write("End Minute: {}\n".format(end_min))
    
    # Chunk size
    chunk_size = 1000
    
    f.write("############# GA Parameters #############\n")
    # Set the number of generations to run the GA
    max_generations = 50
    f.write("Number of Generations: {}\n".format(max_generations))
    
    f.write("Population Size: {}\n".format(500))
        
    # Set the length of the chromosome
    Chromosomes.chromosome_length = 7
    f.write("Chromosome length: {}\n".format(Chromosomes.chromosome_length))
    
    # Set the num of crypto currencies:
    # Pure Crypto: 34
    # Stable Crypto: 23
    # Pure-Stable Crypto: 56
    Chromosomes.num_crypto = 34 
    
    # Set the number of offsprings to be generated
    Population.num_offsprings = 250
    f.write("Number of offsprings: {}\n".format(Population.num_offsprings))
    
    # Set the tournament size for parent selection
    Population.tournamnet_size = 10
    f.write("Tournament size: {}\n".format(Population.tournamnet_size))
    
    f.write("Crossover Probability: {}\n".format(0.8))    
    f.write("Mutation Probability: {}\n".format(0.3)) 
    f.write("########################################\n")
    
    minute = start_min
    
    f.write("Minute|Arbitrage|Fitness\n")
    while minute <= end_min:
        try:
            
            if end_min - minute + 1 < chunk_size:
                chunk_size = end_min - minute + 1
            
            
            # Call main() from source.py to read the files an extarct the exchnage
            # rates. 
            # source.main() returns the exchange rate matrix and the the index of the
            # crypto currencies. 
            exchange_rate_matrix, Chromosomes.crypto_index =\
                                                        source.main(directory_name,
                                                        intermediate_currency,
                                                        minute,
                                                        chunk_size,
                                                        transaction_cost)
            for t in range(chunk_size):
                
                print("########################################")
                print("Optimizing for minute: {}".format(minute+t))
                print("########################################\n")
                
                Chromosomes.exchange_rate_matrix = exchange_rate_matrix[t]
                                            
                # Create the Population object
                # Set the population size
                # Set the probability of crossover
                # Set the probability of mutation
                pop = Population(size = 500, crossover = 0.8, mutation = 0.3)
        
                # Run the optimization procedure for max_generations number of generations
                for i in range(1, max_generations + 1):
                
                    print("Generation: {}".format(i))
                
                    # Print the top most chromosome in the population
                    print("{}\t{}".format(pop.entire_population[0].chromosome,
                                      pop.entire_population[0].fitness))
                
                    # Start evolving the population
                    pop.evolve()
                
                f.write("{}|".format(minute+t))
                for j in (pop.entire_population[0].chromosome):
                    f.write("{} ".format(j))
                f.write("|{}\n".format(pop.entire_population[0].fitness))
            
               
            minute += chunk_size
            
        except Exception as e:
            e = sys.exc_info()
            print('Error Return Type: ', type(e))
            print('Error Class: ', e[0])
            print('Error Message: ', e[1])
            print('Error Traceback: ', traceback.format_tb(e[2]))
            f.write('Error Return Type:{}\n'.format(type(e)))
            f.write('Error Class::{}\n'.format(e[0]))
            f.write('Error Message::{}\n'.format(e[0]))
            f.write('Error Traceback::{}\n'.format(traceback.format_tb(e[2])))
            f.close()

    f.close()