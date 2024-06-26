from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from game import config
from game.map.road_sections.obstacles.base_obstacle import BaseObstacle
from game.helper import normalize_signed_input, transform_distance

if TYPE_CHECKING:
    from game.map.road_sections.dynamic_road_section import DynamicRoadSection
    from game.player.player import Player


class DynamicObstacle(BaseObstacle):
    def __init__(
        self,
        speed: float,
        road_section: DynamicRoadSection,
        starting_x_pos: float,
        car_overhang: int,
    ):
        """
        Initializes a DynamicObstacle object.

        Parameters:
        - speed (float): The speed of the dynamic obstacle.
        - road_section (DynamicRoadSection): The road section the dynamic obstacle belongs to.
        - starting_x_pos (float): The starting x position of the dynamic obstacle.
        - car_overhang (int): Describes how far the car goes over the display until it is moved back to the start

        Returns:
        - None
        """
        image = pygame.Surface((config.BLOCK_SIZE, config.BLOCK_SIZE * 1.8))
        image.fill((100, 0, 0))
        super().__init__(image, starting_x_pos, road_section)

        self.speed = speed
        self.car_overhang = car_overhang

    def calc_distance_right_obstacle_left_from_player(
        self, rect: pygame.rect.Rect
    ) -> float:
        return (
            super().calc_distance_right_obstacle_left_from_player(rect)
            + self.car_overhang
        )

    def calc_distance_left_obstacle_right_from_player(
        self, rect: pygame.rect.Rect
    ) -> float:
        return (
            super().calc_distance_left_obstacle_right_from_player(rect)
            + self.car_overhang
        )


class DynamicObstacleMovingRight(DynamicObstacle):
    def __init__(self, speed, road_section, starting_x_pos=0, car_overhang=0):
        super().__init__(speed, road_section, starting_x_pos, car_overhang)

    def update(self):
        self.rect.move_ip(self.speed * config.BLOCK_SIZE, 0)
        if self.rect[0] > config.WINDOW_WIDTH + self.car_overhang:
            self.rect[0] = 0


class DynamicObstacleMovingLeft(DynamicObstacle):
    def __init__(self, speed, road_section, starting_x_pos=0, car_overhang=0):
        super().__init__(speed, road_section, starting_x_pos, car_overhang)

    def update(self):
        self.rect.move_ip(self.speed * config.BLOCK_SIZE, 0)
        if self.rect.right < -self.car_overhang:
            self.rect.left = config.WINDOW_WIDTH
