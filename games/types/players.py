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
        raise ValueError('Name shouldn\'t change, define a new FActions instead.')

    def __len__(self):
        return len(self.actions)

    def __repr__(self):
        return str(self.actions)[1:-1]


class Player:
    def __init__(self, name, index, actions, util):
        self._name = name
        self._index = index
        if isinstance(actions, Actions):
            self._actions = actions
        else:
            raise TypeError('actions must be of type Actions')
        self._util = util

    def U(self, play, board):
        return self._util(play, board)

    def move(self, play, board):
        pass

    def __repr__(self):
        return '{} : player {} \n  actions : {}'.format(self.name, self.index, self.actions)

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, actions):
        raise ValueError('Actions shouldn\'t change, define a new player instead.')

    @property
    def util(self):
        return self.U

    @util.setter
    def util(self, util):
        raise ValueError('Utility function shouldn\'t change, define a new player instead.')

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, index):
        raise ValueError('Index shouldn\'t change, define a new player instead.')

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, name):
        raise ValueError('Name shouldn\'t change, define a new player instead.')

