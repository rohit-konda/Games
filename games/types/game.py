from games.types.players import *

class Board:
    def __init__(self, state):
        self.state = state

    def move(self, play):
        pass


class Game:
    def __init__(self, players, board):
        self.players = sort(players, key=lambda x : x.index)
        self.board = board
        self.N = len(players)

    def move(self, play):
        [p.move(self.board, play) for p in players]
        self.board.move()


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

