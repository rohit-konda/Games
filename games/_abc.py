#!/usr/bin/env python
"""

Author : Rohit Konda
Copyright (c) 2020 Rohit Konda. All rights reserved.
Licensed under the MIT License. See LICENSE file in the project root for full license information.

Summary:
    Defines abstract class definitions for Actions, Players, Payoffs, Equilibria, and Games.
"""

from abc import ABC, abstractmethod
from collections.abc import Set


class Ac:
    """
    Abstract class for action.

    Attributes:
        tag (str): string label for the action.
    """

    def __init__(self, tag):
        self._tag = tag

    @property
    def tag(self):
        """ getter method for self._tag

        Returns:
            (str): self._tag 
        """
        return self._tag

    @tag.setter
    def tag(self, val):
        """ setter method for self._tag

        Args:
            val (str): string label
        """
        self._tag = val

    def __repr__(self):
        """
        represention is action tag

        Returns:
            (str): tag
        """
        return self._tag


class Action:
    """
    Abstract class for a joint action.

    Attributes:
        _players (PSet): the set of players.
    """
    
    def __init__(self, players):
        self._players = players

    @abstractmethod
    def __getitem__(self, p):
        """ gives action played by player p

        Args:
            p (Player): which player.

        Raises:
            ValueError: if player p is not in Pset

        Returns:
            (Ac): action enacted by player p
        """
        if p not in self._players:
            raise LookupError('given player is not in the player set')


class Player:
    """
    Abstract class for a player.

    Attributes:
        name (str): the name of the player.
        _actions (AcSet): the set of the actions available.
    """

    def __init__(self, name, actions):
        self._name = name
        self._actions = actions

    @property
    def actions(self):
        """ getter method for self._actions

        Returns:
            (str): self._tag 
        """
        return self._tag

    @tag.setter
    def actions(self, val):
        """ setter method for self._actions

        Args:
            val (AcSet): string label
        """
        self._actions = val

    def __repr__(self):
        """
        represent of the player based on its name and action set.

        Returns:
            (str): 'player name: string representation of action set'
        """
        return "{} : {}".format(self._name, self._actions)


class PSet(Set):
    """
    Abstract class for a set of players.
    Extends the Set Class in collections.
    """

    def __init__(self):
        pass


class AcSet(Set):
    """
    Abstract class for a set of actions.
    Extends the Set Class in collections.
    """

    def __init__(self):
        pass


class Eq:
    """
    Abstract class for an Equilibrium - Nash or otherwise.
    """
    
    def __init__(self):
        pass


class Pay:
    """
    Abstract class for a payoff.
    Should follow the Von Neumann and
    Morgenstern axioms for utility.

    Attributes:
        _value: value of the payoff
    """

    def __new__(cls, value):
        i = object.__new__(cls)
        i._value = value
        return i


class Game(ABC):
    """
    Abstract class for a game definition.
    Parent class for all other game constructions.

    Attributes:
        players (Players): list defining a string label for each player i.
    """

    def __init__(self, players):
        self.players = players
        self._check_game()

    @abstractmethod
    def _check_game(self):
        """ check if game construction is valid

        Raises:
            ValueError: if game not valid.
        """
        pass

    @abstractmethod
    def U(self, p, a):
        """ utility function for player p,
        when all players play according to joint action a

        Args:
            p (Player): which player to calculate payoff
            a (Action): Joint action

        Raises:
            ValueError: if player p is not in Pset

        Returns:
            (Payoff): payoff 
        """
        if p not in self._players:
            raise LookupError('given player is not in the player set')
