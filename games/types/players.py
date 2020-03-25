import warnings

class Actions:
    def __call__(self, action, board):
        pass


class FActions(Actions):
    def __init__(self, name, actions):
        self._name = name
        self.actions = actions

    def __call__(self, action, board):
        try:
            ac = self.actions[action]
        except IndexError:
            raise IndexError('Player {} does not have this action available'.format(self.name))
        return ac

    def __getitem__(self, item):
        return self.actions.__getitem__(item)

    def __iter__(self):
        return self.actions.__iter__()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        warnings.warn('Changing name, this should match the corresonding player.')
        self._name = name

    def __len__(self):
        return len(self.actions)


class Player:
    def __init__(self, name, index, actions, util):
        self.name = name
        self.index = index
        self.actions = actions
        self._util = util

    def U(self, play, board):
        return self._util(play, board)

    def move(self, play, board):
        self.actions(play[self.index], board)
