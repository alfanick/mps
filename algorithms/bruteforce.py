import sys
sys.path.append('..')
from base import *
from itertools import permutations

cycles = []

def find_cycles(graph, node=0, path=[], cost=0):
    path.append(node)
    
    if len(path) > 1:
        cost += graph.cost(path[-2], node)
    
    if len(path) == graph.size and graph.is_adjacent(node, path[0]):
        path.append(path[0])
        cost += graph.cost(node, path[0])
        global cycles
        cycles.append((cost, path,))
    else:
        for u in graph.adjacency_list(node).iterkeys():
            if u not in path:
                find_cycles(graph, u, list(path), cost)
            
            
def bruteforce(graph, start=0):
    global cycles
    find_cycles(graph, start)
    cycles.sort()
    try:
        return cycles[0]
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
    graph = Graph.complete(10)
    graph.linearize()

    cost, path = bruteforce(graph)
    if cost is not False:
        print "Cheapest path costs %d and constists of: %s" % (cost, ", ".join(map(str,path)))
    else:
        print "There is no Hamillton cycle in given graph"
