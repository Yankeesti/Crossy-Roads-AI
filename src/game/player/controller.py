import abc
import typing

from .player_action import PlayerAction


class Controller(abc.ABC):

    def __init__(
        self, alpha_value: int = 128, color: typing.Tuple[int, int, int] = (255, 0, 0)
    ) -> None:
        self.alpha_value = alpha_value
        self.color = color

    @abc.abstractmethod
    def get_action(self, inputs: typing.Tuple[float, ...]) -> PlayerAction:
        pass

    @abc.abstractmethod
    def set_fitness(self, fitness: float) -> None:
        pass