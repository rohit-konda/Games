#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

import numpy as np
from typing import List, Callable
from games.types.game import Game
from games.types.strategic import StrategicFactory, StrategicGame
from games.types.congestion import CongestionFactory, CongestionGame
from games.types.resource import ResourceFactory, ResourceGame
from games.analysis.search_nash	import BruteNash


def normal_form_game(payoffs: List[np.ndarray]) -> StrategicGame:
	return StrategicFactory.make_game(payoffs)

def congestion_game(actions: List[List[List[int]]], r_m: int, list_f_r: List[Callable[[int, List[int]], float]]) -> CongestionGame:
	return CongestionFactory.make_game(actions, r_m, w_r, list_f_r)

def welfare_resource_game(actions: List[List[List[int]]], values: List[float], w: List[float], f: List[float]) -> ResourceGame:
	return ResourceFactory.make_game(actions, values, w, f)

def get_payoff(game: Game) -> List[np.ndarray]:
	return BruteNash.game_to_payoffs(game)

def to_normal_form(game: Game) -> StrategicGame:
	return normal_form_game(get_payoff(game))