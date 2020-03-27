def get_poa(game):
    pass

def get_poa(f, w):
    pass


class CongestionPoA:
    def I(cls, n):
        ind = []
        for i in range(1, n+1):
            all_i = [(j[0], j[1]-j[0]-1, i-j[1]+1) for j in combinations(range(i+2), 2)]
            ind += all_i
        return ind

    def I_r(cls, n):
        ind = []
        for i in range(0, n+1):
            not_a = [(0, j, i) for j in range(n+1-i)]
            not_x = [(j, 0, i) for j in range(n+1-i)]
            not_b = [(j, i, 0) for j in range(n+1-i)]
            ind = ind + not_a + not_b + not_x

        ind += [(j[0], j[1]-j[0]-1, n-j[1]+1) for j in combinations(range(n+2), 2)]
        return [j for j in list(set(ind)) if j != (0, 0, 0)]

    def function_poa(self):
        """ returns the distribution rule f for the optimal PoA """
        num = len(self.I_r)
        G = np.zeros((num+1, self.n+1), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        h[num] = -1
        
        c = np.zeros((self.n+1, 1), dtype='float')
        c[0] = 1
        for i in range(num):
            a, x, b = self.I_r[i]
            G[i, a+x] = a
            if a+x < self.n:
                G[i, a+x+1] = -b
            G[i, 0] = -self.w[a+x]
            h[i] = -self.w[b+x]
        G[num][0] = -1

    def dual_poa(cls): 
        if self.f[1] <= 0:
            return 0
        num = len(self.I_r)

        G = np.zeros((num+1, 2), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        c = np.array([[0], [1]], dtype='float')  # variables = [lambda , mu]

        for i in range(num):
            a, x, b = self.I_r[i]
            G[i, 0] = a*self.f[a+x] - b*self.f[a+x+1] if a+x < self.n else a*self.f[a+x]
            G[i, 1] = -self.w[a+x]
            h[i] = -self.w[b+x]
        G[num][0] = -1

    def primal_poa(cls):     
        if self.f[1] <= 0:
            return 0
        num = len(self.I)

        c = -np.array([self.w[b+x] for a, x, b in self.I], dtype='float')
        cons_1 = [a*self.f[a+x] - b*self.f[a+x+1] if a+x < self.n else a*self.f[a+x]
                 for a, x, b in self.I]
        cons_2 = np.identity(num)
        G = -np.vstack((cons_1, cons_2))
        A = np.array([[self.w[a+x] for a, x, b in self.I]], dtype='float')
        b = np.array([[1]], dtype='float')
        h = np.zeros((num+1, 1))

    def worst_case(cls, theta):
        players = [i for i in range(self.n)]
        values = []
        strategies = [[(), ()] for _ in players]
        c = 0
        for j in range(len(self.I)):
                a, x, b = self.I[j]
                val = round(theta[j], 8)  # round theta to avoid ~0 value resources
                if val > 0:
                    values += [val/self.n]*self.n
                    ind = [(k % self.n) + c for k in range(2*self.n)]
                    for p in players:
                        strategies[p][0] = strategies[p][0] + tuple(ind[p:p+a+x])
                        strategies[p][1] = strategies[p][1] + tuple(ind[p+self.n-b:p+self.n+x])
                    c += self.n
        return (players, strategies, values, self.w, self.f)








    self.lp_solver(c, G, h)
    poa = 1./self.sol['primal objective']
    f = [0.] + list(sol['x'])[1:]
    return (poa, f)



    self.lp_solver(c, G, h)
    return 1./self.sol['primal objective']

    self.lp_solver(c, G, h, A, b)
    game = self.worst_case(self.sol['x']) # worst case game instance
    return -1./self.sol['primal objective'], game









    def primal_poa(self):     
        """ primal formulation for calculation of Price of Anarchy """
        N = 4**self.n - 1
        c = np.zeros((N,), dtype='float')
        cons_1 = np.zeros((self.n, N), dtype='float')
        A = np.zeros((1, N), dtype='float')
        for i in range(len(self.partition)):
            p = self.partition[i]
            Na = [k for k in range(self.n) if p[k]==1]
            Nx = [k for k in range(self.n) if p[k]==2]
            Nb = [k for k in range(self.n) if p[k]==3]

            c[i] = -self.w_poa(Nb + Nx)
            A[0, i] = self.w_poa(Na + Nx)
            for j in range(self.n):
                cons_1[j][i] = self.nash_poa(j, Na, Nb, Nx)

        cons_2 = np.identity(N)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((N+self.n, 1))
        b = np.array([[1]], dtype='float')
        
        self.lp_solver(c, G, h, A, b)
        game = self.worst_case(np.array(self.sol['x']).flatten()) # worst case game instance
        return -1./self.sol['primal objective'], game 

    def nash_poa(self, j, Na, Nb, Nx):
        """ define the nash constraint for the computable poa calculation """
        if j in Na:
            return self.f_poa(j, Na + Nx)
        elif j in Nb:
            return -self.f_poa(j, Na + Nx + [j])
        else:
            return 0

    def f_poa(self, i, players):
        """ design distribution function """
        pass

    def w_poa(self, players):
        """ welfare function """
        pass

    def f_r(self, i, res, players):
        """ function design for the utility function depends on what resource,
        and what players are covering it """
        return self.values[res] * self.f_poa(i, players)

    def w_r(self, res, players):
        """ welfare function, returns a scalar value dependent on the resource and which players select it """
        return self.values[res] * self.w_poa(players)

    def worst_case(self, theta):
        """ get worst case instance """
        players = [i for i in range(self.n)]
        values = []
        strategies = [[(), ()] for _ in players]
        c = 0
        for i in range(len(theta)):
            val = round(theta[i], 7) # round theta to avoid ~0 value resources
            if  val > 0:
                values.append(val)
                for j in range(self.n):
                    if self.partition[i][j] == 1:
                        strategies[j][0] += (c,)
                    elif self.partition[i][j] == 2:
                        strategies[j][0] += (c,)
                        strategies[j][1] += (c,)
                    elif self.partition[i][j] == 3:
                        strategies[j][1] += (c,)
                c += 1
        return players, strategies, values, self.w, self.f