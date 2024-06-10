# Auteur   : Küenzi Jean-Daniel
# Desc.    : Main program
# Date     : 12.02.2019

import math
import sys

from matplotlib import pyplot as plt

from Population.population import Population
from Solution.solution import Solution
from Utils.utils import compare_floats, generate_distance_matrix, read_file

def plot_solution(cities, solution):
    x_coords = [cities[i].x for i in solution.individual.path]
    y_coords = [cities[i].y for i in solution.individual.path]
    x_coords.append(cities[solution.individual.path[0]].x)
    y_coords.append(cities[solution.individual.path[0]].y)

    plt.figure(figsize=(10, 6))
    plt.plot(x_coords, y_coords, 'o-', markersize=8, linewidth=2, label='Chemin')
    plt.scatter(x_coords, y_coords, c='red')

    for i, city in enumerate(cities):
        plt.text(city.x, city.y, str(i), fontsize=12, ha='right')

    plt.fill_between(x_coords, y_coords, color='lightblue', alpha=0.5)

    plt.suptitle('Travelling Salesman Problem')
    plt.title('Generation #{:d} - Total distance : {:.5f}'.format(solution.generation, solution.individual.total_distance))
    plt.xlabel('X')
    plt.ylabel('Y')
    plt.legend()
    plt.show()

if __name__ == '__main__':
    if (len(sys.argv) < 9):
        print('Command is : main.py <file_path> <population_size> <tournament_size> <elite_percent> <crossover_rate> <mutation_rate> <stagnation_limit> <generation_limit>')
        print('Ex: python main.py Data/average.tsp.raw 500 5 0.02 0.45 0.02 50 1000')
        exit(0)

    filename = sys.argv[1]
    population_size = int(sys.argv[2])
    tournament_size = int(sys.argv[3])
    elite_rate = float(sys.argv[4])
    crossover_rate = float(sys.argv[5])
    mutation_rate = float(sys.argv[6])
    stagnation_limit = int(sys.argv[7])
    generation_limit = int(sys.argv[8])

    cities = read_file(filename)
    distance_matrix = generate_distance_matrix(cities)

    nb_permutation = math.factorial(distance_matrix.shape[0]-1)//2
    if (population_size > nb_permutation):
        print('Careful your population size is greater than the number of unique possibilities ({:.0f})'.format(nb_permutation))
        exit(0)

    population = Population(distance_matrix, population_size, tournament_size, elite_rate, crossover_rate, mutation_rate)
    population.generate_random_population()

    stagnation = 0
    final_solution = Solution()
    print('Searching best path ...')
    while (stagnation < stagnation_limit and population.generation < generation_limit):
        population.evaluate_population()
        new_best_individual = population.select_best_individual()
        if final_solution.individual is None or compare_floats(new_best_individual.total_distance, final_solution.individual.total_distance) == -1:
            final_solution.individual = new_best_individual
            final_solution.generation = population.generation
            print(final_solution)
            stagnation = 0
        else:
            stagnation += 1
        population.new_generation()
        population.mutation()
    print('End searching')
    print('Final solution : {:s}'.format(str(final_solution)))

    plot_solution(cities, final_solution)