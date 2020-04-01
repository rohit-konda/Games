class Eq:
    pass


class DomEq(Eq):
	def __init__(self, play):
		self.play = play


class PureEq(Eq):
    def __init__(self, play):
        self.play = play


class MixedEq(Eq):
	pass


class CorrelatedEq(Eq):
	pass


class CoarseEq(Eq):
	pass