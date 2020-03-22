#!/usr/bin/env python
"""

Author : Rohit Konda
Copyright (c) 2020 Rohit Konda. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for full license information.

Summary:
    Defines abstract class definitions for Actions, Players, Payoffs, Equilibria, and Games.
"""

from abc import ABC, abstractmethod


class _Indexed:
    """
    Class for objects that are indexed in a set or a list

    Attributes:
        index (tuple): index of object
    """
    def __init__(self, index):
        self._index = index

    @property
    def index(self):
        """
        getter method for self._index

        Returns:
            (str): self._index
        """
        return self._index

    @index.setter
    def index(self, val):
        """
        setter method for self._index

        Args:
            val (str): string label
        """
        self._index = val


class _Tagged:
    """
    Class for objects that are tagged with an ID

    Attributes:
        tag (str): ID of the object
    """
    def __init__(self, tag):
        self._tag = tag


    @property
    def tag(self):
        """
        getter method for self._tag

        Returns:
            (str): self._tag 
        """
        return self._tag

    @tag.setter
    def tag(self, val):
        """
        setter method for self._tag

        Args:
            val (str): string label
        """
        self._tag = val


class Action(_Tagged, _Indexed):
    """
    Abstract class for action.

    Attributes:
        name (str): the name of the player.
    """
    def __init__(self, tag, index):
        _Tagged.__init__(self, tag)
        _Indexed.__init__(self, index)

    def __repr__(self):
        """
        represention is action tag

        Returns:
            (str): tag
        """
        return self._tag


class Player(_Tagged, _Indexed):
    """
    Abstract class for a player.

    Attributes:
        name (str): the name of the player.
        _actions (set(Act)): the set of the actions available.
    """

    def __init__(self, tag, index, actions):
        _Tagged.__init__(self, tag)
        _Indexed.__init__(self, index)
        self._actions = actions

    def U(self, a):
        pass

    @property
    def actions(self):
        """
        getter method for self._actions

        Returns:
            (str): self._actions
        """
        return self._actions

    @actions.setter
    def actions(self, val):
        """
        setter method for self._actions

        Args:
            val (set(Action)): set of Action objects
        """
        self._actions = actions

    def __repr__(self):
        """
        represent of the player based on its name and action set.

        Returns:
            (str): 'player name: string representation of action set'
        """
        return "{} : {}".format(self._name, self._actions)


class Eq:
    """
    Abstract class for an Equilibrium.
    """
    pass


class NashEq(Eq):
    pass


class GameFactory(ABC):
    """
    Abstract class for game construction, used for correct construction
    of game objects
    """

    @abstractmethod
    def make_game(self, *args):
        """
        constructor for a game

        Args:
            *args (list): generic list of arguments to generate a game

        Raises:
            ValueError: if there is an error in construction

        Returns:
            (Game): A valid game construction
        """
        self._check_game(*args)
        return Game(*args)

    @abstractmethod
    def _check_game(self, *args):
        """
        check if game construction is valid

        Args:
            *args (list): generic list of arguments to generate a game

        Raises:
            ValueError: if game not valid.
        """
        pass


class Game(ABC):
    """
    Abstract class for a game definition.
    Parent class for all other game constructions.

    Attributes:
        players (set(Player)): An abstract set of Player Objects
    """

    def __init__(self, players):
        self.players = players
        self.state = state