

class CongestionFactory(GFactory):
	def _make_players()




def U_i(self, i, strategy):
    """ utility for the strategy for player i """
    strategy_i = list(strategy[i])
    p_cover = self.player_cover(strategy)
    return sum([self.f_r(i, j, p_cover[j]) for j in strategy_i])

def f_r(self, i, res, players):
    """ function design for the utility function depends on what resource,
    and what players are covering it """
    pass

self.w = w  # w(j) welfare basis function ((n+1,) np.array)
self.f = f  # f(j) design function for the utility ((n+1,) np.array)

self.values = values  # values (v_r) associated with each resource

Wr = np.dot(np.diag(values), np.array([w] * len(values)))  # Wr(j) = v_r * w(j)
Fr = np.dot(np.diag(values), np.array([f] * len(values)))  # Fr(j) = v_r * f(j)

def w_r(self, res, players):
    """ welfare function, returns a scalar value dependent on the resource and which players select it """
    pass
