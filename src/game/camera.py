from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from .game_manager import GameManager

if TYPE_CHECKING:
    from .map.road_sections.base_road_section import BaseRoadSection


from . import config


class CameraBase:
    def __init__(self, game_manager: GameManager) -> None:
        self.game_manager: GameManager = game_manager
        self.display_surface: pygame.surface.Surface = pygame.display.get_surface()
        self.y_offset: float = -config.WINDOW_HEIGHT

    def draw(self) -> None:
        self.display_surface.fill((0, 0, 0))

        self.draw_road_sections()
        self.draw_players()
        pygame.display.flip()

    def draw_road_sections(self, road_sections: list[BaseRoadSection]):
        for section in road_sections:
            section.draw(self.display_surface, self.y_offset)

    def draw_players(self):
        for player in self.game_manager.player_manager.sprites():
            self.display_surface.blit(
                player.image, (player.rect[0], player.rect[1] - self.y_offset)
            )
