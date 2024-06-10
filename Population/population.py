# Auteur   : Küenzi Jean-Daniel
# Desc.    :
# Date     : 12.02.2019

from math import ceil
import random
from Individual.individual import Individual

class Population:
    def __init__(self, distance_matrix, population_size, tournament_size, elite_rate, crossover_rate, mutation_rate):
        self.generation = 0
        self.individuals = []
        self.distance_matrix = distance_matrix
        self.population_size = population_size
        self.tournament_size = tournament_size
        self.elite_rate = elite_rate
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.nb_elite = ceil(self.elite_rate * self.population_size)
        self.nb_child = self.population_size - self.nb_elite

    def generate_random_population(self):
        self.generation += 1
        while len(self.individuals) < self.population_size:
            new_individual = Individual(self.crossover_rate, self.mutation_rate)
            new_individual.generate_random_path(self.distance_matrix.shape[0])
            new_individual.calcul_total_distance(self.distance_matrix)
            
            if self.is_unique(self.individuals, new_individual):
                self.individuals.append(new_individual)
    
    def is_unique(self, individuals, other):
        for individual in individuals:
            if other == individual:
                return False
        return True
    
    def new_generation(self):
        self.generation += 1
        new_individuals = self.elitist_selection()
        for _i in range(self.nb_child//2):
            relative1 = self.select_parent()
            relative2 = self.select_parent()
            while relative1 == relative2:
                relative2 = self.select_parent()    
            child1 = relative1.reproduction(relative2)
            child2 = relative2.reproduction(relative1)
            new_individuals.append(child1)
            new_individuals.append(child2)
        self.individuals = new_individuals
    
    def mutation(self):
        for individual in self.individuals:
            individual.mutation()
    
    def select_parent(self):
        sub_population = random.sample(self.individuals, self.tournament_size)
        return min(sub_population, key=lambda individual: individual.total_distance)

    def evaluate_population(self):
        for individual in self.individuals:
            individual.calcul_total_distance(self.distance_matrix)

    def select_best_individual(self):
        return min(self.individuals, key=lambda individual: individual.total_distance)
    
    def elitist_selection(self):
        return sorted(self.individuals, key=lambda individual: individual.total_distance)[:self.nb_elite]