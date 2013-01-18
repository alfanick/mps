import sys
sys.path.append('..')
from base import *

from random import choice

def random(available):
    return choice(available.keys())

def shortest(available):
    return min(available, key=available.get)

def longest(available):
    return max(available, key=available.get)

def tsp(G, select_function = longest, start = 0, allowed = True):
    path = []
    length = 0

    path.append(start)

    if allowed is True:
        allowed = range(0, G.size)

    allowed.remove(start)

    allowed_and_adjacent = { }

    for key, value in G.adjacency_list(start).iteritems():
        if key in allowed:
            allowed_and_adjacent[key] = value

    if (len(allowed_and_adjacent) > 0):
        next_city = select_function(allowed_and_adjacent)
        length = G.cost(start, next_city)

        result = tsp(G, select_function, next_city, allowed)
        
        length += result[0]
        path += result[1]

    return (length, path)