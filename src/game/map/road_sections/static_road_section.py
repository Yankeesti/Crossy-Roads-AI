from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import random

from game import config
from .base_road_section import BaseRoadSection
from .obstacles.static_obstacle import StaticObstacle

if TYPE_CHECKING:
    from game.map.road_section_manager import RoadSectionManager
    from game.player.player import Player


class StaticRoadSection(BaseRoadSection):
    def __init__(
        self,
        index: int,
        road_section_manager: RoadSectionManager,
        previous_section: BaseRoadSection = None,
        next_section: BaseRoadSection = None,
        static_obstacle_positions: list[int] = None,
    ) -> None:
        image = pygame.surface.Surface((config.WINDOW_WIDTH, config.BLOCK_SIZE))
        if index % 2 == 0:
            image.fill((0, 161, 43, 255))
        else:
            image.fill((37, 255, 0, 255))
        super().__init__(index, image, road_section_manager, previous_section)
        self.static_obstacles = pygame.sprite.Group()
        self.static_obstacle_positions = static_obstacle_positions
        self.init_static_obstacles(static_obstacle_positions)

    def init_static_obstacles(self, static_obstacle_positions: list[int]) -> None:
        if static_obstacle_positions is None:
            self.static_obstacle_positions = random.sample(
                range(0, config.ROAD_COLUMNS + 2 * config.UNSTEPABLEE_COLUMNS),
                random.randint(0, 3),
            )
        for position in self.static_obstacle_positions:
            self.static_obstacles.add(
                StaticObstacle(position * config.BLOCK_SIZE, self)
            )

    def draw(self, surface: pygame.Surface, y_offset: int):
        super().draw(surface, y_offset)
        for static_obstacle in self.static_obstacles:
            surface.blit(
                static_obstacle.image,
                (static_obstacle.rect[0], static_obstacle.rect[1] - y_offset),
            )

    def move_possible(self, player: Player, move: tuple[int, int]):
        player.rect.move_ip(move)
        out_put = pygame.sprite.spritecollide(player, self.static_obstacles, False)
        player.rect.move_ip((-move[0], -move[1]))
        return out_put == []

    def to_dict(self):
        return {
            "type": "StaticRoadSection",
            "index": self.index,
            "static_obstacle_positions": self.static_obstacle_positions,
        }
    
    def get_obstacle_positions_relative_to_player(self, player) -> list[float]:
        obstacle_pos = [
            ((obstacle.rect.centerx - player.rect.centerx) / config.BLOCK_SIZE, 0)
            for obstacle in self.static_obstacles
        ]
        obstacle_pos.sort(key=lambda pos: abs(pos[0]))
        default_values = [(15, 0)] * (3 - len(obstacle_pos))
        obstacle_pos.extend(default_values)
        return obstacle_pos
