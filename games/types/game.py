from games.types.players import *

class Board:
    def __init__(self, state):
        self.state = state

    def move(self, play):
        pass

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return repr(self.state)


class RepeatBoard(Board):
    def __init__(self):
        Board.__init__(self, 0)

    def move(self, play):
        self.state += 1


class Game:
    def __init__(self, players, board):
        self._players = players
        self._board = board
        self._N = len(players)
        self.eq = []
        self._check()

    def _check(self):
        try:
            iter(self._players)
            if len(self._players) == 0:
                raise ValueError('Player list is empty.')
        except TypeError:
            raise TypeError('self.players must be iterable.')
        if not isinstance(self._board, Board):
            raise TypeError('Board must be of type games.types.Board.')
        if not all([isinstance(p, Player) for p in self._players]):
            raise TypeError('Players must contain players of type games.types.players.Player.')

        self._players = sorted(self._players, key=lambda x : x.index)
        if [p.index for p in self._players] != [i for i in range(self._N)]:
            raise ValueError('Player\'s indices must be from 0 to the number of players')

    def move(self, play):
        [p.move(play, self._board) for p in self._players]
        self._board.move(play)

    def U_i(self, i, play):
        all_play = [p.actions(play[p.index], self._board) for p in self._players]
        return self._players[i].U(all_play, self._board)

    def actions(self):
        return [p.actions for p in self._players]

    def get_actions(self):
        return [str(p.actions) for p in self._players]

    def get_players(self):
        return [str(p) for p in self._players]

    def get_board(self):
        return str(self._board)

    def __str__(self):
        return self.__name__ + '(state : {}, players: {}.)'.format(str(self._board), ' '.join(self.get_players()))

    def __repr__(self):
        rep = self.__name__ + 'with \nstate : \n{} \nand {} players:'.format(repr(self._board), self._N)
        return rep + ''.join(['\n' + repr(p) for p in self._players])

    @property
    def players(self):
        return self._players

    @players.setter
    def players(self, players):
        raise ValueError('Can\'t change the players in the game. Create a new game instead.')

    @property
    def board(self):
        return self._board

    @board.setter
    def board(self, board):
        raise ValueError('Can\'t change the board in the game. Create a new game instead.')

    @property
    def N(self):
        return self._N

    @N.setter
    def N(self, N):
        raise ValueError('N should match the number of players')

class NCGame(Game):
    def __init__(self, players):
        Game.__init__(self, players, Board(None))

    def __str__(self):
        return self.__name__ + '({} players)'.format(str(self._board), self._N)


class WelfareGame(Game):
    def __init__(self, players, board):
        Game.__init__(self, players, board)

    def welfare(self, play, board):
        raise NotImplementedError


class PotentialGame(WelfareGame):
    def __init__(self, players, board):
        WelfareGame.__init__(self, players, board)

    def potential(self, play, board):
        raise NotImplementedError

    def welfare(self, play, board):
        return self.potential(play, board)