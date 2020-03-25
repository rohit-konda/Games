def game_to_payoffs(game):
    if not isinstance(game, NCGame):
        raise ValueError('game must be of type NCGame')

    num_act = [len(p.actions) for p in game.players]
    payoffs = [None]*game.N
    for i, player in enumerate(game.players):
        payoff_i = np.zeros(num_act)
        # generate all possible types of action indices
        for a in product(*[range(n_i) for n_i in num_act]):
            play = [game.players[i].actions[j] for i, j in enumerate(a)]
            payoff_i[a] = game.U_i(i, play)
        payoffs[i] = payoff_i
    return payoffs

def find_eq(payoffs):
    tolerance = 10**-8  # numerical tolerance for comparing floats
    # candidate pure nash equilibria
    cpnes = list(np.argwhere(payoffs[0] > np.amax(payoffs[0], 0) - tolerance))
    cpnes = [tuple(cpne) for cpne in cpnes]
    for i in range(1, self.N):
        pm = payoffs[i]
        for cpne in cpnes[:]:
            ind = cpne[:i] + (slice(None),) + cpne[i+1:]
            if pm[cpne] < np.max(pm[ind]) - tolerance:
                cpnes.pop(cpnes.index(cpne))
    return cpnes