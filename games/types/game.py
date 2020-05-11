class Game:
    def __init__(self, players):
        self.players = players
        self.N = len(players)
        self.eq = []

    def all_play(self, play):
        return [p.actions(play[p.index]) for p in self.players]

    def U_i(self, i, play, *args):
        return self.players[i].U(self.all_play(play))

    def actions(self):
        return [p.actions for p in self.players]

    def __str__(self):
        players_str = map(str, self.players)
        return self.__class__.__name__ + '(players: {})'.format(', '.join(players_str))

    def __repr__(self):
        players_str = map(repr, self.players)
        eq_str = map(repr, self.eq)
        return self.__class__.__name__ + '(players: [{}], eq: [{}])'.format(', '.join(players_str), ', '.join(eq_str))


class Player:
    def __init__(self, name, index, actions):
        self.name = name
        self.index = index
        self.actions = actions

    def U(self, play, *args):
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + '({}: {})'.format(self.index, self.name)

    def __repr__(self):
        return self.__class__.__name__ + '(index: {}, name: {}, actions: {})'.format(self.index, self.name, repr(self.actions))


class Actions:
    def __call__(self, action, *args):
        raise NotImplementedError


class Eq:
    def __init__(self, play):
        self.play = play

    def __repr__(self):
        return self.__class__.__name__ + '({})'.format(repr(self.play))