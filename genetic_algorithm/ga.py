# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:45:03 2020

@author: shamid
"""
from random import randint, random, choice 
import source

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

    exchange_rate_matrix = 0
    chromosome_length = 0
    num_crypto = 0
    crypto_index = {}
    start_exchnage_currency = "USD"
    end_exchnage_currency = "USD"
    transaction_cost = 1 * 0.05 # {1, 5, 10, 15}
    
    def __init__(self, chromosome):

#        print("In init Chromosomes")
        self.chromosome = chromosome
        self.fitness = Chromosomes.uptade_fitnesss(chromosome)
        
    
    def crossover(self, mate):
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        One Point Crossover
        """
        pivot = randint(0, len(self.chromosome) - 1)
        chromosome1 = self.chromosome[:pivot] + mate.chromosome[pivot:]
        chromosome2 = mate.chromosome[:pivot] + self.chromosome[pivot:]

        return Chromosomes(chromosome1), Chromosomes(chromosome2)
    
    def mutate(self):
        """
        Method used to generate a new chromosome based on a change in a random
        character in the geene of this chromosome. A new chormosome will be
        created, but this original will not be affected.
        """
#        print("In mutation funtion")
       
        genes = list(self.chromosome)
#        print("Genes are:{}".format(genes))
        new_gene = randint(0, Chromosomes.num_crypto - 1)
#        print("New gene is:{}".format(new_gene))
        idx = randint(0, len(genes) - 1)
#        print("The index is :{}".format(idx))
        genes[idx] = new_gene

        return Chromosomes(genes)
        
        
                
    
    @staticmethod
    def uptade_fitnesss(chromosome):
        """
        Helper method used to return the fitness for the chromosome based on
        its gene.
        """
        
#        print("Chromosome is: {}".format(chromosome))
        
        #print("Excnahge rate matrix is:\n{}".format(Chromosome.exchange_rate_matrix))
        
        # key for key, value in dict.items() if value == 1
        
#        start_ex_idx = key for key, value in Chromosome.crypto_index.items() if value == "USD"
#        end_ex_idx = key for key, value in Chromosome.crypto_index.items() if value == "USD"
        
        for key, value in Chromosomes.crypto_index.items():
            #print("{} :{}".format(key,value))
            if value == Chromosomes.start_exchnage_currency:
                start_ex_idx = key
                
#                print("{} is at {}".format(value, start_ex_idx))
                
            if value == Chromosomes.end_exchnage_currency:
                end_ex_idx = key
#                print("{} is at {}".format(value, end_ex_idx))
                
        
        fitness = 1
        
        for i in range(len(chromosome)+1):
            
#            if(i != len(gene)):
#                print("{}\t{}".format(gene[i], Chromosome.crypto_index[gene[i]]))
            value = 0
            #print("I is: {}".format(i))
            if i == 0:
#                print("{} to {} is: {}".format(Chromosomes.start_exchnage_currency, Chromosomes.crypto_index[chromosome[i]],\
#                                                  Chromosomes.exchange_rate_matrix[0][start_ex_idx][chromosome[i]]))
                value = Chromosomes.exchange_rate_matrix[0][start_ex_idx][chromosome[i]]
                
            elif i == len(chromosome):
#                print("{} to {} is : {}".format(Chromosomes.crypto_index[chromosome[i-1]],Chromosomes.end_exchnage_currency,\
#                                                  Chromosomes.exchange_rate_matrix[0][chromosome[i-1]][end_ex_idx]))
                value = Chromosomes.exchange_rate_matrix[0][chromosome[i-1]][end_ex_idx]
                
            else:
#                 print("{} to {} is : {}".format(Chromosomes.crypto_index[chromosome[i-1]],Chromosomes.crypto_index[chromosome[i]],\
#                                                   Chromosomes.exchange_rate_matrix[0][chromosome[i-1]][chromosome[i]]))
                 value = Chromosomes.exchange_rate_matrix[0][chromosome[i-1]][chromosome[i]]
                                  
            fitness *= ((value) - (value * Chromosomes.transaction_cost))

        return fitness
    
    @staticmethod
    def gen_random():
        """
        A convenience mehtod for generating a random chromosome with a random
        gene.
        """
