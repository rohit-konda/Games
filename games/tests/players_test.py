from games.types.players import *
import unittest as ut


class TestPlayers(ut.TestCase):
	def test_player(self):
		name = 'test'
		index = 0
		actions = Actions()
		def util(play, board):
			return play[0]
		player = FluidPlayer(name, index, actions, util)
		play, board = [0], None
		self.assertEqual(player.U(play, board), 0)
		self.assertIsNone(player.move(play, board))

		def wrongaction(): Player(name, index, None, util)
		self.assertRaises(TypeError, wrongaction)

		def changename(): player.name = None
		def changeaction(): player.actions = None
		def changeindex(): player.index = None
		def changeutil(): player.util = None
		self.assertRaises(ValueError, changename)
		self.assertRaises(ValueError, changeaction)
		self.assertRaises(ValueError, changeindex)
		self.assertRaises(ValueError, changeutil)

class TestFActions(ut.TestCase):
	def test_FActions(self):
		name = 'p1'
		actions = [1, 2]
		fact = FActions(name, actions)
		self.assertEqual(fact(0, None), 1)
		self.assertEqual(fact[0], 1)
		self.assertEqual([i for i in fact], actions)
		self.assertEqual(fact.name, 'p1')
		self.assertEqual(len(fact), 2)

		def testequaler(): fact.name = None
		self.assertRaises(ValueError, testequaler)
		self.assertRaises(IndexError, fact, 2, None)

if __name__ == '__main__':
	ut.main()