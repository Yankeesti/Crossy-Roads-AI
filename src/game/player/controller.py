import abc
import typing

from .player_action import PlayerAction


class Controller(abc.ABC):

    @abc.abstractmethod
    def get_action(self, inputs: typing.Tuple[float, ...]) -> PlayerAction:
        pass

    @abc.abstractmethod
    def set_fitness(self, fitness: float) -> None:
        pass

    def get_player_color(self) -> typing.Tuple[int, int, int]:
        """
        Returns the color of the player when drawing the game.

        By overriding this method, games can highlight specific players.

        Returns:
            A tuple representing the RGB color values of the player.
        """
        return (255, 0, 0)
