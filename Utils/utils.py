# Auteur   : Küenzi Jean-Daniel
# Desc.    :
# Date     : 12.02.2019

from math import isclose
import numpy as np
from City.city import City

def read_file(filename):
    cities = []
    with open(filename, 'r') as file:
        for line in file:
            x, y = map(float, line.strip().split(','))
            cities.append(City(x, y))
    return cities

def generate_distance_matrix(cities):
    n = len(cities)
    coords = np.array([(city.x, city.y) for city in cities])
    distance_matrix = np.zeros((n, n))
    
    for i in range(n):
        for j in range(i + 1, n):
            distance = np.linalg.norm(coords[i] - coords[j])
            distance_matrix[i,j] = distance
            distance_matrix[j,i] = distance  # Symmetry
    
    return distance_matrix

def compare_floats(a, b, epsilon=1e-10):
    if isclose(a, b, abs_tol=epsilon):
        return 0
    elif a < b:
        return -1
    else:
        return 1