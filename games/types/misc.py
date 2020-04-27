from games.types.game import Game, Actions, Player


class WelfareGame(Game):
    def __init__(self, players):
        Game.__init__(self, players)

    def welfare(self, play, *args):
        raise NotImplementedError


class PotentialGame(Game):
    def __init__(self, players):
        Game.__init__(self, players)

    def potential(self, play, *args):
        raise NotImplementedError


class FActions(Actions):
    def __init__(self, actions):
        self.actions = actions

    def __call__(self, action):
        return self.actions[action]

    def __getitem__(self, item):
        return self.actions.__getitem__(item)

    def __iter__(self):
        return self.actions.__iter__()

    def __len__(self):
        return len(self.actions)

    def __repr__(self):
        return 'FActions({})'.format(str(self.actions)[1:-1])


class MutablePlayer(Player):
    def __init__(self, name, index, actions, util):
        Player.__init__(self, name, index, actions)
        self._util = util 

    def U(self, play, *args):
        return self._util(play, *args)


