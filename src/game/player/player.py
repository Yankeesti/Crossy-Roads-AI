from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from .. import config
if TYPE_CHECKING:
    from ..map.road_sections.road_section_base import RoadSectionBase
    from game.player.controller import Controller
    import game.player.player_manager as player_manager

class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        current_section: RoadSectionBase,
        controller: Controller,
        manager: player_manager.PlayerManager,
    ) -> None:
        super().__init__()
        self.image: pygame.surface.Surface = pygame.Surface(
            (config.BLOCK_SIZE, config.BLOCK_SIZE)
        )
        self.image.fill(controller.get_player_color())

        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.midbottom = (config.WINDOW_WIDTH / 2, 0)

        # list of road sections that the player is currently on
        self.sections: list[RoadSectionBase] = [current_section]
        # current_section.add_player(self)

        self.manager: player_manager.PlayerManager = manager
        self.controller: Controller = controller
        self.highest_section: RoadSectionBase = current_section
        # the y point where the player will be killed
        self.killing_y_point: float = config.MAX_BLOCKS_BACK * config.BLOCK_SIZE
        # Stores the amount of frames where no input was fetched, when its higher then INPUT_FETCH_INTERVAL input is fetched  from controller and value is set back to 0
        self.last_input_fetch: int = config.INPUT_FETCH_INTERVAL

def update(self):
    self.killing_y_point -= config.BLOCK_SIZE * config.KILLING_POINT_SPEED
    
