#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Abstract definition for a factory class to create a game.
"""
from games.types.game import Game, Player

class GFactory:

    """ Factory class for creating a game.
    """
    
    @classmethod
    def make_game(cls, *args) -> Game:
        """ Main method for game creation.
        
        Args:
            *args: Arguments needed for creating a game.
        
        Raises:
            NotImplementedError: Needs to be implemented.
        """
        raise NotImplementedError

    @classmethod
    def _make_player(cls, *args) -> Player:
    	""" Method for creating players in a game.
    	
    	Args:
    	    *args: Arguments needed to create a player.
    	
    	Raises:
    	    NotImplementedError: Needs to be implemented.
    	"""
    	raise NotImplementedError

    @classmethod
    def _check_args(cls, *args) -> None:
        """ Error check here to make sure the specified game is created properly.
        
        Args:
            *args: Arguments for game creation
        
        Raises:
            NotImplementedError: Description
        """
        raise NotImplementedError