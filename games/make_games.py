from games.types.strategic import SGFactory
#from games.types.congestion import CongestionFactory


def payoff_game(payoffs):
	return SGFactory().make_game(payoffs)

def congestion_game():
	return CongestionFactory().make_game()