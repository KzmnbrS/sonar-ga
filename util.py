import random

from functools import wraps


def random_pairs(iterable):
    assert len(iterable) % 2 == 0

    unpaired = [i for i in range(len(iterable))]
    while unpaired:
        i = random.randint(0, len(unpaired) - 1)
        x = unpaired[i]
        del unpaired[i]

        i = random.randint(0, len(unpaired) - 1)
        y = unpaired[i]
        del unpaired[i]

        yield iterable[x], iterable[y]


def with_prob(func):
    @wraps(func)
    def decorated(*args, prob: float, **kwargs):
        dice = random.randint(0, 100) / 100
        if dice > prob:
            return
        return func(*args, **kwargs)

    return decorated
