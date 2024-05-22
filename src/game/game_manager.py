import pygame

from . import config
from .player.controller import Controller
from .player.player_manager import PlayerManager
from .map.road_section_manager import RoadSectionManager


WIN = pygame.display.set_mode((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))


class GameManager:

    def __init__(
        self,
        controllers: list[Controller],
        road_section_manager: RoadSectionManager,
    ) -> None:
        self.road_section_manager = road_section_manager
        self.player_manager = PlayerManager(
            controllers, road_section_manager.road_sections[0]
        )

    def reset(
        self, controllers: list[Controller], road_section_manager: RoadSectionManager
    ) -> None:
        self.__init__(
            controllers=controllers, road_section_manager=road_section_manager
        )

    def update(self) -> bool:
        self.road_section_manager.update()
        return self.player_manager.update()
