import numpy as np

class hillclimber:

  def __init__(self, N):

    self.N = N
  
  def climb(self, V, T, E):

    Vs = np.zeros((T, self.N))

    Es = np.zeros(T)

    VE = E(V)

    Vs[0] = V

    Es[0] = VE

    for t in range(1, T):

      V_ = V.copy()

      i = np.random.randint(0, self.N)

      V_[i] = 1 - V_[i]

      V_E = E(V_)

      if V_E <= VE:

        V = V_

        VE = V_E
      
      Vs[t] = V

      Es[t] = VE

    return (Vs, Es)

  def multiple_restart(self, T, R, E):

    runs = {}

    for r in range(R):

      runs[r] = self.climb(np.random.choice((0, 1), self.N), T, E)
    
    return runs

class PBIL:

  def __init__(self, N, lr, nlr, mut_prob, mut_shift):

    self.P = np.ones(N) - 0.5

    self.N = N

    self.lr = lr

    self.nlr = nlr

    self.mut_prob = mut_prob

    self.mut_shift = mut_shift
  
  def optimize(self, T, population_size, E):

    best_inds = np.zeros((T, self.N))

    best_inds_E = np.zeros(T)

    for t in range(T):

      population = (np.random.uniform(0, 1, (population_size, self.N)) <= self.P).astype(np.int)

      best_ind = population[0]

      best_ind_E = E(best_ind)

      worst_ind = population[0]

      worst_ind_E = E(worst_ind)

      for ind in population:

        ind_E = E(ind)

        if ind_E <= best_ind_E:

          best_ind = ind

          best_ind_E = ind_E
        
        if ind_E >= worst_ind_E:

          worst_ind = ind

          worst_ind_E = ind_E
        
      self.P = self.P * (1 - self.lr) + best_ind * self.lr

      neq = best_ind != worst_ind

      self.P = self.P * (1 - (self.nlr * neq)) + best_ind * self.nlr * neq

      mut = (np.random.uniform(0, 1, self.N) <= self.mut_prob).astype(np.int)

      shift = (np.random.uniform(0, 1, self.N) >= 0.5).astype(np.int) * self.mut_shift

      self.P = self.P * (1 - (shift * mut)) + shift * mut
      
      best_inds[t] = best_ind

      best_inds_E[t] = best_ind_E

    return (best_inds, best_inds_E)

class rHNS:

  def __init__(self, N, lr):

    self.N = N

    self.lr = lr

    self.W = np.zeros((N, N))

    self.diag = 1 - np.diag(np.ones(N))

  def E(self, V):

    V = V[:, np.newaxis]

    return -((V.T @ self.W) @ V) / 2
  
  def hebb(self, V):

    V = V[:, np.newaxis]

    dW = (V @ V.T) * self.lr

    self.W = (self.W + dW) * self.diag

  def relax(self, V, T, f):

    Vs = np.zeros((T, self.N))

    Es = np.zeros(T)

    i_t = np.random.randint(0, self.N, T)

    VE = self.E(V) + f(V)

    Vs[0] = V

    Es[0] = VE

    for t in range(T):

      V_ = V.copy()

      V_[i_t[t]] = V_[i_t[t]] * -1

      V_E = self.E(V_) + f(V_)

      if V_E <= VE:

        V = V_

        VE = V_E
        
      Vs[t] = V

      Es[t] = f(V)
    
    self.hebb(V)
    
    return (Vs, Es)
  
  def multiple_relax(self, T, R, f):

    runs = {}

    for r in range(R):

      runs[r] = self.relax(np.random.choice((-1, 1), self.N), T, f)
    
    return runs