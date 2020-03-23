class Eq:
    pass


class DomEq(Eq):
	def __init__(self, play):
		self.play = play


class NashEq(Eq):
    def __init__(self, play):
        self.play = play


class MixedNashEq(Eq):
	pass


class CorrelatedEq(Eq):
	pass


class CoarseCorrelated(Eq):
	pass