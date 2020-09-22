from __future__ import annotations

import math
from typing import List
from signal import signal, SIGINT

from species import Specie, recombine, evolve
from util import random_pairs

# N - species count, L - genotype length,
# R - recombination, M - mutation,
# p - probability, c - count.
N = 30
L = 300
Rp = .99
Mp = .3
Mc = 2 * round(math.log2(L))


def best_in(population: List[Specie]) -> Specie:
    solution = population[0]
    for specie in population:
        if specie.fitness > solution.fitness:
            solution = specie
    return solution


def is_good_enough(solution: Specie) -> bool:
    return False
    # return solution.fitness >= 10


solutions = []


def conclude(signum, frame):
    print('\r', end='')
    if not solutions:
        print('No solutions has been found yet.')
    else:
        solution = best_in(solutions)
        print(f'{len(solutions)}! {round(solution.fitness, 4)}')
        print(solution.genotype)
    exit(0)


signal(SIGINT, conclude)

population = [Specie.poor(L) for _ in range(N)]
solution = best_in(population)
solutions.append(solution)

while not is_good_enough(solution):
    print(f'{len(solutions)}. {round(solution.fitness, 4)}')

    younglings = []
    for pair in random_pairs(population):
        offspring = recombine(*pair, prob=Rp)
        if offspring:
            younglings.extend(offspring)

    for specie in younglings:
        specie.mutate(Mc, prob=Mp)

    population.extend(younglings)
    population = evolve(population, N)

    solution = best_in(population)
    solutions.append(solution)

conclude(0, 0)
