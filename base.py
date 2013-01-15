class Reader(object):
    def __init__(self, n, m):
        pass

class Graph(object):
    def __init__(self, n):
        self.klist = []
        for i in range(n):
            self.klist.append( [ ] )
            
    def append(self, n, m, k):
        self.klist[n].append( (m, k,) )
    
    def is_incident(self, n, m):
        try:
            return len([True for (x,y) in self.klist[n] if x == m]) > 0
        except:
            return False
    
    def _visit(self, n):
      pass
            
    def is_connected(self, n, m, visited=False):
      if not visited:
        visited = [False]*len(self.klist)
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
        pass

