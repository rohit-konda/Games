    





    def set_sec(self):
        """ set pure security values and policies """
        max_first = np.max(self.payoffs[0], 1)
        V_underbar = np.min(max_first)
        p1_policy = np.nonzero(max_first == V_underbar)[0].tolist()
        min_first = np.min(self.payoffs[0], 0)
        V_overbar = np.max(min_first)
        p2_policy = np.nonzero(min_first == V_overbar)[0].tolist()
        self.sec = [(V_underbar, p1_policy), (V_overbar, p2_policy)]

    def set_msec(self):
        """ set mixed security values and policies """
        n = len(self.strategies[0])
        m = len(self.strategies[1])
        O_n = np.ones((n, 1))
        O_m = np.ones((m, 1))
        Z_n = np.zeros((n, 1))
        Z_m = np.zeros((m, 1))
        I_n = np.identity(n)
        I_m = np.identity(m)
        P = self.payoffs[1]
        
        # get security policy for player 1
        c_n = matrix(np.hstack((np.array([1]), np.zeros((n,)))))
        G_n = matrix(np.vstack((np.hstack((-O_m, P.T)), np.hstack((Z_n, -I_n)))))
        h_n = matrix(np.vstack((Z_m, Z_n)))
        A_n = matrix(np.hstack((np.array([[0]]), O_n.T)))
        b_n = matrix(np.array([1.]))
        sol_n = solvers.lp(c_n, G_n, h_n, A_n, b_n)
        
        # get security policy for player 2
        c_m = matrix(np.hstack((np.array([-1]), np.zeros((m,)))))
        G_m = matrix(np.vstack((np.hstack((O_n, -P)), np.hstack((Z_m, -I_m)))))
        h_m = matrix(np.vstack((Z_n, Z_m)))
        A_m = matrix(np.hstack((np.array([[0]]), O_m.T)))
        b_m = matrix(np.array([1.]))
        sol_m = solvers.lp(c_m, G_m, h_m, A_m, b_m)

        self.msec = (sol_n['x'][0], sol_n['x'][1:], sol_m['x'][1:])