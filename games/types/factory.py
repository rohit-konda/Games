from abc import ABC, abstractmethod

class GFactory(ABC):
    @abstractmethod
    def make_game(cls, *args):
        pass

    @abstractmethod
    def _make_player(cls, *args):
    	pass

    @abstractmethod
    def _check_args(cls, *args):
        pass