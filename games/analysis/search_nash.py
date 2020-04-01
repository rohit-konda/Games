from games.types.equilibrium import PureEq

def find_NCnash(game):
    return find_nash(game_to_payoffs(game))

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

def find_nash(payoffs):
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


def set_poas(self):
    if self.welfare is None:
        raise ValueError('must set value of self.welfare')

    if self.pnes is None:
        raise ValueError('must set value of self.pnes')

    pne_welfare = np.array([self.welfare[pne] for pne in self.pnes], dtype='float')
    price_ratios = list(pne_welfare/self.welfare[self.opt])
    self.poa, pos = min(price_ratios), max(price_ratios)

def set_opt(self):
    if self.welfare is None:
        raise ValueError('must set value of self.welfare')

    self.opt = np.unravel_index(np.argmax(self.welfare), self.welfare.shape)

def player_cover(self, strategies):
    return [[j for j in range(self.n) if i in strategies[j]] for i in range(self.r_m)]

def set_s_payoff(self):
    sp_dict = {}
    for k, v in self.st_dict.items():
        p_cover = self.player_cover(v)
        value = sum([self.w_r(i, p_cover[i]) for i in range(self.r_m)])
        sp_dict.update({k: value})
    self.s_payoff = np.array(dict_nlist(sp_dict))
