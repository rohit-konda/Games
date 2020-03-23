    def lp_solver(self, c, G, h, A=None, b=None):
        """ function for solving the relevant optimization program"""
        if self.solver == 'cvxopt':
            c = matrix(c)
            G = matrix(G)
            h = matrix(h)
            A = matrix(A) if A is not None else None
            b = matrix(b) if b is not None else None
            self.sol = lp(c, G, h, A, b)
            if self.sol['status'] != 'optimal':
                raise ValueError('no feasible solution found')
        else:
            raise ValueError('indicated a invalid solver name for self.solver')