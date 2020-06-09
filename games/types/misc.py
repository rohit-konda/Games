#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Miscellaneous class definitions and functions that are useful for creating games.
"""
from games.types.game import Game, Actions, Player
from typing import List, Callable, Union, Any
from itertools import product
import numpy as np

class WelfareGame(Game):

    """ Game endowed with a system welfare function.
    Convention is larger welfare is better.

    Args:
        players (List[Player]): List of players defining the game interactions.
    """

    def __init__(self, players: List[Player]):
        Game.__init__(self, players)

    def welfare(self, play: list, *args) -> Union[float, Any]:
        """Welfare function.

        Args:
            play (list): Which indexes of actions are played by each player.
            *args: Here for extendability of the class.

        Returns:
            Union[float, Any]: Welfare of the system.

        Raises:
            NotImplementedError: Needs to be implemented.
        """
        raise NotImplementedError


class PotentialGame(Game):

    """Potential Game endowed with a potential function.

    Args:
        players (List[Player]): List of players defining the game interactions.
    """

    def __init__(self, players: List[Player]):
        Game.__init__(self, players)

    def potential(self, play: list, *args) -> float:
        """Potential function.

        Args:
            play (list): Which indexes of actions are played by each player.
            *args: Here for extendability of the class.

        Returns:
            float: Potential of the game.

        Raises:
            NotImplementedError: Needs to be implemented.
        """
        raise NotImplementedError


class FActions(Actions):

    """Wrapper for a finite action set using a list.

    Args:
        actions (list): Available actions to a player.

    Attributes:
        actions (list): Available actions to a player.
    """

    def __init__(self, actions: list):
        self.actions: list = actions

    def __call__(self, play: int) -> Any:
        return self.actions[play]

    def __getitem__(self, item: Any) -> Any:
        return self.actions.__getitem__(item)

    def __iter__(self) -> Any:
        return self.actions.__iter__()

    def __len__(self) -> Any:
        return len(self.actions)

    def __repr__(self) -> str:
        return 'FActions({})'.format(str(self.actions)[1:-1])


class MutablePlayer(Player):

    """Player with utility function as a object parameter.

    Args:
        name (str): Label for the player.
        index (int): Index for the player for easy reference in a list of players in a game.
        actions (Actions): Actions object that the player can take.
        util (Callable[..., Union[float, Any]]): Prescribed utility function for the player.
    """

    def __init__(self, name: str, index: int, actions: Actions, util: Callable[..., Union[float, Any]]):
        Player.__init__(self, name, index, actions)
        self._util: Callable[..., Union[float, Any]] = util

    def U(self, actions: list, *args) -> Union[float, Any]:
        """ Utility function that should follow the von Neumann - Morgenstern axioms.
        Outlines preferences of own actions based on what actions othe rplayers have taken.

        Args:
            actions (list): List of actions that each player in the game has taken.
            *args: Here for extendability of the class.

        Returns:
            Union[float, Any]: Utility of the player.
        """
        return self._util(actions, *args)


class MixedPlayer(Player):
    def __init__(self, name, index, actions, all_actions):
        Player.__init__(self, name, index, actions)
        self.all_actions = all_actions  # list of actions for all players

    def mixedU(self, probs, *args):
        def ut(zipped):  # prob of playing a times U_i(a)
            return np.prod(zipped[1]) * self.U(list(zipped[0]))
        mixed_play = product(*(enumerate(p) for p in probs))
        return sum(ut(list(zip(*i))) for i in mixed_play)
