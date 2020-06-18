# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 09:45:03 2020

@author: shamid
"""
from random import randint, random, choice, sample
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
        
    
    def crossover_onepoint(self, mate):
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        One Point Crossover
        """
        pivot = randint(0, len(self.chromosome) - 1)
        chromosome1_temp = self.chromosome[:pivot] + mate.chromosome[pivot:]
        chromosome1 = []
        for i in range(len(chromosome1_temp)):
            while chromosome1_temp.count(chromosome1_temp[i])>1 and i >= pivot:
                print("Here1:{}".format(chromosome1_temp[i]))
                gene = randint(0, Chromosomes.num_crypto - 1)
                print("Changed to:{}".format(gene))
                chromosome1_temp[i] = gene
            chromosome1.append(chromosome1_temp[i])
            
        chromosome2_temp = mate.chromosome[:pivot] + self.chromosome[pivot:]
        chromosome2 = []
        for i in range(len(chromosome2_temp)):
            while chromosome2_temp.count(chromosome2_temp[i])>1 and i >= pivot:
                print("Here2:{}".format(chromosome2_temp[i]))
                gene = randint(0, Chromosomes.num_crypto - 1)
                print("Changed to:{}".format(gene))
                chromosome2_temp[i] = gene
            chromosome2.append(chromosome2_temp[i])

        return Chromosomes(chromosome1), Chromosomes(chromosome2)
    
    def crossover_ord1(self, mate):
        """
        Method used to mate the chromosome with another chromosome,
        resulting in a new chromosome being returned.
        Order One Crossover
        """
        p1 = self.chromosome
        p2 = mate.chromosome
        
        size = len(p1)
        r1, r2 = sample(range(size), 2)
        if r1 > r2:
            r1, r2 = r2, r1
    
            
        offspring1 = [-1] * size
        print("r1:{}\tr2:{}".format(r1,r2))
        for i in range(r1 ,r2+1):
            offspring1[i] = p1[i]
            
        #print("child 1 is:{}".format(child1))
        
        
        p2_rotate = p2[r2+1:]+p2[:r2+1]
        #print("P2 rotate is:{}".format(p2_rotate))
        
        temp1 = [0] * (size-(r2-r1)-1) 
        j = 0
        for i in range(size):
            if p2_rotate[i] not in offspring1:
                temp1[j] = p2_rotate[i]
                j += 1
            if j == len(temp1):
                break
            
        print("temp is:{}".format(temp1))
        for i in range(len(temp1)):
            idx = (r2 + i + 1) % size
            offspring1[idx] = temp1[i]
            
        print("Offspring1 is:{}".format(offspring1))
        
        offspring2 = [-1] * size
        for i in range(r1, r2+1):
            offspring2[i] = p2[i]
            
                
        p1_rotate = p1[r2+1:]+p1[:r2+1]
        
        temp2 = [0] * (size-(r2-r1)-1)
        j = 0
        for i in range(size):
            if p1_rotate[i] not in offspring2:
                temp2[j] = p1_rotate[i]
                j += 1
            if j == len(temp2):
                break
                
        for i in range(len(temp2)):
            idx = (r2 + i + 1) % size
            offspring2[idx] = temp2[i]
            
        print("Offspring2 is:{}".format(offspring2))
        
        return Chromosomes(offspring1), Chromosomes(offspring2)
    
    def mutate(self):
        """
        Method used to generate a new chromosome based on a change in a random
        character in the geene of this chromosome. A new chormosome will be
        created, but this original will not be affected.
        """
#        print("In mutation funtion")
       
        genes = list(self.chromosome)
#        print("Genes are:{}".format(genes))

#        print("New gene is:{}".format(new_gene))
        idx = randint(0, len(genes) - 1)
        new_gene = randint(0, Chromosomes.num_crypto - 1)
        while new_gene == genes[idx]:
            new_gene = randint(0, Chromosomes.num_crypto - 1)
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
            if value == Chromosomes.start_exchange_currency:
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
#                print("{} to {} is: {}".format(Chromosomes.start_exchange_currency, Chromosomes.crypto_index[chromosome[i]],\
#                                                  Chromosomes.exchange_rate_matrix[0][start_ex_idx][chromosome[i]]))
                value = Chromosomes.exchange_rate_matrix[0][start_ex_idx][chromosome[i]]
                
            elif i == len(chromosome):
