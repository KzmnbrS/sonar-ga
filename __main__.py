from __future__ import annotations

import os
import math
from typing import List
from signal import signal, SIGINT

import plotly.express as px

from species import Specie, recombine, evaluate
from util import random_pairs

# N - species count, L - genotype length,
# R - recombination, M - mutation,
# p - probability, c - count.
N = 70
L = 32
Rp = .99
Mp = .3
Mc = 2 * round(math.log2(L))


def compute_average_fitness(population: List[Specie]) -> float:
    return sum(specie.fitness for specie in population) / len(population)


def best_in(population: List[Specie]) -> int:
    best = 0
    for i in range(len(population)):
        if population[i].fitness > population[best].fitness:
            best = i
    return best


def is_good_enough(solution: Specie) -> bool:
    return solution.fitness >= 8


solutions = []
average_fitness = []


def conclude(signum, frame):
    columns = int(os.popen('stty size', 'r').read().split()[1])
    print('\r' + '-' * columns + '\n', end='')

    solutions.sort(key=lambda i: i[2].fitness)
    gen_num, i, solution = solutions[-1]

    print('%-10s %.3f' % (f'{gen_num}.{i}', solution.fitness))
    print(solution.genotype)

    px.line(x=range(len(solutions)),
            y=average_fitness,
            labels=dict(x='Generation number', y='Average fitness')).show()

    px.line(x=range(L),
            y=solution.correlation(),
            labels=dict(x='Bits received', y='Self-correlation')).show()
    exit(0)


signal(SIGINT, conclude)


def examine(population: List[Specie]) -> (int, Specie):
    gen_num, best = len(solutions), best_in(population)
    solutions.append((len(solutions), best, population[best]))
    average_fitness.append(compute_average_fitness(population))
    return gen_num, best


population = [Specie.poor(L) for _ in range(N)]
while 1:
    gen_num, best = examine(population)
    if is_good_enough(population[best]):
        break

    print('%-10s %.3f' % (f'{gen_num}.{best}', population[best].fitness))

    younglings = []
    for pair in random_pairs(population):
        offspring = recombine(*pair, prob=Rp)
        if offspring:
            younglings.extend(offspring)

    for specie in younglings:
        specie.mutate(Mc, prob=Mp)

    population.extend(younglings)
    population = evaluate(population, count=N)

conclude(0, 0)
