from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from game import config
from game.helper import (
    transform_distance,
    normalize_signed_input,
    normalize_positive_input,
)


if TYPE_CHECKING:
    from game.map.road_sections.static_road_section import StaticRoadSection


class BaseObstacle(pygame.sprite.Sprite):
    def __init__(
        self, image: pygame.surface.Surface, x_pos: int, road_section: StaticRoadSection
    ) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.bottomleft = (x_pos, road_section.rect.bottom)
        self.road_section = road_section

    # There are two distances, left and right the left distance describes the distance fom the left site of the player rect to
    # the right site of the obstacle rect, when the obstacle is right from the player the distance calculated by adding the distance of
    # the Player to the left to the distance of the obstacle to the right, as if the section is a circle (left end of section = right end of section)

    def calc_distance_right_obstacle_left_from_player(
        self, rect: pygame.rect.Rect
    ) -> float:
        """calculates the distance from the players right side to obstacles left side when obstacle left from player"""
        return (config.WINDOW_WIDTH - rect.right + self.rect.left) / config.BLOCK_SIZE

    def calc_distance_left_obstacle_right_from_player(
        self, rect: pygame.rect.Rect
    ) -> float:
        """ "calculates the distance from the players right side to obstacles left side when obstacle left from player"""
        return (rect.left + (config.WINDOW_WIDTH - self.rect.right)) / config.BLOCK_SIZE

    def get_relative_position(self, rect: pygame.rect.Rect) -> tuple[float, float]:
        """Returns the relative position of the obstacle to the player.
        The first value represents the distance to the left of the player,
        and the second value represents the distance to the right of the player."""
        distance_left: float
        distance_right: float
        if rect.left >= self.rect.right:
            # obstacle is left from Player
            distance_left = (rect.left - self.rect.right) / config.BLOCK_SIZE
            distance_right = self.calc_distance_right_obstacle_left_from_player(rect)
        elif rect.right <= self.rect.left:
            # obstacle is right from player
            distance_left = self.calc_distance_left_obstacle_right_from_player(rect)
            distance_right = (self.rect.left - rect.right) / config.BLOCK_SIZE
        else:
            # obstacle is overlapping with rect
            distance_left = 0
            distance_right = 0

        # normalize inputs
        distance_left = normalize_positive_input(
            transform_distance(distance_left), 0, config.MAX_DISTANCE_TO_PLAYER
        )

        distance_right = normalize_positive_input(
            transform_distance(distance_right), 0, config.MAX_DISTANCE_TO_PLAYER
        )

        return distance_left, distance_right
