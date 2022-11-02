import numpy as np

class TSP:

    def __init__(self, C, symmetric=True):

        self.C = C

        self.symmetric = symmetric
    
        self.idx_length = np.sqrt(C).astype(np.int)

        self.tour_string_length = (C * self.idx_length).astype(np.int)

        self.roads = np.random.uniform(low=0, high=1, size=(C,C))

        diag = 1 - np.diag(np.ones(C))

        roads = roads * roads.T * diag
    
    def tour_length(self, tour_string):

        indexes = np.zeros(self.C)

        for i in range(self.C):

            bits = tour_string[i * self.idx_length: (i + 1) * self.idx_length]

            indexes[i] = bits.dot(2**np.arange(bits.size)[::-1])
        
        order = np.argsort(indexes)

        tour_length = sum([roads[order[i-1], order[i]] for i in range(1, self.C)])

        return 1/tour_length