#                print("{} to {} is : {}".format(Chromosomes.crypto_index[chromosome[i-1]],Chromosomes.end_exchange_currency,\
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
            if gene not in chromosome:
                chromosome.append(gene)
            
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
    # The tournament size for parent selection
    tournamnet_size = 0
    
    # Number of offsprings to be generated
    num_offsprings = 0
    
    def __init__(self, size=10, crossover=0.8, mutation=0.3):
        """
        Constructor for the class
        initializes the probabbility of crossover and the probablility of 
        mutation and the size of the population
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
        print("The entire population is:")
        for chromo in self.entire_population:
            print("{}\t{}".format(chromo.chromosome,
                                  chromo.fitness))
        
    
    def tournament_selection(self):
        """
        A helper method used to select a random chromosome from the population
        using a tournament selection algorithm.
        
        """
        best = choice(self.entire_population)
        
        #print("Best is:{} \t {}".format(best.chromosome, best.fitness))
        
        for i in range(Population.tournamnetSize):
            cont = choice(self.entire_population)
            #print("cont is:{} \t {}".format(cont.chromosome, cont.fitness))
            if(cont.fitness > best.fitness):
                best = cont
        #print("Best is:{} \t {}".format(best.chromosome, best.fitness))
        return best 
    
    def selectParents(self):
        """
        A helper method used to select two parents from the population using a
        tournament selection algorithm
        """
#        print("In select Parent")
        return (self.tournament_selection(), self.tournament_selection())
    
    def evolve(self):
        """
        Method to evolve the population of chromosomes.
        """
#        print("In Population evolve")
        #len(self.entire_population)/2
#        buf = sorted(self.entire_population[:8], key=lambda x: x.fitness)
        old_population = self.entire_population[:len(self.entire_population)-self.num_offsprings]
#        for i in range(len(old_population)):
#            print("{}".format(old_population[i].chromosome))
        
        buf = []
        
        i = 0
        while i <  self.num_offsprings/2: #size:
            if random() <= self.crossover:
                (p1, p2) = self.selectParents()
                print("P1 is:\n{}\t{}".format(p1.chromosome, p1.fitness))
                print("P2 is:\n{}\t{}".format(p2.chromosome, p2.fitness))
                offspring_crossover = p1.crossover_ord1(p2)
                print("The off-springs are:")
                for child in offspring_crossover:
                    print("{}\t{}".format(child.chromosome, child.fitness))
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
        print("New Population")
        for pop in self.entire_population:
            print("{}\t{}".format(pop.chromosome, pop.fitness))
            
        
        pass

if __name__ == "__main__":
    
    # Pure Crypto: 
    #   Start Currency: ADA
    #   End Currency: ZEC
    #   Intermerdiate Currency: BTC
    
    # Stable Crypto:
    #   Start Currency: 
    #   End Currency: 
    #   Intermerdiate Currency:       
    
    # Pure-Stable Crypto:
    #   Start Currency: 
    #   End Currency: 
    #   Intermerdiate Currency:       
    
    # Set the Start Crypto Currency
    start_crypto_currency = "ADA"
    
    # Set the End Crypto Currency
    end_crypto_currency = "ZEC"
    
    # Set the Intermediate Crypto Currency
    intermediate_currency = "BTC"
    
    # Set the number of generations to run the GA
    max_generations = 1
    
    # Call main() from source.py to read the files an extarct the exchnage
    # rates. 
    # source.main() returns the exchange rate matrix and the the index of the
    # crypto currencies. 
    Chromosomes.exchange_rate_matrix, Chromosomes.crypto_index = source.main(
                                                    start_crypto_currency,
                                                    end_crypto_currency,
                                                    intermediate_currency)
    # Set the length of the chromosome
    Chromosomes.chromosome_length = 7
    
    # Set the num of crypto currencie:
    # Pure Crypto: 34
    # Stable Crypto: 
    # Pure-Stable Crypto:
    Chromosomes.num_crypto = 34
    
    # Set the start exchange currency
    Chromosomes.start_exchange_currency = "USD"
    
    # Set the end exchange currency
    Chromosomes.end_exchange_currency = "USD"
    
    # Set the transaction cost:
    # Transaction cost in {1, 5, 10, 15}
    Chromosomes.transaction_cost = 1 * 0.05 # {1, 5, 10, 15}
    
    # Set the tournament size for parent selection
    Population.tournamnet_size = 3
    
    # Set the number of offsprings to be generated
    Population.num_offsprings = 2
    
    # Create the Population object
    # Set the population size
    # Set the probability of crossover
    # Set the probability of mutation
    pop = Population(size = 8, crossover = 0.8, mutation = 0.3)
    
    # Run the optimization procedure for max_generations number of generations
    for i in range(1, max_generations + 1):
        
        print("Generation: {}".format(i))
        
        # Print the top most chromosome in the population
        print("{}\t{}".format(pop.entire_population[0].chromosome,
                              pop.entire_population[0].fitness))
        
        # Start evolving the population
        pop.evolve()
