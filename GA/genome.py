import cybw
import random
from copy import deepcopy

def mutation_rates():
    return {'create_worker': .9,
            'create_supply': .3,
            'swap': .05}

def build_requirements_met(start, build_order, required_units):
    for required_unit, required_amount in required_units.items():
        amount = 0
        if required_unit in start.keys():
            amount += start[required_unit]
        for unit in build_order:
            if unit == required_unit:
                amount += 1
        if amount < required_amount:
            return False
    return True

'''
example build order
9 Pylon
13 Gateway
14 Assimilator
16 Pylon
17 Cybernetics core

probe, probe, probe, probe, pylon,
probe, probe, probe, probe, gateway
probe, Assimilator
probe, probe, pylon
probe, Cybernetics core
  '''

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
        :param build_order: the build order this genome will be populated with
        :param start: the starting game state
        """
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
        if random.random() < self.mutation_rates['create_worker']:
            self.create_worker()

        if random.random() < self.mutation_rates['create_supply']:
            self.create_supply()

        if random.random() < self.mutation_rates['swap']:
            self.swap()

        print(self.build_order)
        self.make_genes()

    def create_worker(self):
        """
        Randomly inject a new SCV into the build order
        """
        random_index = random.randint(0, len(self.build_order)-1)

        # check to make sure there is supply for a worker at this index and
        # check to see if there is room at the resource depot for this worker at this index
        if self.enough_supply(cybw.UnitTypes.Terran_SCV, random_index):
            self.build_order.insert(random_index, cybw.UnitTypes.Terran_SCV)
        else:
            self.build_order.insert(random_index, cybw.UnitTypes.Terran_Supply_Depot)
            self.build_order.insert(random_index, cybw.UnitTypes.Terran_SCV)

    def create_supply(self):
        """
        Randomly inject a new supply depot into the build order
        """
        random_index = random.randint(0, len(self.build_order)-1)
        self.build_order.insert(random_index, cybw.UnitTypes.Terran_Supply_Depot)

    def swap(self):
        """
        Randomly swap two elements of the build order
        """
        random_a = None
        random_b = None
        while random_a == random_b:
            random_a = random.randint(0, len(self.build_order)-1)
            random_b = random.randint(0, len(self.build_order)-1)

        # check to make sure that the unit at [random_b] will have all the build requirments at [random_a].

        if  self.requirements_met(random_a, random_b):
            self.build_order[random_a], self.build_order[random_b] = self.build_order[random_b], self.build_order[random_a]

    def enough_supply(self, unit, index):
        """
        Check to see if there is enough supply for the unit at the index of the build order
        :param unit: the unit to be injected
        :param index: the index of the build order to inject the unit
        """
        remaining_supply = 0
        for unit, value in self.start.items():
            remaining_supply += (unit.supplyProvided() - unit.supplyRequired())*value
        for i in range(index):
            remaining_supply += self.build_order[i].supplyProvided() - self.build_order[i].supplyRequired()
        remaining_supply += unit.supplyProvided() - unit.supplyRequired()
        if remaining_supply < 0:
            return False
        return True

    def requirements_met(self, index_a, index_b):
        if index_a > index_b:
            index_a, index_b = index_b, index_a

        unit_b = self.build_order[index_b]

        return build_requirements_met(self.start, self.build_order[:index_a], unit_b.requiredUnits())


    def copy_genome(self):
        # type: (Genome) -> Genome
        new_genome = Genome(build_order=[])
        new_genome.start = self.start
        for command in self.build_order:
            new_genome.build_order.append(command)
        return new_genome

    def make_genes(self):
        self.genes.clear()
        for i in range(len(self.build_order)-1):
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