# Auteur   : Küenzi Jean-Daniel
# Desc.    : Individual represent one solution in our population
# Date     : 12.02.2019

from math import ceil
import random

from Utils.utils import compare_floats

class Individual:
    def __init__(self, crossover_rate, mutation_rate):
        self.path = []
        self.total_distance = 0.0
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate

    def generate_random_path(self, nb_cities):
        cities_index = list(range(nb_cities))
        random.shuffle(cities_index)
        self.path = cities_index

    def calcul_total_distance(self, distance_matrix):
        self.total_distance = sum(distance_matrix[self.path[i],self.path[i+1]] for i in range(len(self.path)-1))
        self.total_distance += distance_matrix[self.path[0],self.path[-1]]

    def reproduction(self, other):
        path_len = len(self.path)

        child = Individual(self.crossover_rate, self.mutation_rate)
        child.path = [None] * path_len

        for i in random.sample(range(path_len), ceil(self.crossover_rate * path_len)):
            child.path[i] = self.path[i]

        j = 0
        for i in range(path_len):
            if child.path[i] is None:
                while other.path[j] in child.path:
                    j += 1
                child.path[i] = other.path[j]
                j += 1

        return child
    
    def mutation(self):
        p = random.random()
        if p <= self.mutation_rate:
            i1, i2 = random.sample(range(len(self.path)), 2)
            self.path[i1], self.path[i2] = self.path[i2], self.path[i1]
    
    def __eq__(self, other):
        return compare_floats(self.total_distance, other.total_distance) == 0

    def __str__(self):
        individual_str = 'path: [' + ' '.join(map(str, self.path)) + ']'
        return individual_str + ' - distance: {:.5f}'.format(self.total_distance)
