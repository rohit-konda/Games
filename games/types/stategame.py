#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from games.types.boardgame import Board, BoardGame, BoardPlayer


class StatePlayer(BoardPlayer):
    def __init__(self, name, index, actions, state):
        BoardPlayer.__init__(self, name, index, actions)
        self.state = state


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


