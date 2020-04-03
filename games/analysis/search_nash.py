
import numpy as np
from itertools import product
from games.types.equilibrium import PureEq
from games.types.game import NCGame


class BruteNash:
    TOLERANCE = 10**-8

    def find_NCnash(cls, game):
        return find_nash(game_to_payoffs(game))

    def game_to_payoffs(cls, game):
        if not isinstance(game, NCGame):
            raise ValueError('game must be of type NCGame')

        num_act = [len(p.actions) for p in game.players]
        payoffs = [None]*game.N
        for i, player in enumerate(game.players):
            payoff_i = np.zeros(num_act)
            # generate all possible types of action indices
            for a in product(*[range(n_i) for n_i in num_act]):
                play = [game.players[j].actions[k] for j, k in enumerate(a)]
                payoff_i[a] = game.U_i(i, play)
            payoffs[i] = payoff_i
        return payoffs

    def find_nash(cls, payoffs):
        cpnes = list(np.argwhere(payoffs[0] > np.amax(payoffs[0], 0) - cls.TOLERANCE))
        cpnes = [tuple(cpne) for cpne in cpnes]
        N = len(payoffs)
        
        for i in range(1, N):
            pm = payoffs[i]
            for cpne in cpnes[:]:
                ind = cpne[:i] + (slice(None),) + cpne[i+1:]
                if pm[cpne] < np.max(pm[ind]) - cls.TOLERANCE:
                    cpnes.pop(cpnes.index(cpne))
        
        return [PureEq(cpne) for cpne in cpnes]


class BrutePoA:
    def game_to_welfare(cls, game):
        if not isinstance(game, WelfareGame):
            raise ValueError('game must be of type WelfareGame')

        num_act = [len(p.actions) for p in game.players]
        welfare = np.zeros(num_act)
        # generate all possible types of action indices
        for a in product(*[range(n_i) for n_i in num_act]):
            play = [game.players[i].actions[j] for i, j in enumerate(a)]
            welfare[a] = game.welfare(play)
        return welfare

    def set_poas(cls, list_pureeq, welfare):
        pne_welfare = [welfare[pne.play] for pne in list_pureeq]
        opt = welfare[cls.get_opt(welfare)]
        price_ratios = [float(pne)/opt for pne in pne_welfare]
        return min(price_ratios), max(price_ratios)

    def get_opt(cls, welfare): return np.unravel_index(np.argmax(welfare), welfare.shape)
