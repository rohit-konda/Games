#!/usr/bin/env python
# Author : Rohit Konda
# Copyright (c) 2020 Rohit Konda. All rights reserved.
# Licensed under the MIT License. See LICENSE file in the project root for full license information.

from games.types.game import Game, Actions, Player
from typing import List, Callable, Union, Any


class WelfareGame(Game):
    def __init__(self, players: List[Player]):
        Game.__init__(self, players)

    def welfare(self, play: list, *args) -> Union[float, Any]:
        raise NotImplementedError


class PotentialGame(Game):
    def __init__(self, players: List[Player]):
        Game.__init__(self, players)

    def potential(self, play: list, *args) -> float:
        raise NotImplementedError


class FActions(Actions):
    def __init__(self, actions: list):
        self.actions: list = actions

    def __call__(self, play: Union[int, float]) -> Any:
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
    def __init__(self, name: str, index: int, actions: Actions, util: Callable[..., Union[float, Any]]):
        Player.__init__(self, name, index, actions)
        self._util: Callable[..., Union[float, Any]] = util 

    def U(self, actions: list, *args) -> Union[float, Any]:
        return self._util(actions, *args)



# class DocParser:
#     KEYWORDS = ['Summary', 'Args', 'Example', 'Attributes', 'Returns', 'Raises', 'Todo']
#     @staticmethod
#     def splitdoc(doc):
#         lines = [l for l in doc.split('\n') if l.strip()]
#         return lines

#     @staticmethod
#     def get_args(lines):
#         ind = 

#     @staticmethod
#     def get_attr(lines)