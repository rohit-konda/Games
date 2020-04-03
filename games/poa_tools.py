    self.lp_solver(c, G, h)
    poa = 1./self.sol['primal objective']
    f = [0.] + list(sol['x'])[1:]
    return (poa, f)



    self.lp_solver(c, G, h)
    return 1./self.sol['primal objective']

    self.lp_solver(c, G, h, A, b)
    game = self.worst_case(self.sol['x']) # worst case game instance
    return -1./self.sol['primal objective'], game