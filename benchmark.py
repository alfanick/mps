from algorithms import bruteforce, ant_colony, greedy, genetic
from base import *

if __name__ == '__main__':
    print "### Benchmark for 10-vertex complete, linarized graph ###\n\n"
    graph = Graph.complete(10)
    graph.linearize()
    
    # Bruteforce
    cost, path = bruteforce.bruteforce(graph)
    print "Shortest (optimal) path (calculated by bruteforce)\n%d - %s\n" % (cost, path,)
    
    # Greedy
    cost, path = greedy.tsp(graph, func_name="shortest")
    print "Shortest path calculated calculated by greedy algorithm\n%d - %s\n" % (cost, path,)
    cost, path = greedy.tsp(graph, func_name="longest")
    print "Longest path calculated calculated by greedy algorithm\n%d - %s\n" % (cost, path,)
    
    # Genetic
    gtsp = genetic.GeneticTSP(graph, 3, 50, 0.15, 0.1)
    gtsp.run(100)
    cost, path = gtsp.result()
    print "Longest path calculated calculated by greedy algorithm\n%d - %s\n" % (cost, path,)
    
    # Ant Colony
    colony = ant_colony.AntColony(graph, ants_number=15, iterations=120)
    cost, path = colony.run()
    print "Longest path calculated calculated by greedy algorithm\n%d - %s\n" % (cost, path,)
