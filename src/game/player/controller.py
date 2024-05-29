from __future__ import annotations
from typing import TYPE_CHECKING
import abc
import typing

from .player_action import PlayerAction
if TYPE_CHECKING:
    from .player import Player


class Controller(abc.ABC):

    def __init__(
        self, alpha_value: int = 128, color: typing.Tuple[int, int, int] = (255, 0, 0)
    ) -> None:
        self.alpha_value = alpha_value
        self.color = color
        self.player:Player = None

    @abc.abstractmethod
    def get_action(self, inputs: typing.Tuple[float, ...]) -> PlayerAction:
        pass

    @abc.abstractmethod
    def set_fitness(self, fitness: float) -> None:
        pass

    def set_player(self, player:Player) -> None:
        self.player = player