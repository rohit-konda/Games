

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
        self.actions = [p.actions for p in self.players]

    def move(self, play):
        [p.move(self.board, play) for p in players]
        self.board.move()


class WelfareGame(Game):
    def __init__(self, players, board, welfare):
        pass


class PotentialGame(Game):
    def __init__(self, players, board, welfare):
        pass