from games.types.players import *
from warnings import warn

class Board:
    def __init__(self, state):
        self.state = state

    def move(self, play):
        pass


class Game:
    def __init__(self, players, board):
        self._players = sorted(players, key=lambda x : x.index)
        self._board = board
        self._N = len(players)

    def move(self, play):
        [p.move(play, self.board) for p in self._players]
        self.board.move(play)

    def U_i(self, i, play):
        return self._players[i].U(play, self.board)

    def actions(self):
        return [p.actions for p in self._players]

    @property
    def players(self):
        return [str(p) for p in self._players]

    @players.setter
    def players(self, players):
        warn('Changing the players may produce an error in the game. Create a new game instead.')
        self._players = players
        self._N = len(players)

    @property
    def board(self):
        return str(self._board)

    @board.setter
    def board(self, board):
        warn('Changing the board may produce an error in the game. Create a new game instead.')
        self._board = board

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, N):
        raise ValueError('N should match the number of players')

class NCGame(Game):
    def __init__(self, players, board):
        Game.__init__(self, players, board)


class WelfareGame(Game):
    def __init__(self, players, board, welfare):
        Game.__init__(self, players, board)
        self._welfare = welfare

    def welfare(self, play, board):
        return self._welfare(play, board)


class PotentialGame(WelfareGame):
    def __init__(self, players, board, potential, welfare=None):
        if welfare is None:
            WelfareGame.__init__(self, players, board, potential)
        else:
            WelfareGame.__init__(self, players, board, welfare)
        self._potential = potential

    def potential(self, play, board):
        return self._potential(play, board)
