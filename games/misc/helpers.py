#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

"""
Accumulation of general helper functions
"""
from itertools import chain, combinations
from typing import Iterable, List
from games.types.game import Game

def powerset(iterable: Iterable) -> List[tuple]:
    """ Returns a power set from the given iterable.
    
    Args:
        iterable (Iterable): Iterable from which to take the power set from.
    
    Returns:
        List[tuple]: A list of tuples containing subsets of the given Iterable.
    """
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def verify_player_list(game: Game) -> None:
    """Check that player list is nonempty and indexed from 0 to N.
    
    Args:
        game (Game): Game to check.
    
    Raises:
        ValueError: If the player list is empty or not indexed properly.
    """
    if len(game.players) == 0:
        raise ValueError('Player list is empty.')
    game.players = sorted(game.players, key=lambda x : x.index)
    if [p.index for p in game.players] != [i for i in range(game.N)]:
        raise ValueError('Player\'s indices must be from 0 to the number of players')
