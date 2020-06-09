#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from games.types.game import Player, Game


class StatePlayer(Player):
    def __init__(self, name, index, actions, state, time=0):
        Player.__init__(self, name, index, actions)
        self.state = state
        self.time = time

    def Fi(self, actions, states):
        pass

    def move(self, actions, states):
        self.time += 1
        self.state = self.Fi(actions, states)

    def U(self, actions, states, *args):
        pass

    def play(self, states, *args):
        pass


class StateGame(Game):
    def __init__(self, players):
        Game.__init__(self, players)

    def move(self, play, *args):
        actions = self.all_play(play)
        states = self.agg_state()
        for p in self.players:
            p.move(actions, states)

    def U_i(self, i, play, *args):
        actions = self.all_play(play)
        states = self.agg_state()
        return self.players[i].U(actions, states)

    def agg_state(self):
        return [p.state for p in self.players]

    def agg_play(self):
        states = self.agg_state()
        return [p.play(states) for p in self.players]