#        print("In gen random")
        #print("Chromosome length is:{}".format(Chromosome.chromosome_length))
        #print("Number of crypto currencies are:{}".format(Chromosome.num_crypto))
        chromosome = []
        while len(chromosome) < (Chromosomes.chromosome_length):
            gene = randint(0, Chromosomes.num_crypto - 1)
            chromosome.append(gene)
#            if gene not in chromosome:
#                chromosome.append(gene)
            
        #print("The gene is:{}".format(gene))
        
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
    _tournamnetSize = 3
    _num_offsprings = 100
    
    def __init__(self, size=10, crossover=1, mutation=1):
        self.crossover = crossover
        self.mutation = mutation
 
        buf = []
        
        for i in range(size):
            buf.append(Chromosomes.gen_random())
            
            
        self.entire_population = list(sorted(buf[:size], key=lambda x: x.fitness, reverse=True))
        
#        print("The entire population is:")
#        for single_chromosome in self.entire_population:
#            print("{}\t{}".format(single_chromosome.chromosome, single_chromosome.fitness))
        
    
    def _tournament_selection(self):
        """
        A helper method used to select a random chromosome from the population
        using a tournament selection algorithm.
        
        """
        best = choice(self.entire_population)
        
        #print("Best is:{} \t {}".format(best.chromosome, best.fitness))
        
        for i in range(Population._tournamnetSize):
            cont = choice(self.entire_population)
            #print("cont is:{} \t {}".format(cont.chromosome, cont.fitness))
            if(cont.fitness > best.fitness):
                best = cont
        #print("Best is:{} \t {}".format(best.chromosome, best.fitness))
        return best 
    
    def _selectParents(self):
        """
        A helper method used to select two parents from the population using a
        tournament selection algorithm
        """
#        print("In select Parent")
        return (self._tournament_selection(), self._tournament_selection())
    
    def evolve(self):
        """
        Method to evolve the population of chromosomes.
        """
#        print("In Population evolve")
        #len(self.entire_population)/2
#        buf = sorted(self.entire_population[:8], key=lambda x: x.fitness)
        old_population = self.entire_population[:len(self.entire_population)-self._num_offsprings]
#        for i in range(len(old_population)):
#            print("{}".format(old_population[i].chromosome))
        
        buf = []
        
        i = 0
        while i <  self._num_offsprings/2: #size:
            if random() <= self.crossover:
                (p1, p2) = self._selectParents()
                #print("P1 is:\n{}".format(p1.chromosome))
                #print("P2 is:\n{}".format(p2.chromosome))
                offspring_crossover = p1.crossover(p2)
                #print("The off-springs are:")
                #for child in offspring_crossover:
                    #print("{}\t{}".format(child.chromosome, child.fitness))
                for offspring in offspring_crossover:
                    if random() <= self.mutation:
                        mutated_offspring = offspring.mutate()
                        buf.append(mutated_offspring)
#                        print("Mutated offspring is:{}".format(mutated_offspring.chromosome))
                    else:
                        buf.append(offspring)
        
                i += 1
        entire_population_temp = old_population + buf
        self.entire_population = list(sorted(entire_population_temp[:], key=lambda x: x.fitness, reverse = True))
#        for pop in self.entire_population:
#            print("{}\t{}".format(pop.chromosome, pop.fitness))
            
        
        pass

if __name__ == "__main__":
    
    """Pure Crypto: ADA
                    ZEC
    """
    start_crypto_currency = "ADA"
    end_crypto_currency = "ZEC"
    
    maxGenerations = 20000
    Chromosomes.exchange_rate_matrix, Chromosomes.crypto_index = source.main(start_crypto_currency,end_crypto_currency)
    
    Chromosomes.chromosome_length = 5
    Chromosomes.num_crypto = 34
    pop = Population(size = 2000, crossover = 0.8, mutation = 0.2)
    
    for i in range(1, maxGenerations + 1):
        print("Generation: {}".format(i))
        print("{}\t{}".format(pop.entire_population[0].chromosome, pop.entire_population[0].fitness))
        pop.evolve()
