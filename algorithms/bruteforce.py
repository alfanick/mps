import sys
sys.path.append('..')
from base import *
from itertools import permutations


class Bruteforce(object):
    def __init__(self, graph):
        self.graph = graph
        self.cycles = []
        
    def find_cycles(self, node=0, path=[], cost=0):
        path.append(node)
        
        if len(path) > 1:
            cost += self.graph.cost(path[-2], node)
        
        if len(path) == self.graph.size and self.graph.is_adjacent(node, path[0]):
            path.append(path[0])
            cost += self.graph.cost(node, path[0])
            self.cycles.append((cost, path,))
        else:
            for u in self.graph.adjacency_list(node).iterkeys():
                if u not in path:
                    self.find_cycles(u, list(path), cost)
                
                
    def run(self, start=0):
        self.find_cycles(start)
        self.cycles.sort()
        try:
            res = self.cycles[0]
            self.cycles = []
            return res
        except:
            return (False, False)
            
            

def bruteforce2(graph):
    min_path = []
    min_cost = 10000000
    for path in permutations(xrange(graph.size)):
        path += (path[0],)
        cost = 0
        for i in xrange(graph.size):
            cost += graph.cost(path[i], path[i+1])
        if (cost < min_cost):
            min_cost = cost
            min_path = path
    return (min_cost, list(min_path),)

if __name__ == '__main__':
    print "Result for random 10-vertex complete graph"
    graph = Graph.complete(5)
    #graph.linearize()
    bruteforce = Bruteforce(graph)
    cost, path = bruteforce.run()
    print "Cheapest path costs %d and constists of: %s" % (cost, ", ".join(map(str,path)))
    bruteforce = Bruteforce(Graph(graph))
    cost, path = bruteforce.run()
    print "Cheapest path costs %d and constists of: %s" % (cost, ", ".join(map(str,path)))
    bruteforce = Bruteforce(Graph(graph))
    cost, path = bruteforce.run()
    print "Cheapest path costs %d and constists of: %s" % (cost, ", ".join(map(str,path)))
    if cost is not False:
        print "Cheapest path costs %d and constists of: %s" % (cost, ", ".join(map(str,path)))
    else:
        print "There is no Hamillton cycle in given graph"
