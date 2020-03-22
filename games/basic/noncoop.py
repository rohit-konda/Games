#!/usr/bin/env python
"""

Author : Rohit Konda
Copyright (c) 2020 Rohit Konda. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for full license information.

Summary:
    Class definitions for noncooperative games with finite number of players and real payoffs.
"""

from games._abc import *


class FPSet(PSet):
    """
    Finite list of players.
    
    Attributes:
        _inner_list (list): finite list of players
    """
    def __init__(self, players):
        PSet.__init__(self)
        self._inner_list = list(players)

    def __contains__(item):
        return self._inner_list.__contains__(item)

    def __getitem__(item):
        return self._inner_list.__getitem__(item)

    def __iter__(self):
        return self._inner_list.__iter__()

    def __len__(self):
        return self._inner_list.__len__()

    def __repr__(self):
        return self._inner_list.__repr__()


class FAction(Action):
    """
    Attributes:
        _players (PSet): the set of players.
    """
    
    def __init__(self, players):
        self._players = players

    def __getitem__(self, pl):
        """ gives action played by player pl

        Args:
            pl (Player): which player.

        Raises:
            ValueError: if player pl is not in Pset

        Returns:
            (Ac): action enacted by player pl
        """
        Action.__getitem__(pl)


class RPay(float):
    """
    Abstract class for a payoff.
    Should follow the Von Neumann and
    Morgenstern axioms for utility.

    Attributes:
        _value: value of the payoff
    """

    def __new__(cls, value):
        i = float.__new__(cls)
        i._value = value
        return i


class NonCoopGame(Game):
    """
    Class definition for a finite player, finite strategy set game

    Attributes:
        players (FPSet): set of players
        N (int): number of players in the game.
    """

    def __init__(self, players):
        Game.__init__(self, players)
        self.N = len(players)
        self.eq = None