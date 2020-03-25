from games.types.game import Board, Game
from games.types.players import FActions, Player
from games.types.factory import GFactory


class SGFactory(GFactory):
    def make_game(cls, payoffs):
        cls._check_game(*payoffs)
        board = cls._make_board()
        players = [cls._make_player(i, pay) for i, pay in enumerate(payoffs)]
        return Game(players, board)

    def _make_player(cls, ind, payoff):
        actions = FActions(str(ind), [i for i in range(np.shape(payoffs)[i])])
        def util(board, play):
            return payoff[tuple(play)]
        return Player(str(ind), ind, actions, util)

    def _make_board(cls):
        return Board(None)

    def _check_game(cls, payoffs):
        if not [isinstance(pay, np.array) for pay in payoffs].all():
            raise ValueError('payoffs must be a numpy array')
        if not [shape(pay) == shape(payoffs[0]) for pay in payoffs].all(): 
            raise ValueError('payoff matrices must be the same shape')


def game_to_payoffs(game):
    if not isinstance(game.players[0].actions, FActions):
        raise ValueError('action set must be of type FActions')

    num_act = [len(p.actions) for p in game.players]
    payoffs = [None]*game.N
    for i, player in enumerate(game.players):
        payoff_i = np.zeros(num_act)
        # generate all possible types of action indices
        for a in product(*[range(n_i) for n_i in num_act]):
            payoff_i[a] = player.U(list(a))
        payoffs[i] = payoff_i
    return payoffs
