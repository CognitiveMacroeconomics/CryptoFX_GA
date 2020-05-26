# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:45:03 2020

@author: shamid
"""
from random import randint
import source

__all__ = ['Chromosome','Population']

start_exchange_currency = "USDT"
end_exchange_currency = "XLM"

class Chromosome:
    """
    This class id used to define a chromosome for the genetic algorithm
    simulation.
    
    This class is essentially nothing more than a container for the details of 
    the chromosome, namely the gene (the string that represents our target 
    string) and the fitness (how close the gene is to the target string).
    
    Note that this class is immutable. Calling mate()  or mutate() will result 
    in a new chromosome instance being created.
    """

    exchange_rate = 0
    chromosome_length = 0
    num_crypto = 0
    crypto_index = 0
    
    def __init__(self, gene):

        print("In init chromosome")
        self.gene = gene
        self.fitness = Chromosome.uptade_fitnesss(gene)
        pass
    
    def mate():
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        """
        
        pass
    
    def mutate():
        """
        Method used to generate a new chromosome based on a change in a random
        character in the geene of this chromosome. A new chormosome will be
        created, but this original will not be affected.
        """
        pass
    
    @staticmethod
    def uptade_fitnesss(gene):
        """
        Helper method used to return the fitness for the chromosome based on
        its gene.
        """
        
        print("Gene is: {}".format(gene))
        
        fitness = 99

        return fitness
    
    @staticmethod
    def gen_random():
        """
        A convenience mehtod for generating a random chromosome with a random
        gene.
        """
        print("In gen random")
        #print("Chromosome length is:{}".format(Chromosome.chromosome_length))
        #print("Number of crypto currencies are:{}".format(Chromosome.num_crypto))
        gene = []
        while len(gene) < (Chromosome.chromosome_length):
            num = randint(0, Chromosome.num_crypto - 1)
            if num not in gene:
                gene.append(num)
            
        #print("The gene is:{}".format(gene))
        
        return Chromosome(gene)
        pass
    

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
    def __init__(self, size=10, crossover=0.8, mutation=0.03):
        self.crossover = crossover
        self.mutation = mutation
 
        entire_population = []
        for i in range(size):
            entire_population.append(Chromosome.gen_random())
        
        print("The entire population is:")
        for single_chromosome in entire_population:
            print("{}\t{}".format(single_chromosome.gene, single_chromosome.fitness))
        pass
    
    def _tournament_selection():
        """
        A helper method used to select a random chromosome from the population
        using a tournament selection algorithm.
        """
        pass
    
    def _selectParents():
        """
        A helper method used to select two parents from the population using a
        tournament selection algorithm
        """
        pass
    
    def evolve():
        """
        Method to evolve the population of chromosomes.
        """
        pass

if __name__ == "__main__":
    
    maxGenerations = 5
    Chromosome.exchange_rate, Chromosome.crypto_index = source.main(start_exchange_currency,end_exchange_currency)
    Chromosome.chromosome_length = 4
    Chromosome.num_crypto = 7
    pop = Population(size=10, crossover=0.8, mutation=0.3)
