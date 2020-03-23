class Actions:
    def __call__(self, action, board):
        pass




class FActions(Actions):
    def __init__(self, name, actions):
        self.name = name
        self.actions = actions

    def __call__(self, action, board):
        try:
            ac = self.actions[action]
        except IndexError:
            raise IndexError('Player {} does not have this action available'.format(self.name))
        return ac

    def __len__(self):
        return len(self.actions)


class Player(_Tagged, _Indexed):
    def __init__(self, name, index, actions, util):
        self.name = name
        self.index = index
        self.actions = actions
        self._util = util

    def U(self, play, board):
        self._util(play, board)

    def move(self, play, board):
        self.actions.move(play[self.index], board)
