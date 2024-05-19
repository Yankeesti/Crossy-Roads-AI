import abc
import typing

import action

class Controller(abc.ABC):

    @abc.abstractmethod
    def get_action(self, inputs : typing.Tuple[float,...]) -> action.Action:
        pass

    @abc.abstractmethod
    def set_fitness(self, fitness : float) -> None:
        pass