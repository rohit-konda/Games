from games.types.game import *
from games.types.misc import FActions
import unittest as ut
import numpy as np


class Game_Test(ut.TestCase):
	class ZeroPlayer(Player):
		def __init__(self, name, index):
			Player.__init__(self, name, index, FActions([0]))

		def U(self, play):
			return 0

	def test_actions(self):
		actions = Actions()
		self.assertRaises(NotImplementedError, actions, None)

	def test_players(self):
		player = Player(None, None, None)
		self.assertRaises(NotImplementedError, player.U, None)
		zero = self.ZeroPlayer('zero', 0)
		self.assertEqual(zero.U(None), 0)
		self.assertEqual(str(zero), 'ZeroPlayer(0: zero)')
		self.assertEqual(repr(zero), 'ZeroPlayer(index: 0, name: zero, actions: FActions(0))')
	
	def test_game(self):
		z1 = self.ZeroPlayer('zero', 0)
		z2 = self.ZeroPlayer('one', 1)
		z3 = self.ZeroPlayer('two', 2)
		game = Game([z1, z2, z3])
		self.assertEqual(game.N, 3)
		self.assertEqual(game.U_i(0, [0, 0, 0]), 0)
		self.assertEqual(str(game.actions()), '[FActions(0), FActions(0), FActions(0)]')
		self.assertEqual(str(game), 'Game(players: ZeroPlayer(0: zero), ZeroPlayer(1: one), ZeroPlayer(2: two))')
		self.assertEqual(repr(game), 'Game(players: [ZeroPlayer(index: 0, name: zero, actions: FActions(0)), ZeroPlayer(index: 1, name: one, actions: FActions(0)), ZeroPlayer(index: 2, name: two, actions: FActions(0))], eq: [])')

	def test_eq(self):
		eq = Eq(0)
		self.assertEqual(str(eq), 'Eq(0)')

'''
class Game_Test(ut.TestCase):
	def game1(self):
		class BoardMove(Board):
			def __init__(self):
				Board.__init__(self, 0)

			def move(self, play):
			    self.state += 1

		class PlayerMoving(FluidPlayer):
			def __init__(self, name, index, actions, util):
				FluidPlayer.__init__(self, name, index, actions, util)
				self.hasMoved = False

			def move(self, play, board):
			    self.hasMoved = True

		def util1(play, board): return play[0] + board.state
		def util2(play, board): return play[1] + board.state
		player1 = PlayerMoving('1', 0, FActions('1', [1, 2]), util1)
		player2 = PlayerMoving('2', 1, FActions('2', [3, 4]), util2)
		return Game([player2, player1], BoardMove())

	def test_game1(self):
		game = self.game1()

		self.assertEqual(game.get_players(), ['1', '2'])
		self.assertEqual(game.N, 2)
		self.assertEqual(game.get_board(), '0')
		self.assertEqual(game.get_actions(), ['1, 2', '3, 4'])

		self.assertEqual(game.U_i(0, [0, 0]), 1)
		self.assertEqual(game.U_i(0, [1, 0]), 2)
		self.assertEqual(game.U_i(1, [0, 0]), 3)
		self.assertEqual(game.U_i(1, [0, 1]), 4)
		self.assertEqual(game.players[0].hasMoved, False)

		game.move([0, 0])

		self.assertEqual(game.U_i(0, [0, 0]), 2)
		self.assertEqual(game.U_i(0, [1, 0]), 3)
		self.assertEqual(game.U_i(1, [0, 0]), 4)
		self.assertEqual(game.U_i(1, [0, 1]), 5)
		self.assertEqual(game._players[0].hasMoved, True)

		self.assertEqual(game.get_board(), '1')
		
		def changeN(): game.N = None
		def changeplayers(): game.players = []
		def changeboard(): game.board = None
		self.assertRaises(ValueError, changeN)
		self.assertRaises(ValueError, changeplayers)
		self.assertRaises(ValueError, changeboard)

	def test_check(self):
		def util(play, board):
			return play[0]
		players = [FluidPlayer('0', 0, Actions(), util), FluidPlayer('1', 1, Actions(), util)]
		players2 = [FluidPlayer('0', 0, Actions(), util), FluidPlayer('1', 2, Actions(), util)]
		def setnullgame(): Game(None, None)
		def setnullboard(): Game(players, None)
		def setnullplayers(): Game([], Board(None))
		def setwrongplayers(): Game([None, None], Board(None))
		def setwrongindex(): Game(players2, Board(None))
		self.assertRaises(TypeError, setnullgame)
		self.assertRaises(TypeError, setnullboard)
		self.assertRaises(ValueError, setnullplayers)
		self.assertRaises(TypeError, setwrongplayers)
		self.assertRaises(ValueError, setwrongindex)
'''

if __name__ == '__main__':
	ut.main()