from typing import List, Any, Union


class Actions:
    def __call__(self, action: Any, *args) -> Any:
        raise NotImplementedError


class Player:
    def __init__(self, name: str, index: int, actions: Actions):
        self.name: str = name
        self.index: int = index
        self.actions: Actions = actions

    def U(self, play: list, *args) -> Union[float, Any]:
        raise NotImplementedError

    def __str__(self):
        return self.__class__.__name__ + '({}: {})'.format(self.index, self.name)

    def __repr__(self):
        return self.__class__.__name__ + '(index: {}, name: {}, actions: {})'.format(self.index, self.name, repr(self.actions))


class Eq:
    def __init__(self, play: list):
        self.play: list = play

    def __repr__(self):
        return self.__class__.__name__ + '({})'.format(repr(self.play))



class Game:
    def __init__(self, players: List[Player]):
        self.players : List[Player] = players
        self.actions : List[Actions] = [p.actions for p in self.players]
        self.N : int = len(players)
        self.eq : List[Eq] = []

    def all_play(self, play: list) -> list:
        return [p.actions(play[p.index]) for p in self.players]

    def U_i(self, i: int, play: list, *args) -> Union[float, Any]:
        return self.players[i].U(self.all_play(play))

    def __str__(self):
        players_str = map(str, self.players)
        return self.__class__.__name__ + '(players: {})'.format(', '.join(players_str))

    def __repr__(self):
        players_str = map(repr, self.players)
        eq_str = map(repr, self.eq)
        return self.__class__.__name__ + '(players: [{}], eq: [{}])'.format(', '.join(players_str), ', '.join(eq_str))




