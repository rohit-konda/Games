#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from games.types.game import Game, Player
from games.types.factory import GFactory


class BGFactory(GFactory):
    @classmethod
    def _make_board(cls, *args):
        pass


class BoardGame(Game):
    def __init__(self, players, board):
        Game.__init__(self, players)
        self.board = board

    def move(self, play, *args):
        [p.move(self.all_play(play), self.board.state) for p in self.players]
        self.board.move(all_play)

    def U_i(self, i, play, *args):
        all_play = [p.actions(play[p.index], self.board) for p in self.players]
        return self.players[i].U(all_play, self.board)


class BoardPlayer(Player):
    def __init__(self, name, index, actions):
        Player.__init__(self, name, index, actions)

    def move(self, actions, boardstate=None, *args):
        raise NotImplementedError

    def U(self, actions, boardstate=None, *args):
        raise NotImplementedError


class Board:
    def __init__(self, state):
        self.state = state

    def move(self, actions, *args):
        pass

    def __str__(self):
        return str(self.state)

    def __repr__(self):
        return self.__class__.__name__ + '({})'.format(repr(self.state))


class RepeatBoard(Board):
    def __init__(self):
        Board.__init__(self, 0)

    def move(self, actions):
        self.state += 1
