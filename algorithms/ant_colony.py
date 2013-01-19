import sys
sys.path.append('..')
from base import *

#DEBUG = True
DEBUG = False

class Ant(object):
    def __init__(self, graph, node, colony):
        self.tabu = [node]
        self.graph = graph
        self.current_node = node
        self.colony = colony
        self.cost = 0
        
        # Local pheromones values
        self.pheromones = []
        for i in xrange(self.graph.size):
            self.pheromones.append( { } )
        
    def probabilities(self, i):
        '''
        Generate list containing probabilities for each adjacent node
        
        i - node we are looking adjacency for
        '''
        
        # Adjacent nodes not in tabu list
        available = [(j, cost) for (j,cost) in self.graph.adjacency_list(i).iteritems() if j not in self.tabu]

        # Given equation (16.3 bottom)
        to_sum = [ ((self.colony.pheromones[i][x])**self.colony.alfa*(1.0/y)**self.colony.beta) for (x,y) in available ]
        entire = sum(to_sum)
        
        #Calculate probability for each available node
        res = []
        for (j,cost) in available:
            # Given equation (16.3 top)
            res.append((self.colony.pheromones[i][j]**self.colony.alfa*(1.0/cost)**self.colony.beta, j,))
        
        res.sort(reverse=True)
        
        return res
            

    def step(self):
        '''
        Make step further to the best possible node
        '''
        
        # Ant has already found cycle
        if len(self.tabu) == self.graph.size:
            self.tabu.append(self.tabu[0])
            self.cost += self.graph.cost(self.tabu[-2], self.tabu[-1])
            return False
        
        probabilities = self.probabilities(self.current_node)

        # Choose node with biggest probability from sorted list
        chosen_node = probabilities[0][1]
        
        # Move to node
        self.cost += self.graph.cost(self.current_node, chosen_node)
        self.current_node = chosen_node
        self.tabu.append(chosen_node)
        
        return True
    

    def update_path(self):
        '''
        Update pheromone trace on each visited node
        '''
        
        # Every two tabu nodes
        for i,j in zip(self.tabu, self.tabu[1:]):
            self.pheromones[i][j] = self.colony.basic_pheromone / self.cost
            
        
            
class AntColony(object):
    def __init__(self, graph, ants_number, iterations):
        # Parameters
        self.ro = 0.9
        self.alfa = 0.5
        self.beta = 1

        self.graph = graph
        
        self.reset_pheromones()
                
        self.iterations = iterations
        self.ants_number = ants_number
    
    def reset_pheromones(self):
        avg = self.average_cost()
        self.basic_pheromone = 1.0 / (self.graph.size * 0.5 * avg)
        
        self.pheromones = []
        for i in xrange(self.graph.size):
            self.pheromones.append( { } )
            for node in self.graph.adjacency_list(i):
                self.pheromones[i][node] = self.basic_pheromone
    
    def update_pheromones(self, ants):
        '''
        Update pheromone traces on each edge basing on 
        each ant information
        
        ants - ants population
        '''
        
        dry = []
        for i in xrange(self.graph.size):
            dry.append( { } )
        
        for ant in ants:
            for i in xrange(self.graph.size):
                for j,pheromone in ant.pheromones[i].iteritems():
                    if j not in dry[i]:
                        self.pheromones[i][j] = (1-self.ro)*self.pheromones[i][j]
                        dry[i][j] = True
                    self.pheromones[i][j] += pheromone

    def run(self):
        '''
        Start ant colony algorithm
        '''
        
        best_cost = sys.maxint
        best_path = []
        
        for i in xrange(self.iterations):
            
            ants = []
            for i in xrange(self.ants_number):
                ants.append(Ant(self.graph, 0, self))
                
            for ant_id,ant in enumerate(ants):
                while ant.step():
                    if DEBUG:
                        print "Mrowka %d %s" % (ant_id, ant.tabu)
                ant.update_path()
                
                if best_cost > ant.cost:
                    best_path = ant.tabu
                    best_cost = ant.cost
                    
                self.update_pheromones(ants[ant_id:ant_id+1])
        
        return (best_cost, best_path)
    
    def average_cost(self):
        return self.average(self.graph.neighbours_matrix())
        
    def average(self, matrix):
        
        suma = 0
        for r in xrange(0, self.graph.size):
            for s in xrange(0, self.graph.size):
                suma += matrix[r][s]

        avg = suma / (self.graph.size * self.graph.size)
        
        return avg
        
        
        
if __name__ == '__main__':
    graph = Graph.from_input()
    colony = AntColony(graph, 10, 10)
    cost, path = colony.run()
    print cost, path
    
