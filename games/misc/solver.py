from warnings import warn

def lp(solver, c, G, h, A=None, b=None, progress=False):
    wrapper = SolverWrapper(solver, progress)
    return wrapper.lp(c, G, h, A, b)


class SolverWrapper:
    SUPPORTED = ['cvxopt']
    LP_SUPPORTED = ['cvxopt']

    def __init__(self, solver, progress):
        self.solver = solver
        self.check_solver(solver)
        self.progress = progress
        self.returnall = False
    
    def lp(self, c, G, h, A, b):
        if self.solver == 'cvxopt':
            from cvxopt import matrix
            from cvxopt.solvers import lp
            
            c = matrix(c)
            G = matrix(G)
            h = matrix(h)
            A = matrix(A) if A is not None else None
            b = matrix(b) if b is not None else None
            sol = lp(c, G, h, A, b, options={'show_progress': self.progress})
            if sol['status'] != 'optimal':
                warn('no feasible solution found')
            else:
                if self.returnall:
                    return sol
                else:
                    return {'min': sol['primal objective'], 'argmin': list(sol['x'])}
        else:
            raise ImportError('Not a valid or implemented lp solver. Supported lp solvers include ' + ', '.join(self.LP_SUPPORTED) + '.')

    def check_solver(self, solver):
        if self.solver == 'cvxopt':
            pass
        else:
            raise ImportError('Not a valid or implemented solver. Supported solvers include ' + ', '.join(self.SUPPORTED) + '.')