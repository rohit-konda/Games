
from itertools import chain, combinations

def powerset(iterable):
    """ returns the powerset of an iterable object (as a list of tuples)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))
