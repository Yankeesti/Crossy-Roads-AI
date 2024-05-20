from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from game import config
from game.map.road_sections.obstacles.base_obstacle import BaseObstacle

if TYPE_CHECKING:
    from game.map.road_sections.static_road_section import StaticRoadSection

class StaticObstacle(BaseObstacle):
    def __init__(self, x_pos: int, road_section: StaticRoadSection):
        image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE))
        image.fill((0, 0, 0))

        super().__init__(image, x_pos, road_section)

