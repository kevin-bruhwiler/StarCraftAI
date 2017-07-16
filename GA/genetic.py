import logging
import math
import random
from copy import deepcopy

from GA import genome as genome

def mutation_rates():
    return {}

def convert_to_minimum_architecture(start, goal):
    difference = []
    for key, value in goal.items():
        if key not in start.keys():
            difference.append([key, value])
        else:
            difference.append([key, value])
    print(difference)


class Pool(object):
    """
    :type species: list[Species]
    :type best_genome: ml.genome.Genome
    """
    def __init__(self, start=None, goal=None, size=5000, stale_species=15):
        self.genes = []
        self.minimum_architecture = convert_to_minimum_architecture(start, goal)
        self.species = []
        self.generation = 0
        self.max_fitness = -1
        self.mutation_rates = mutation_rates()
        self.best_genome = None
        self.population = size
        self.stale_species = stale_species

        self.init_pool()

    def total_average_fitness(self):
        """
        Compute the total average fitness (sum of all species' average fitness)
        """
        total = 0
        for species in self.species:
            total += species.average_fitness
        return total

    def cull_species(self, cull_to_one):
        """
        Kill the bottom have of the genomes in every species
        :param cull_to_one: kill every genome in all species except the top one per species
        """
        for species in self.species:
            species.genomes.sort(key=lambda genome: genome.fitness, reverse=True)
            remaining = math.ceil(len(species.genomes) / 2)
            if cull_to_one:
                remaining = 1
            while len(species.genomes) > remaining:
                species.genomes.pop()

    def remove_stale_species(self):
        """
        If a species' top fitness has not improved for more generations that self.stale_species, remove the species and
        all of its genomes from pool.
        """
        survived = []
        for species in self.species:
            species.update_staleness()
            if species.staleness < self.stale_species or species.top_fitness >= self.max_fitness:
                survived.append(species)
        self.species = survived

    def remove_weak_species(self):
        """
        If a species is deemed "weak", remove the species and all of its genomes from the pool.
        """
        survived = []
        total = self.total_average_fitness()
        for species in self.species:
            breed = math.floor((species.average_fitness / total) * self.population)
            if breed >= 1:
                survived.append(species)
        self.species = survived

    def add_to_species(self, child):
        """
        Check to see if child belongs to any current species, if it does, add it. If not, make a new species and add
        it to the new species.
        :type child: genome
        """
        found_species = False
        if len(self.species) == 0:
            child_species = Species(self.mutation_rates)
            child_species.genomes.append(child)
            self.species.append(child_species)
            return
        for species in self.species:
            if not found_species and same_species(child, species.genomes[0]):
                species.genomes.append(child)
                found_species = True
        if not found_species:
            child_species = Species(self.mutation_rates)
            child_species.genomes.append(child)
            self.species.append(child_species)

    def rank_globally(self):
        """
        Ranks every genome in the pool according to its fitness
        """
        all_genomes = []
        for species in self.species:
            for g in species.genomes:
                all_genomes.append(g)

        all_genomes.sort(key=lambda g: g.fitness, reverse=True)

        i = 0
        for g in all_genomes:
            g.global_rank = i
            i += 1

    def new_generation(self):
        """
        Steps:
        1. Remove the bottom half of each speices
        2. Remove stale species (species that haven't improved in several generations)
        3. Rank each genome according to its fitness
        4. Remove species that are under performing
        5. Add children to each species according to that species' average fitness.
            The more fit the species, the more children the species receives.
        6. Remove all but the top individual per species
        7. Add the children to their appropriate species, as outline in add_too_species()
        """
        logging.info('Best accuracy: {}%'.format(self.best_genome.fitness*100.))
        logging.info('Making a new generation...')
        self.cull_species(False)
        self.remove_stale_species()
        self.rank_globally()
        for species in self.species:
            species.calculate_average_fitness()
        self.remove_weak_species()
        total = self.total_average_fitness()
        children = []
        for species in self.species:
            breed = math.floor(species.average_fitness / total * self.population) - 1
            for j in range(0, int(breed)):
                child = self.breed(species)
                children.append(child)

        self.cull_species(True)

        while len(children) + len(self.species) < self.population:
            random_species = random.choice(self.species)
            child = self.breed(random_species)
            children.append(child)

        for child in children:
            self.add_to_species(child)
        self.generation += 1

    def init_pool(self):
        """
        Declare a minimum architectue, create the population by mutating the minimum architecture, and add the generated
        individuals to species according to their architecture
        """
        for i in range(0, self.population):
            g = genome.Genome(self.mutation_rates, genes=deepcopy(self.minimum_architecture))
            self.mutate(g)
            self.add_to_species(g)

    def mutate(self, g):
        """
        Mutate genome, check to see if the new gene is unique to the pool's gene pool.
            If True: keep the new innovation number the gene received upon creation
            If False: change the new gene's innovation number to the innovation number of the gene is resembles in the
                gene pool
        :type g: genome
        """
        g.mutate()
        # check to see if a new gene emerged
        found_gene = False
        for g1 in g.genes:
            for g2 in self.genes:
                if g1.equals(g2):
                    # since they are the same gene, they need to have the same innovation number
                    g1.innovation = g2.innovation
                    found_gene = True
            # if g1 is unique, add it to the gene pool
            if not found_gene:
                self.genes.append(g1)
            found_gene = False

    def breed(self, species) -> genome:
        """
        Choose a random genome from species, mutate it, and return the mutated child
        :type species: Species
        """
        g = random.choice(species.genomes)
        child = g.copy_genome(self.mutation_rates)
        self.mutate(child)

        return child


class Species(object):
    """
    :type genomes: list[genome]
    """

    def __init__(self, mutation_rates):
        self.top_fitness = 0
        self.staleness = 0
        self.genomes = []
        self.average_fitness = 0
        self.mutation_rates = mutation_rates

    def calculate_average_fitness(self):
        """
        Calculate the average fitness for all genomes in self.genomes
        """
        total = 0
        for g in self.genomes:
            total += g.fitness
        self.average_fitness = total / len(self.genomes)

    def breed(self) -> genome:
        """
        Choose a random genome, mutate it, and return it
        """
        child = random.choice(self.genomes).copy_genome(self.mutation_rates)
        child.mutate()
        return child

    def update_staleness(self):
        """
        Choose a random genome, mutate it, and return it
        """
        self.genomes.sort(key=lambda g: g.fitness, reverse=True)
        if self.genomes[0].fitness > self.top_fitness:
            self.top_fitness = self.genomes[0].fitness
            self.staleness = 0
        else:
            self.staleness += 1

def same_species(g1, g2):
    """
    :type g1: genome
    :type g2: genome
    """
    dd = 2 * disjoint(g1.genes, g2.genes)
    return dd < 1


def disjoint(g1, g2):
    i1 = []
    for gene in g1:
        i1.append(gene.innovation)

    i2 = []
    for gene in g2:
        i2.append(gene.innovation)

    disjoint_genes = len(list(set(i1) - set(i2)))

    n = max(len(g1), len(g2))
    return disjoint_genes / n