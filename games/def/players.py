class _Indexed:
    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        return self._index

    @index.setter
    def index(self, val):
        self._index = val


class _Tagged:
    def __init__(self, tag):
        self._tag = tag

    @property
    def tag(self):
        return self._tag

    @tag.setter
    def tag(self, val):
        self._tag = val


class Action(_Tagged, _Indexed):
    def __init__(self, tag, index):
        _Tagged.__init__(self, tag)
        _Indexed.__init__(self, index)

    def __repr__(self):
        return str(self._tag)

class Actions:
    def move(self, action):
        pass


class Player(_Tagged, _Indexed):
    def __init__(self, tag, index, actions, util):
        _Tagged.__init__(self, tag)
        _Indexed.__init__(self, index)
        self._actions = actions
        self._util = util

    def U(self, board, play):
        self._util(board, play)

    def move(self, board, play):
        self._actions.move(play[self._index])

    @property
    def actions(self):
        return self._actions

    @actions.setter
    def actions(self, val):
        self._actions = actions
