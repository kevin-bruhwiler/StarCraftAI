import cybw
from GA import genetic as genetic

import time

pool_size = 50
max_generations = 50
stale_species = 15

def evaluate(genome):
    """
    Build Order Genetic Algorithm Search Simulation
    """
    #TODO: THIS
    genome.fitness = 5 #seconds

#I want to use NEAT as my genetic algorithm..... not just basic GA shit
# I am using gentic algorithms to find the best build order between the start and goal.
# start is the current game state, goal is the desired game state determined by a NN.
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
        while self.GA.generation < 2:
            self.evaluate_population()
            self.GA.update_best_genome()
            self.GA.new_generation()
        self.optimal_build_order = self.GA.best_genome

        print('Total elapsed time: ' + str(time.time() - start_time))

    def evaluate_population(self):
        for species in self.GA.species:
            for genome in species.genomes:
                evaluate(genome)

# test code
GA_search = BOGASS(start={cybw.UnitTypes.Terran_SCV: 5, cybw.UnitTypes.Terran_Command_Center: 1},
            goal={cybw.UnitTypes.Terran_Command_Center: 2,
            cybw.UnitTypes.Terran_Engineering_Bay: 1})

GA_search.find_optimal_build_order()

