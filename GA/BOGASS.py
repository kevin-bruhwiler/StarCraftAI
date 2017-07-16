import cybw

from GA import genetic as genetic

pool_size = 500
max_generations = 100
stale_species = 15

def evaluate(genome):
    """
    Build Order Genetic Algorithm Search Simulation
    """

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
        while self.GA.generation < 100:
            self.evaluate_population()
            self.GA.new_generation()
        self.optimal_build_order = self.GA.best_genome

    def evaluate_population(self):
        for species in self.GA.species:
            for genome in species.genomes:
                evaluate(genome)


# test code
GA_search = BOGASS(start={cybw.UnitTypes.Protoss_Probe: 5, cybw.UnitTypes.Protoss_Nexus: 1},
            goal={cybw.UnitTypes.Protoss_Nexus: 2,
            cybw.UnitTypes.Protoss_Gateway: 2,
            cybw.UnitTypes.Protoss_Stargate: 1})

GA_search.find_optimal_build_order()

