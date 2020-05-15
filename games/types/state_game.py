from games.types.board_game import Board, BoardGame, BoardPlayer

class StateBoard(Board):
    def __init__(self, state, time=0):
        Board.__init__(self, state)
        self.time = time

    def f(self, play):
    	pass

    def move(self, play):
        self.time += 1
        self.state = self.f(play)

class MutableStateBoard(StateBoard):
	def __init__(self, state, f, time=0):
		StateBoard.__init__(self, state, time)
		self._f = f

	def f(self, play):
		return self._f(self.state, play)


