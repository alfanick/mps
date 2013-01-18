from random import randrange
from math import ceil

class Graph(object):
    '''
    Simple Graph representation
    '''

    def __init__(self, n, undirected = True):
        '''
        The constructor - creates graph with given n vertices.

        n - number of vertices
        undirected - True if graph should be undirected, False for directed.
                     Complementary edges are added automatically
        '''

        self.klist = []
        self.undirected = undirected
        self.size = 0
        for i in xrange(n):
            self.klist.append( [ ] )
            self.size = n
            
    def append(self, n, m, k):
        '''
        Add edge between two vertices with given cost. Creates two edges if
        graph is undirected.

        n,m - edges to connect
        k - cost
        '''

        self.klist[n].append( (m, k,) )

        if self.undirected:
            self.klist[m].append( (n, k, ) )
    
    def is_incident(self, n, m):
        '''
        Check if two vertices are incident (directly connected)
        '''

        try:
            return len([True for (x,y) in self.klist[n] if x == m]) > 0
        except:
            return False
    
    def is_connected(self, n, m, visited=False):
        '''
        Check if there is a path between two vertices
        '''

        if not visited:
            visited = [False] * self.size
        visited[n] = True
        
        for (x,y) in self.klist[n]:
            if x == m:
                return True
            elif not visited[x]:
                return self.is_connected(x, m, visited)
        return False

    def cost(self, u, v):
        '''
        Returns a cost between two incident verticies
        '''

        for (x,w) in self.klist[u]:
            if x == v:
                return w
        return False

    def neighbours_matrix(self):
        '''
        Returns neighbours matrix representation of the graph
        '''

        matrix = []
        for i in xrange(self.size):
            matrix.append([-1] * self.size)
        for i,adj in enumerate(self.klist):
            for u,w in adj:
                matrix[i][u] = w
        return matrix

    def remove_edge(self, a, b):
        '''
        Removes connection between a and b (one way only!).

        If graph is undirected, removing connection from a to b, will not
        remove connection form b to a.
        '''

        if self.is_connected(a, b):
            self.klist[a] = filter(lambda x: x[0] != b, self.klist[a])

            return True

        return False

    def __str__(self):
        '''
        Human readable form of the graph
        '''

        ret = ""
        for (a, A) in enumerate(self.klist):
            ret += "%d:\n  " % a

            ret += ", ".join(["  %d(%d)" % x for x in A]) + "\n"
        return ret


    @staticmethod
    def from_input(undirected = True):
        '''
        Parses stdin into graph.
        First row: n m - where n is number of vertices, m number of edges, then
        m rows of triples a b c (path from a to b with cost c).
        '''

        n, m = (int(v) for v in raw_input().split())

        G = Graph(n, undirected)

        for i in xrange(m):
            G.append(*(int(v) for v in raw_input().split()))
        
        return G

    @staticmethod
    def complete(n = 8, max_c = False):
        '''
        Creates complete undirected graph of given size n. It randomizes cost
        from [1, max_c) - where max_c is n*n unless given.
        '''

        if max_c is False:
            max_c = n*n

        G = Graph(n)

        for i in xrange(n):
            for j in xrange(i):
                G.append(i, j, randrange(1, max_c))
        
        return G

    @staticmethod
    def random(n = 8, f = 0.7, max_c = False):
        '''
        Creates random undirected graph with given size n and fill factor.
        '''

        if max_c is False:
            max_c = n*n

        G = Graph(n)

        e = int(ceil(((n*(n-1))/2.0) * f))

        for i in xrange(e):
            while True:
                a = randrange(0, n)
                b = randrange(0, n)
                
                if a == b or G.is_incident(a,b):
                    continue

                G.append(a, b, randrange(1, max_c))

                break

        return G
