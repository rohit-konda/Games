class _Indexed:
    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val


class _Tagged:
    def __init__(self, tag):
        self._tag = tag


    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, val):
        self._tag = val


class Action(_Tagged, _Indexed):
    def __init__(self, tag, index):
        _Tagged.__init__(self, tag)
        _Indexed.__init__(self, index)

    def __repr__(self):
        return self._tag


class Player(_Tagged, _Indexed):
    def __init__(self, tag, index, actions, util):
        _Tagged.__init__(self, tag)
        _Indexed.__init__(self, index)
        self._actions = actions
        self._util = util

    def U(self, board, play):
        self._util(board, play)

    def move(self, board, play):
        pass

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, val):
        self._actions = actions


class Eq:
    pass


class NashEq(Eq):
    def __init__(self, play):
        self.play = play


class GFactory(ABC):

    @abstractmethod
    def make_game(self, *args):
        self._check_game(*args)
        return Game(*args)

    @abstractmethod
    def _check_game(self, *args):
        pass


class Game:
    def __init__(self, players, board):
        self.players = sort(players, key=lambda x : x.index)
        self.board = board
        self.N = len(players)
        self.actions = [p.actions for p in self.players]

    def move(self, play):
        [p.move(self.board, play) for p in players]
        self.board.move()




class Board:
    def __init__(self, state):
        self.state = state

    def move(self, play):
        pass


class WelfareGame(Game):
    def __init__(self, players, board, welfare):
        pass


class PotentialGame(Game):
    def __init__(self, players, board, welfare):
        pass



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

def set_poas(self):
    """ calculate price of anarchy and price of stability
    from all pure nash and social optimum

    Note:
        setter method for self.poa & self.pos

    Raises:
        ValueError: if self.welfare or self.pnes is None
    """
    if self.welfare is None:
        raise ValueError('must set value of self.welfare')

    if self.pnes is None:
        raise ValueError('must set value of self.pnes')

    pne_welfare = np.array([self.welfare[pne] for pne in self.pnes], dtype='float')
    price_ratios = list(pne_welfare/self.welfare[self.opt])
    self.poa, pos = min(price_ratios), max(price_ratios)

def set_opt(self):
    """ find action that maximizes welfare

    Note:
        setter method for self.opt

    Raises:
        ValueError: if self.welfare is None
    """
    if self.welfare is None:
        raise ValueError('must set value of self.welfare')

    self.opt = np.unravel_index(np.argmax(self.welfare), self.welfare.shape)

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