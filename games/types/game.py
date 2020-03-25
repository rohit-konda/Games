from games.types.players import *
import warnings

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
        [p.move(play, self.board) for p in self.players]
        self.board.move(play)

    def U_i(self, i, play):
        return self.players[i].U(play, self.board)

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, players):
        warnings.warn('Changing the players may produce an error in the game. Create a new game instead.')
        self._players = players

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        warnings.warn('Changing the board may produce an error in the game. Create a new game instead.')
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

    def welfare(self, board, play):
        return self._welfare(board, play)


class PotentialGame(WelfareGame):
    def __init__(self, players, board, potential, welfare=None):
        if welfare is None:
            WelfareGame.__init__(self, players, board, potential)
        else:
            WelfareGame.__init__(self, players, board, welfare)
        self._potential = potential

    def potential(self, board, play):
        return self._potential(board, play)
