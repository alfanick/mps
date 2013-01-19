from algorithms import bruteforce, ant_colony, greedy, genetic
from base import *
import sys
import os
from time import time

def bruteforce_run(graph):
    return bruteforce.bruteforce2(graph)

def greedy_shortest(graph):
    return greedy.tsp(graph, func_name="shortest")

def greedy_longest(graph):
    return greedy.tsp(graph, func_name="longest")

def genetic_10n(graph):
    gtsp = genetic.GeneticTSP(graph, 3, 50, 0.35, 0.1)
    gtsp.run(graph.size * 10)
    return gtsp.result()

def genetic_100n(graph):
    gtsp = genetic.GeneticTSP(graph, 3, 50, 0.35, 0.1)
    gtsp.run(graph.size * 100)
    return gtsp.result()

def ant_colony_10n(graph):
    colony = ant_colony.AntColony(graph, ants_number=15,
            iterations=graph.size*10)
    return colony.run()

def ant_colony_100n(graph):
    colony = ant_colony.AntColony(graph, ants_number=15,
            iterations=graph.size*100)
    return colony.run()
    
def file_inputs_graphes():
    inputs = os.listdir('tests/')
    for filename in inputs:
        if Graph.from_file('tests/%s' % (filename)) is not False:
            yield Graph.from_file('tests/%s' % (filename))
    

if __name__ == '__main__':
    N = xrange(3,12)
    AVG = 5

    benchmark_set = []
    rnd = True

    if len(sys.argv) == 2:
        benchmark_set = [Graph.from_file(sys.argv[1])]
        N = [benchmark_set[0].size]
        rnd = False
    else:
        benchmark_set = [Graph.complete(n) for n in N]

    # Uncomment to get inputs from files in tests dir
    #benchmark_set = file_inputs_graphes()
    
    ALGORITHMS = []
    if rnd:
        ALGORITHMS.append(('Brute Force', bruteforce_run,))     # Comment to fuck bruteforce!!!!
    ALGORITHMS.append(('Greedy Shortest', greedy_shortest,))
    ALGORITHMS.append(('Greedy Longest', greedy_longest,))
    ALGORITHMS.append(('Genetic 10n', genetic_10n,))
    ALGORITHMS.append(('Genetic 100n', genetic_100n,))
    ALGORITHMS.append(('Ant Colony 10n', ant_colony_10n,))
    ALGORITHMS.append(('Ant Colony 100n', ant_colony_100n,))

    TIME = [dict() for n in N]
    RESULT = [dict() for n in N]

    for (n, G) in enumerate(benchmark_set):
        if rnd:
            print "Benchmarking %d-vertices complete, random graph" % (n + N[0])
        else:
            print "Benchmarking %d-vertices complete graph '%s'" % (n + N[0],
                    sys.argv[1])

        for (name, tsp) in ALGORITHMS:
            print "  %s:" % name
            
            t = 0
            min_length = 10000000
            min_path = []
            start_time = 0
            end_time = 0
            for k in xrange(AVG):
                sys.stdout.write("    #%d: " % (k+1))
                start_time = time()
                
                length, path = tsp(G)

                end_time = time() - start_time
                t += end_time
                if length < min_length:
                    min_length = length
                    min_path = []
                sys.stdout.write("%d in %.3fs\n" % (length, end_time))
            TIME[n][name] = t/float(AVG)
            RESULT[n][name] = float(min_length)
            
            if rnd:
                bt =  TIME[n][name] / TIME[n]['Brute Force'] 
                bl = RESULT[n][name] / RESULT[n]['Brute Force']
            
                d = (name, min_length, t/AVG, bt * 100, bl * 100, bl * bt * 100)
                sys.stdout.write("\n    '%s' best %d in %.3fs (t = %.2f%%BF, l = %.2f%%BF, overall %.2f%%)\n      " % d)
            else:
                sys.stdout.write("\n    '%s' best %d in %.3fs\n      " % (name,
                    min_length, t/AVG))
            print path
            print

        print "\n\n"

    print "\n\n"
    print "Nazwa,%s" % (",".join(map(lambda x: str(x), N)))
    for (name, tsp) in ALGORITHMS:
        sys.stdout.write("%s," % name)
        sys.stdout.write("%s\n" % (",".join(map(lambda n: "%.5f" % TIME[n-N[0]][name], N))))

    print "\n\n"
    print "Nazwa,%s" % (",".join(map(lambda x: str(x), N)))
    for (name, tsp) in ALGORITHMS:
        sys.stdout.write("%s," % name)
        sys.stdout.write("%s\n" % (",".join(map(lambda n: "%d" % RESULT[n-N[0]][name], N))))


