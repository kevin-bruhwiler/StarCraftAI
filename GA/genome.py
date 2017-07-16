import random
import string
from copy import deepcopy


def generate_layer_name():
    return ''.join(random.choice(string.ascii_lowercase) for x in range(20))


class Genome(object):
    def __init__(self, mutation_rates, genes):
        """
        Initializes the genome with constant mutation rates
        :param genes: the set of genes this genome will be prepopulated with
        """
        self.full_id = None
        self.genes = genes

        self.fitness = -1
        self.adjusted_fitness = 0
        self.global_rank = 0

        self.mutation_rates = mutation_rates

    def mutate(self):
        """
        Randomly apply mutations to this genome.
        """
        pass

    def copy_genome(self, mutation_rates: dict):
        # type: (Genome) -> Genome
        new_genome = Genome(mutation_rates, genes=[])
        for gene in self.genes:
            new_genome.genes.append(deepcopy(gene))
        return new_genome