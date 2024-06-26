from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import random

from .base_road_section import BaseRoadSection
from game.map.road_sections.moving_direction import MovingDirection
from game.helper import normalize_signed_input
from game import config
from game.map.road_sections.obstacles.dynamic_obstacles import (
    DynamicObstacleMovingLeft,
    DynamicObstacleMovingRight,
)

if TYPE_CHECKING:
    from game.map.road_section_manager import RoadSectionManager


def get_random_car_positions(
    border_overhang: float, direction: MovingDirection, car_number: int = None
) -> list[float]:
    if car_number is None:
        car_number = random.randint(1, config.MAX_OBSTACLES)
    max_distance_per_car = config.COLUMNS_TOTAL / car_number - 1.8
    car_positions = [0]
    for i in range(1, car_number):
        car_positions.append(
            car_positions[-1] + round(random.uniform(0, max_distance_per_car) + 1.8, 2)
        )

    # Random move car to left/right according to the direction
    offset = 0
    if direction == MovingDirection.LEFT:
        offset = round(
            random.uniform(-border_overhang, config.COLUMNS_TOTAL - car_positions[-1]),
            2,
        )
    else:
        offset = round(
            random.uniform(
                0, config.COLUMNS_TOTAL - car_positions[-1] + border_overhang
            ),
            2,
        )
    return [position + offset for position in car_positions]


class DynamicRoadSection(BaseRoadSection):
    def __init__(
        self,
        index: int,
        road_section_manager: RoadSectionManager,
        previous_section: BaseRoadSection,
        car_speed: float,
        car_direction: MovingDirection,
        car_starting_positions: list[float],
        border_overhang: float,
    ):
        """
        Initializes a DynamicRoadSection object.

        Args:
            index (int): The index of the road section.
            road_section_manager (RoadSectionManager): The manager for road sections.
            previous_section (BaseRoadSection): The previous road section.
            car_speed (int): The speed of the cars on the road section.
            car_direction (MovingDirection): The direction in which the cars are moving.
            car_starting_positions (list[float]): The positions of the cars on the road section in Blocks.
            border_overhang (float): Describes how far the cars go over the display until moved back to the start (in Blocks)
        Returns:
            None
        """
        image = pygame.surface.Surface((config.WINDOW_WIDTH, config.BLOCK_SIZE))
        if index % 2 == 0:
            image.fill((80, 80, 80, 255))
        else:
            image.fill((144, 144, 144, 255))
        super().__init__(index, image, road_section_manager, previous_section)

        self.car_speed = car_speed
        self.cars = pygame.sprite.Group()
        self.car_starting_positions = car_starting_positions
        self.border_overhang = border_overhang
        if car_direction == MovingDirection.RIGHT:
            self.init_cars_move_right()
        else:
            self.init_cars_move_left()
        self.car_direction: MovingDirection = car_direction
        if car_direction == MovingDirection.LEFT:
            self.car_speed = -self.car_speed
        self.car_speed_normalized = normalize_signed_input(
            self.car_speed, -config.MAX_CAR_SPEED, config.MAX_CAR_SPEED
        )

    def init_cars_move_right(self):
        for pos in self.car_starting_positions:
            self.cars.add(
                DynamicObstacleMovingRight(
                    self.car_speed, self, pos * config.BLOCK_SIZE, self.border_overhang
                )
            )

    def init_cars_move_left(self):
        for pos in self.car_starting_positions:
            self.cars.add(
                DynamicObstacleMovingLeft(
                    -self.car_speed, self, pos * config.BLOCK_SIZE, self.border_overhang
                )
            )

    def update(self):
        self.inputs.clear()
        self.cars.update()
        dead_players = pygame.sprite.groupcollide(
            self.players_on_section, self.cars, False, False
        )
        for player in dead_players:
            player.kill()

    def draw(self, surface: pygame.surface.Surface, y_offset: int):
        super().draw(surface, y_offset)
        for car in self.cars:
            surface.blit(car.image, (car.rect[0], car.rect[1] - y_offset))

    def to_dict(self):
        return {
            "type": "DynamicRoadSection",
            "index": self.index,
            "car_speed": self.car_speed,
            "car_direction": self.car_direction.value,
            "car_starting_positions": self.car_starting_positions,
            "border_overhang": self.border_overhang,
        }

    def calculate_input_values(self, rect: pygame.Rect) -> list[float]:
        input_values = [car.get_relative_position(rect) for car in self.cars]
        input_values.sort(key=lambda pos: pos[0], reverse=True)
        output = []
        for input_value in input_values:
            output.extend(input_value)
        output.extend((0, 0) * (3 - len(input_values)))  # Add default values
        output.insert(0, self.car_speed_normalized)
        return output
