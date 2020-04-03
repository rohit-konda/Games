from itertools import combinations

class CongestionPoA:
    def I(cls, N):
        ind = []
        for i in range(1, N+1):
            all_i = [(j[0], j[1]-j[0]-1, i-j[1]+1) for j in combinations(range(i+2), 2)]
            ind += all_i
        return ind

    def I_r(cls, N):
        ind = []
        for i in range(0, N+1):
            not_a = [(0, j, i) for j in range(N+1-i)]
            not_x = [(j, 0, i) for j in range(N+1-i)]
            not_b = [(j, i, 0) for j in range(N+1-i)]
            ind = ind + not_a + not_b + not_x

        ind += [(j[0], j[1]-j[0]-1, N-j[1]+1) for j in combinations(range(N+2), 2)]
        return [j for j in list(set(ind)) if j != (0, 0, 0)]

    def check_welfare(cls, w):
        try:
            iter(w)
        except Exception as e:
            raise ValueError('w must be iterable.')
        if w[0] != 0: 
            raise ValueError('Should input w with w[0] = 0.')
        if any(w[1:] <= 0):
            raise ValueError('Should input w with w[n] > 0 for all n > 0.')

    def check_f(cls, f, w):
        try:
            iter(f)
        except Exception as e:
            raise ValueError('f must be iterable.')

        if f[0] != 0: 
            raise ValueError('Should input f with f[0] = 0.')
        if self.f[1] <= 0:
            raise ValueError('PoA = 0 if f[1] <= 0.')
        if len(f) != len(w):
            raise ValueError('Should input f with length matching w.')

    def function_poa(cls, w):
        cls.check_welfare(w)
        N = len(w)
        I_r = cls.I_r(n)
        num = len(I_r)
        
        G = np.zeros((num+1, N+1), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        h[num] = -1
        c = np.zeros((N+1, 1), dtype='float')
        c[0] = 1

        for i, a, x, b in enumerate(I_r):
            #a, x, b = i_r
            G[i, a+x] = a
            if a+x < N:
                G[i, a+x+1] = -b
            G[i, 0] = -w[a+x]
            h[i] = -w[b+x]
        G[num][0] = -1
        
        return c, G, h

    def dual_poa(cls, f, w): 
        cls.check_welfare(w)
        cls.check_f(f, w)
        N = len(w)
        I_r = cls.I_r(N)
        num = len(I_r)

        G = np.zeros((num+1, 2), dtype='float')
        h = np.zeros((num+1, 1), dtype='float')
        c = np.array([[0], [1]], dtype='float')  # variables = [lambda , mu]

        for i, a, x, b in enumerate(I_r):
            #a, x, b = i_r
            G[i, 0] = a*f[a+x] - b*f[a+x+1] if a+x < N else a*f[a+x]
            G[i, 1] = -w[a+x]
            h[i] = -w[b+x]
        G[num][0] = -1

        return c, G, h

    def primal_poa(cls, f, w):     
        cls.check_welfare(w)
        cls.check_f(f, w)
        N = len(w)
        I = cls.I(N)
        num = len(I)

        c = -np.array([w[b+x] for a, x, b in I], dtype='float')
        cons_1 = [a*f[a+x] - b*f[a+x+1] if a+x < N else a*f[a+x] for a, x, b in I]
        cons_2 = np.identity(num)
        G = -np.vstack((cons_1, cons_2))
        A = np.array([[w[a+x] for a, x, b in I]], dtype='float')
        b = np.array([[1]], dtype='float')
        h = np.zeros((num+1, 1))

        return c, G, h, A, b

    def worst_case(cls, theta, N):
        values = []
        actions = [[(), ()] for _ in range(N)]
        I = cls.I(N)

        c = 0
        for j, a, x, b in enumerate(I):
                #a, x, b = res
                val = round(theta[j], 8)  # round theta to avoid ~0 value resources
                if val > 0:
                    values += [val/N]*N
                    ind = [(k % N) + c for k in range(2*N)]
                    for p in range(N):
                        strategies[p][0] = strategies[p][0] + tuple(ind[p:p+a+x])
                        strategies[p][1] = strategies[p][1] + tuple(ind[p+N-b:p+N+x])
                    c += N
        
        return actions, values


class ResourcePoA(CongestionPoA):
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