#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Top level module for creating a Game object instance.
Also abstractly defines Player, Action, and Equilibrium objects.
"""
from typing import List, Any, Union


class Actions:

    """ Wrapper for an action that a Player can take.
    """
    
    def __call__(self, action: Any, *args) -> Any:
        """ Returns action description based on the index of the action.
        
        Args:
            action (Any): Index of action being taken.
            *args: Here for extendability of the class.
        
        Raises:
            NotImplementedError: Not implemented.

        Returns:
            Any: The action taken.
        """
        raise NotImplementedError


class Player:

    """ Game theoretical based description of a player in a game.

    Attributes:
        name (str): Label for the player.
        index (int): Index for the player for easy reference in a list of players in a game.
        actions (Actions): Actions object that the player can take.
    """
    
    def __init__(self, name: str, index: int, actions: Actions):
        """
        Args:
            name (str): Label for the player.
            index (int): Index for the player for easy reference in a list of players in a game.
            actions (Actions): Actions object that the player can take.
        """
        self.name: str = name
        self.index: int = index
        self.actions: Actions = actions

    def U(self, actions: list, *args) -> Union[float, Any]:
        """ Utility function that should follow the von Neumann - Morgenstern axioms. 
        Outlines preferences of own actions based on what actions othe rplayers have taken.
        
        Args:
            actions (list): List of actions that each player in the game has taken.
            *args: Here for extendability of the class.
        
        Raises:
            NotImplementedError: Not implemented.

        Returns:
            Union[float, Any]: Utility of player i.
        """
        raise NotImplementedError

    def __str__(self) -> str:
        """ String description.
        
        Returns:
            str: "Player(index : name)".
        """
        return self.__class__.__name__ + '({}: {})'.format(self.index, self.name)

    def __repr__(self) -> str:
        """ String representation.
        
        Returns:
            str: "Player(index, name, actions)".
        """
        return self.__class__.__name__ + '(index: {}, name: {}, actions: {})'.format(self.index, self.name, repr(self.actions))


class Eq:

    """ Wrapper for an equilibrium solution for the game instance.

    Attributes:
        play (list): Index of action being taken.
    """
    
    def __init__(self, play: list):
        """
        Args:
            play (list): Index of action being taken.
        """
        self.play: list = play

    def __repr__(self) -> str:
        """ String representation.
        
        Returns:
            str: "Eq(play)".
        """
        return self.__class__.__name__ + '({})'.format(repr(self.play))


class Game:

    """ Bare-bones game theoretical defintion of a game instance.

    Attributes:
        players (List[Player]): List of players defining the game interactions.
        actions (List[Actions]): List of Actions object for each player.
        N (int): Number of players in the game.
        eq (List[Eq]): List of equilibrium solutions to the game.
    """
    
    def __init__(self, players: List[Player]):
        """
        Args:
            players (List[Player]): List of players defining the game interactions.
        """
        self.players : List[Player] = players
        self.actions : List[Actions] = [p.actions for p in self.players]
        self.N : int = len(players)
        self.eq : List[Eq] = []

    def all_play(self, play: list) -> list:
        """ Returns a list of actions based on the indexes of play taken by each player.
        
        Args:
            play (list): Index of each action taken by each player
        
        Returns:
            list: A list of actions taken by each player.
        """
        return [ac(play[p.index]) for ac in self.actions]

    def U_i(self, i: int, play: list, *args) -> Union[float, Any]:
        """ Returns utility of player i based on the play.
        
        Args:
            i (int): For returning the utility of player i.
            play (list): Which indexes of actions are played by each player.
            *args: Here for extendability of the class.
        
        Returns:
            Union[float, Any]: Utility of player i.
        """
        return self.players[i].U(self.all_play(play))

    def __str__(self) -> str:
        """ String description.
        
        Returns:
            str: "Game(players)".
        """
        players_str = map(str, self.players)
        return self.__class__.__name__ + '(players: {})'.format(', '.join(players_str))

    def __repr__(self) -> str:
        """ String representation.
        
        Returns:
            str: "Game(players, eq)".
        """
        players_str = map(repr, self.players)
        eq_str = map(repr, self.eq)
        return self.__class__.__name__ + '(players: [{}], eq: [{}])'.format(', '.join(players_str), ', '.join(eq_str))
