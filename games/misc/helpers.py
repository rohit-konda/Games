
from itertools import chain, combinations

def powerset(iterable):
    """ returns the powerset of an iterable object (as a list of tuples)"""
    s = list(iterable)
    return chain.from_iterable(combinations(s, r) for r in range(len(s)+1))

def verify_game(self, game):
    try:
        iter(game.players)
        if len(game.players) == 0:
            raise ValueError('Player list is empty.')
    except TypeError:
        raise TypeError('self.players must be iterable.')
    if not all([isinstance(p, Player) for p in game.players]):
        raise TypeError('Players must contain players of type games.types.players.Player.')
    game.players = sorted(game.players, key=lambda x : x.index)
    if [p.index for p in game.players] != [i for i in range(game.N)]:
        raise ValueError('Player\'s indices must be from 0 to the number of players')