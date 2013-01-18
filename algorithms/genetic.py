import sys
sys.path.append('..')
from base import *
from random import randrange, random, shuffle, choice
from copy import copy
from heapq import *

class Genome(list):
    def __init__(self, graph):
        super(list, self).__init__()
        self.graph = graph

        for i in xrange(self.graph.size):
            self.append(i)

        shuffle(self)

        self.et = False

    def mutate(self):
        eb = self.eval()

        a, b = 0, 0
        while a == b:
            a = randrange(len(self))
            b = randrange(len(self))

        ea = self.eval()

        if ea > eb:
            self[a], self[b] = self[b], self[a]
        else:
            self.et = False


    def crossover(self, other):
        try:
            i = other.index(self[0])
            if self.graph.cost(other[i], other[i+1]) <= self.graph.cost(self[0], self[1]):
                k = self.index(other[i+1])
                self[1], self[k] = self[k], self[1]
                self.et = False
        except:
            pass

    def eval(self):
        if not self.et is False:
            return self.et

        length = 0
        for i in xrange(self.graph.size-1):
            length += self.graph.cost(self[i], self[i+1])

        self.et = length + self.graph.cost(self[-1], self[0])
        return self.et

    def __lt__(self, other):
        return self.eval() < other.eval()

    def __str__(self):
        return ("  %d: " % self.eval()) + "-".join(map(lambda x: str(x), self + [self[0]]))


class GeneticTSP(object):
    def __init__(self, graph, longliving = 3, population = 20, mutation = 0.15, crossover = 0.60):
        self.epoch = 0
        self.graph = graph

        self.population = []
        for i in xrange(population):
            heappush(self.population, Genome(self.graph))
        self.population_size = population

        self.mutation_factory = mutation
        self.crossover_factory = crossover
        self.longliving = longliving

    def __str__(self):
        return "#%d <p:%d m:%.2f c: %.2f>" % (self.epoch+1, len(self.population),
                self.mutation_factory, self.crossover_factory)

    def run(self, epochs):
        for self.epoch in xrange(epochs):
            new_population = []
            for i in xrange(self.longliving):
                heappush(new_population, heappop(self.population))
            
            for i in range(self.longliving, self.population_size):
                experiment = copy(heappop(self.population))
                if random() < self.mutation_factory:
                    experiment.mutate()
                if random() < self.crossover_factory:
                    experiment.crossover(new_population[0])
            
                heappush(new_population, experiment)

            self.population = new_population
    
    def result(self):
        m = self.population[0]
        return (m.eval(), list(m + [m[0]]))

if __name__ == '__main__':
    print "Result for random 10-vertex complete graph"
    graph = Graph.complete(10)
    graph.linearize()

    gtsp = GeneticTSP(graph, 2, 50, 0.15, 0.1)

    gtsp.run(50)

    length, path = gtsp.result()

    print "Genetic algorithm %s: %s, %s" % (str(gtsp), length, path)

