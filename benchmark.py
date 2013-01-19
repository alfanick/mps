from algorithms import bruteforce, ant_colony, greedy, genetic
from base import *

if __name__ == '__main__':
    print "### Benchmark for 10-vertex complete, random graph ###\n\n"
    graph = Graph.complete(15)
    #graph.linearize()
    
    # Bruteforce
    cost, path = bruteforce.bruteforce(graph)
    print "Bruteforce algorithm - Shortest, optimal\n%d - %s\n" % (cost, path,)
    
    # Greedy
    cost, path = greedy.tsp(graph, func_name="shortest")
    print "Greedy algorithm - shortest path\n%d - %s\n" % (cost, path,)
    cost, path = greedy.tsp(graph, func_name="longest")
    print "Greedy algorithm - longest path\n%d - %s\n" % (cost, path,)
    
    # Genetic
    gtsp = genetic.GeneticTSP(graph, 3, 50, 0.15, 0.1)
    gtsp.run(100)
    cost, path = gtsp.result()
    print "Genetic algorithm - shortest path\n%d - %s\n" % (cost, path,)
    
    # Ant Colony
    colony = ant_colony.AntColony(graph, ants_number=15, iterations=120)
    cost, path = colony.run()
    print "Ant Colony algorithm - shortest path\n%d - %s\n" % (cost, path,)
    