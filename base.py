class Graph(object):
    def __init__(self, n):
        self.klist = []
        self.size = 0
        for i in xrange(n):
            self.klist.append( [ ] )
            self.size = n
            
    def append(self, n, m, k):
        self.klist[n].append( (m, k,) )
    
    def is_incident(self, n, m):
        try:
            return len([True for (x,y) in self.klist[n] if x == m]) > 0
        except:
            return False
    
    def is_connected(self, n, m, visited=False):
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
      for (x,w) in self.klist[u]:
        if x is v:
          return w
      return False

    def neighbours_matrix(self):
        matrix = []
        for i in xrange(self.size):
            matrix.append([-1] * self.size)
        for i,adj in enumerate(self.klist):
            for u,w in adj:
                matrix[i][u] = w
        return matrix

    def __str__(self):
        ret = ""
        for (a, A) in enumerate(self.klist):
            ret += "%d:\n  " % a

            ret += ", ".join(["  %d(%d)" % x for x in A]) + "\n"
        return ret


    @staticmethod
    def from_input():
        n, m = (int(v) for v in raw_input().split())

        G = Graph(n)

        for i in xrange(m):
            G.append(*(int(v) for v in raw_input().split()))
        
        return G
