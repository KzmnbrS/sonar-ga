from __future__ import annotations

import random
import numpy as np

from typing import List

from util import with_prob

Genotype = List[int]


class Specie:
    def __init__(self, genotype: Genotype):
        self.genotype = genotype
        self._fitness = self.compute_fitness()

    @classmethod
    def poor(cls, length: int):
        """Generates a poor specie with '1' * `length` genotype."""
        return cls([1 for _ in range(length)])

    def clone(self) -> Specie:
        return Specie(list(self.genotype))

    @property
    def fitness(self) -> float:
        """Cached value is updated on `mutate` and `__setitem__` calls.
        You can update in manually by calling `update_cached_fitness`."""
        return self._fitness

    def compute_fitness(self) -> float:
        correlation = []
        for i, value in enumerate(reversed(self.genotype)):
            cut = len(self.genotype) - (i + 1)
            shift = self.genotype[cut:]

            accum = 0
            for j in range(len(shift)):
                accum += self.genotype[j] * shift[j]
            correlation.append(accum)

        peak = correlation[-1]
        max_petal = max(map(abs, correlation[:-1]))
        return peak / max_petal

    def update_cached_fitness(self):
        self._fitness = self.compute_fitness()

    @with_prob
    def mutate(self, count: int):
        """Mutates `count` choromosomes in the `genotype`."""
        for _ in range(count):
            i = random.randint(0, len(self.genotype) - 1)
            self.genotype[i] *= -1
        self.update_cached_fitness()

    def __getitem__(self, key):
        return self.genotype[key]

    def __setitem__(self, key, new_value):
        self.genotype[key] = new_value
        self.update_cached_fitness()


@with_prob
def recombine(alice: Specie, bob: Specie) -> (Specie, Specie):
    """Recombines given species using a single-point method."""
    assert len(alice.genotype) == len(bob.genotype)
    carol, dan = alice.clone(), bob.clone()

    cut = random.randint(0, len(carol.genotype) - 1)
    carol[cut:], dan[cut:] = dan[cut:], carol[cut:]
    return dan, carol


def evolve(population: List[Specie], count: int) -> List[Specie]:
    """Evolves the `population` leaving the `count` species.
    Probability roulette is used as a selection method."""
    nextgen = []
    for _ in range(count):
        cumulative_fitness = sum(specie.fitness for specie in population)

        def relative_fitness(specie):
            return specie.fitness / cumulative_fitness

        lucker = np.random.choice(range(len(population)),
                                  p=list(map(relative_fitness, population)))

        nextgen.append(population[lucker])
        del population[lucker]
    return nextgen
