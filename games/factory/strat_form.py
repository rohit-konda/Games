class SGFactory(GFactory):
    def make_game(payoffs):
        self._check_game(payoffs)
        board = Board(0)
        players = [self._make_player(i, pay) for i, pay in enumerate(payoffs)]

    def _make_player(i, payoff):
        actions = [Action(str(i) + str(ind), ind) for ind in range(np.shape(payoffs)[i])] 
        def util(board, play):
            play = sort(play, key=lambda x : x.index)
            return payoff[tuple(play)]
        return Player(str(i), i, actions, util)

    def _check_game(self, payoffs):
        if not [isinstance(pay, np.array) for pay in payoffs].all():
            raise ValueError('payoffs must be a numpy array')
        if not [shape(pay) == shape(payoffs[0]) for pay in payoffs].all(): 
            raise ValueError('payoff matrices must be the same shape')


def game_to_payoffs(game):
    #### NEED TO DO ####
    payoffs = [None]*self.N
    for i in :
        payoff_i = np.zeros(self.num_act)
        # generate all possible types of action indices
        for a in product(*[range(n_i) for n_i in self.num_act]):
            payoff_i[a] = self.U(i, list(a))
        payoffs[i] = payoff_i
    return payoffs