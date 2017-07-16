import random
import string
from copy import deepcopy

def mutation_rates():
    return {}

def generate_genome_name():
    return ''.join(random.choice(string.ascii_lowercase) for x in range(20))

class Gene(object):
    def __init__(self, previous_unit=None, unit=None, proceeding_unit=None):
        self.previous_unit = previous_unit
        self.proceeding_unit = proceeding_unit
        self.unit = unit
        self.innovation = 0

    def __eq__(self, other):
        if type(self.previous_unit) == type(other.previous_unit) and type(self.proceeding_unit) == type(other.proceeding_unit) and type(self.unit) == type(other.unit):
            return self.previous_unit == other.previous_unit and self.proceeding_unit == other.proceeding_unit and self.unit == other.unit
        return False


class Genome(object):
    def __init__(self, build_order, start=None):
        """
        Initializes the genome with constant mutation rates
        :param genes: the set of genes this genome will be prepopulated with
        """
        self.full_id = generate_genome_name()
        self.build_order = build_order
        self.genes = []
        self.start = start

        self.fitness = -1
        self.adjusted_fitness = 0
        self.global_rank = 0

        self.mutation_rates = mutation_rates()

    def mutate(self):
        """
        Randomly apply mutations to this genome.
        """
        print(self.start)
        self.inject_mineral_worker()
        #self.inject_gas_worker()
        self.make_genes()
        pass

    def inject_mineral_worker(self):
        worker  = self.build_order[0].getRace().getWorker()
        print(len(self.build_order))
        random_index = random.randint(0, len(self.build_order))

        # check to make sure there is supply for a worker at this index
        if self.enough_supply(worker, random_index):
        # check to see if there is room at the resource depot for this worker at this index

            self.build_order.insert(random_index, worker)

    def inject_gas_worker(self):
        worker  = self.build_order[0].getRace().getWorker()
        random_index = random.randrange(0, len(self.build_order))
        # check to make sure there is supply for a worker at this index

        # check to see if there is room at a geyser for this worker at this index
        self.build_order.insert(random_index, worker)

    def enough_supply(self, unit, index):
        supply = 0
        for unit, value in self.start.items():
            supply += (unit.supplyProvided() - unit.supplyRequired())*value
        for i in range(index):
            supply += self.build_order[i].supplyProvided() - self.build_order[i].supplyRequired()
        print(supply)
        return True

    def copy_genome(self):
        # type: (Genome) -> Genome
        new_genome = Genome(build_order=[])
        for gene in self.build_order:
            new_genome.build_order.append(deepcopy(gene))
        return new_genome

    def make_genes(self):
        for i in range(len(self.build_order)):
            if i == 0:
                gene = Gene(previous_unit=None,
                            unit=self.build_order[i],
                            proceeding_unit=self.build_order[i+1])
            elif i == len(self.build_order) - 1:
                gene = Gene(previous_unit=self.build_order[i - 1],
                            unit=self.build_order[i],
                            proceeding_unit=None)
            else:
                gene = Gene(previous_unit=self.build_order[i-1],
                            unit=self.build_order[i],
                            proceeding_unit=self.build_order[i+1])

            if gene not in self.genes:
                self.genes.append(gene)