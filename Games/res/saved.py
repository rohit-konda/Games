











'''
class InfoPoaGame(CompResourceGame, DistInfoGame):
    """ framework for resource games with computable price of anarchy """
    def __init__(self, players, strategies, values, w, f, infograph, solver='cvxopt'):
        CompResourceGame.__init__(self, players, strategies, values, w, f, solver)
        DistInfoGame.__init__(self, players, strategies, values, w, f, infograph)
        self.partition = list(product([1, 2, 3, 4], repeat=self.n))[:-1]

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
            c[i] = -self.w[len(Nb + Nx)]
            A[0, i] = self.w[len(Na + Nx)]
            for j in range(self.n):
                if j in Na:
                    nash = self.f[len(self.viewed(Na + Nx, j))]
                elif j in Nb:
                    nash = -self.f[len(self.viewed(Na + Nx, j)) + 1]
                else:
                    nash = 0
                cons_1[j][i] = nash

        cons_2 = np.identity(N)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((N+self.n, 1))
        b = np.array([[1]], dtype='float')
        self.poa_solver(c, G, h, A, b)
        game = self.worst_case(np.array(self.sol['x']).flatten()) # worst case game instance
        return -1./self.sol['primal objective'], game 

    def viewed(self, covered, j):
        """ modify the outcome based on which other agents are viewed """
        return [k for k in covered if k in self.infograph[j] + [j]]

    def optimal_function(self):
        """ get optimal distriution function """
        pass

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
        return players, strategies, values, self.w, self.f, self.infograph


class InfoPoaSumGame(InfoPoaGame):
    """ See if sum Nash condition returns the same value """
    def __init__(self, players, strategies, values, w, f, infograph, solver='cvxopt'):
        InfoPoaGame.__init__(self, players, strategies, values, w, f, infograph, solver)

    def primal_poa(self):     
        """ primal formulation for calculation of Price of Anarchy """
        N = 4**self.n - 1
        c = np.zeros((N,), dtype='float')
        cons_1 = np.zeros((1, N), dtype='float')
        A = np.zeros((1, N), dtype='float')
        for i in range(len(self.partition)):
            p = self.partition[i]
            Na = [k for k in range(self.n) if p[k]==1]
            Nx = [k for k in range(self.n) if p[k]==2]
            Nb = [k for k in range(self.n) if p[k]==3]
            c[i] = -self.w[len(Nb + Nx)]
            A[0, i] = self.w[len(Na + Nx)]
            nash_cond = 0
            for j in range(self.n):
                if j in Na:
                    nash = self.f[len(self.viewed(Na + Nx, j))]
                elif j in Nb:
                    nash = -self.f[len(self.viewed(Na + Nx, j)) + 1]
                else:
                    nash = 0
                nash_cond += nash
            cons_1[0][i] = nash_cond

        cons_2 = np.identity(N)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((N+1, 1))
        b = np.array([[1]], dtype='float')
        
        self.poa_solver(c, G, h, A, b)
        game = self.worst_case(np.array(self.sol['x']).flatten()) # worst case game instance
        return -1./self.sol['primal objective'], game 


class AltruisticGame(InfoPoaGame):
    """ See if sum Nash condition returns the same value """
    def __init__(self, players, strategies, values, w, f, infograph, solver='cvxopt', alpha=1):
        InfoPoaGame.__init__(self, players, strategies, values, w, f, infograph, solver)
        self.alpha = alpha

    def primal_poa(self):
        """ primal formulation for calculation of Price of Anarchy """
        N = 4**self.n - 1
        c = np.zeros((N,), dtype='float')
        cons_1 = np.zeros((1, N), dtype='float')
        A = np.zeros((1, N), dtype='float')
        for i in range(len(self.partition)):
            p = self.partition[i]
            Na = [k for k in range(self.n) if p[k]==1]
            Nx = [k for k in range(self.n) if p[k]==2]
            Nb = [k for k in range(self.n) if p[k]==3]
            c[i] = -self.w[len(Nb + Nx)]
            A[0, i] = self.w[len(Na + Nx)]
            nash_cond = 0
            for j in range(self.n):
                if j in Na:
                    nash = self.f[len(Na + Nx)]
                elif j in Nb:
                    nash = -self.f[len(Na + Nx) + 1]
                else:
                    nash = 0
                for k in self.infograph[j]:
                    if k in Na:
                        nash += self.alpha * self.f[len(Na + Nx)]
                    elif k in Nb:
                        nash -= self.alpha * self.f[len(Na + Nx) + 1]
                nash_cond += nash
            cons_1[0][i] = nash_cond

        cons_2 = np.identity(N)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((N+1, 1))
        b = np.array([[1]], dtype='float')

        self.poa_solver(c, G, h, A, b)
        game = self.worst_case(np.array(self.sol['x']).flatten()) # worst case game instance
        return -1./self.sol['primal objective'], game

class AltruisticGame2(InfoPoaGame):
    """ See if sum Nash condition returns the same value """
    def __init__(self, players, strategies, values, w, f, infograph, solver='cvxopt', alpha=1):
        InfoPoaGame.__init__(self, players, strategies, values, w, f, infograph, solver)
        self.alpha = alpha

    def primal_poa(self):
        """ primal formulation for calculation of Price of Anarchy """
        N = 4**self.n - 1
        c = np.zeros((N,), dtype='float')
        cons_1 = np.zeros((1, N), dtype='float')
        A = np.zeros((1, N), dtype='float')
        for i in range(len(self.partition)):
            p = self.partition[i]
            Na = [k for k in range(self.n) if p[k]==1]
            Nx = [k for k in range(self.n) if p[k]==2]
            Nb = [k for k in range(self.n) if p[k]==3]
            c[i] = -self.w[len(Nb + Nx)]
            A[0, i] = self.w[len(Na + Nx)]
            nash_cond = 0
            for j in range(self.n):
                if set(self.infograph[j] + [j]) & set(Na):
                    nash = self.f[len(Na + Nx)]
                elif set(self.infograph[j] + [j]) & set(Nb):
                    nash = -self.f[len(Na + Nx) + 1]
                else:
                    nash = 0
                nash_cond += nash
            cons_1[0][i] = nash_cond

        cons_2 = np.identity(N)
        G = -np.vstack((cons_1, cons_2))
        h = np.zeros((N+1, 1))
        b = np.array([[1]], dtype='float')
        
        self.poa_solver(c, G, h, A, b)
        game = self.worst_case(np.array(self.sol['x']).flatten()) # worst case game instance
        return -1./self.sol['primal objective'], game
'''