import numpy as np

class TSP:

    def __init__(self, C, symmetric=True):

        self.C = C

        self.symmetric = symmetric
    
        self.idx_length = np.sqrt(C).astype(np.int)

        self.tour_string_length = (C * self.idx_length).astype(np.int)

        roads = np.random.uniform(low=0, high=1, size=(C,C))

        diag = 1 - np.diag(np.ones(C))

        self.roads = roads * roads.T * diag
    
    def tour_length(self, tour_string):

        indexes = np.zeros(self.C)

        for i in range(self.C):

            bits = tour_string[i * self.idx_length: (i + 1) * self.idx_length]

            indexes[i] = bits.dot(2**np.arange(bits.size)[::-1])
        
        order = np.argsort(indexes)

        tour_length = sum([self.roads[order[i-1], order[i]] for i in range(1, self.C)])

        return 1/tour_length

class MDKP:

    def __init__(self, S, N):

        self.D = len(S)

        self.S = list(S)

        self.N = N

        self.sizes = np.random.randint(1, np.max(S), [N] + [self.D])

        self.masses = np.random.randint(1, N, N)
    
    def fill_knapsack(self, V):

        filled = np.zeros(self.D)

        S_a = np.array(self.S)

        mass = 0

        i = 0

        while (filled <= S_a).all() and i < self.N:

            print(f'{i}:{(filled <= S_a).all()}:{mass}')

            filled += self.sizes[i]

            mass += self.masses[i]

            i += 1

        if not (filled <= S_a).all():

            return 0
        
        return mass
