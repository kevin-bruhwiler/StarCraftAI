import cybw
from GA import genetic as genetic

import time

pool_size = 50
max_generations = 50
stale_species = 15

def evaluate(genome):
    """
    Compute the amount of time it takes to complete the build order
    """
    #TODO: THIS
    genome.fitness = 5 #seconds

class BOGASS:
    """
    Build Order Genetic Algorithm Search Simulation
    """
    def __init__(self, start=None, goal=None):
        """
        :type start: dict
        :type start: dict
        """
        self.GA = genetic.Pool(start=start, goal=goal, size=pool_size, stale_species=stale_species)
        self.optimal_build_order = None


    def find_optimal_build_order(self):
        print('Training {} genomes for {} generations.'.format(pool_size, max_generations))
        start_time = time.time()
        while self.GA.generation < 15:
            self.evaluate_population()
            self.GA.update_best_genome()
            self.GA.new_generation()
        self.optimal_build_order = self.GA.best_genome
        print('Best build order: ' + str(self.GA.best_genome.build_order))
        print('Total elapsed time: ' + str(time.time() - start_time))

    def evaluate_population(self):
        for species in self.GA.species:
            for genome in species.genomes:
                evaluate(genome)
