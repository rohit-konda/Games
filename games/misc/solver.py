from warnings import warn

def lp(solver, c, G, h, A=None, b=None):
    wrapper = SolverWrapper(solver, 'lp')
    return wrapper.lp(c, G, h, A, b)


class SolverWrapper:
    _supported = ['cvxopt']

    def __init__(self, solver, program):
        self.solver = solver
        self.program = program
        self.check_solver(solver)
    
    def lp(cls, c, G, h, A, b):
        if solver == 'cvxopt':
            from cvxopt.solvers import lp
            c = matrix(c)
            G = matrix(G)
            h = matrix(h)
            A = matrix(A) if A is not None else None
            b = matrix(b) if b is not None else None
            sol = lp(c, G, h, A, b)
            if sol['status'] != 'optimal':
                warn('no feasible solution found')
            else:
                return sol

    def check_solver(self, solver):
        if self.solver == 'cvxopt':
            from cvxopt import matrix
        else:
            pass