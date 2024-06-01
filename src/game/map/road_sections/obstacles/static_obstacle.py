from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from game import config
from game.map.road_sections.obstacles.base_obstacle import BaseObstacle
from game.helper import transform_distance, normalize_signed_input

if TYPE_CHECKING:
    from game.map.road_sections.static_road_section import StaticRoadSection
    from game.player.player import Player


class StaticObstacle(BaseObstacle):
    def __init__(self, x_pos: int, road_section: StaticRoadSection):
        image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE))
        image.fill((0, 0, 0))

        super().__init__(image, x_pos, road_section)

    def get_position_relative_to_player(self, player: Player) -> tuple[int, int]:
        center_distance = (self.rect.centerx - player.rect.centerx) / config.BLOCK_SIZE
        if self.rect.centerx < player.rect.centerx:
            center_distance = center_distance + 1
        elif self.rect.centerx > player.rect.centerx:
            center_distance = center_distance - 1

        return normalize_signed_input(
            transform_distance(center_distance, config.MAX_DISTANCE_TO_PLAYER),
            -config.MAX_DISTANCE_TO_PLAYER,
            config.MAX_DISTANCE_TO_PLAYER,
        )
