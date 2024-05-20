from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from .game_manager import GameManager

if TYPE_CHECKING:
    from .player.player import Player
    from .map.road_sections.base_road_section import BaseRoadSection


from . import config

BORDER_SURFACE = pygame.Surface(
    (config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS, config.WINDOW_HEIGHT)
)
BORDER_SURFACE.fill((0, 0, 0))
BORDER_SURFACE.set_alpha(128)


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

    def draw_borders(self):
        # drawn grey transparent rectangle to highlightws unplayable area
        self.display_surface.blit(BORDER_SURFACE, (0, 0))
        self.display_surface.blit(
            BORDER_SURFACE,
            (config.WINDOW_WIDTH - config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS, 0),
        )


class PlayerCamera(CameraBase):
    def __init__(self, game_manager: GameManager) -> None:
        super().__init__(game_manager)

    def draw(self, player: Player) -> None:
        self.display_surface.fill((0, 0, 0))
        self.calc_y_offset(player)
        self.draw_road_sections(player)
        self.draw_players()
        self.draw_borders()
        pygame.display.flip()

    def draw_road_sections(self, player: Player):
        super().draw_road_sections(player.sections[0].get_sections_to_draw())

    def calc_y_offset(self, player: Player):
        self.y_offset = (
            player.rect[1] - (config.DISPLAYED_ROAD_SECTIONS - 3) * config.BLOCK_SIZE
        )
