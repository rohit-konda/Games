from games.types.game import *
from games.types.players import Player, FActions
import unittest as ut
import numpy as np


class Game_Test(ut.TestCase):
	def game1(self):
		class BoardMove(Board):
			def __init__(self):
				Board.__init__(self, 0)

			def move(self, play):
			    self.state += 1

		class PlayerMoving(Player):
			def __init__(self, name, index, actions, util):
				Player.__init__(self, name, index, actions, util)
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
		players = [Player('0', 0, Actions(), util), Player('1', 1, Actions(), util)]
		players2 = [Player('0', 0, Actions(), util), Player('1', 2, Actions(), util)]
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

if __name__ == '__main__':
	ut.main()