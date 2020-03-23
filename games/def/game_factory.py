class GFactory(ABC):

    @abstractmethod
    def make_game(self, *args):
        self._check_game(*args)
        return Game(*args)

    
    @abstractmethod
    def _check_game(self, *args):
        pass