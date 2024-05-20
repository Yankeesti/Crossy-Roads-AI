from __future__ import annotations
from typing import TYPE_CHECKING
import pygame


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
