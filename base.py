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
        try
            return len([True for (x,y) in self.klist[n] if x == m]) > 0
        except:
            return False

    def neighbours_matrix(self):
        pass

