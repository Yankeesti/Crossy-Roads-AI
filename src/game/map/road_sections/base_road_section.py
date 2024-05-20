from __future__ import annotations
from typing import TYPE_CHECKING
import pygame
import abc

from game import config

if TYPE_CHECKING:
    from game.map.road_section_manager import RoadSectionManager
    from game.player.player import Player


class BaseRoadSection(pygame.sprite.Sprite):

    def __init__(
        self,
        index: int,
        surface: pygame.surface.Surface,
        road_section_manager: RoadSectionManager,
        previous_section: BaseRoadSection,
        next_section: BaseRoadSection,
    ) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.index = index
        self.rect.bottomleft = (0, -(index * config.BLOCK_SIZE))
        self.next_section = next_section
        self.previous_section = previous_section
        self.players_on_section = pygame.sprite.Group()
        self.sections_to_draw = None
        self.road_section_manager = road_section_manager

    def get_sections_to_draw(self):
        if self.sections_to_draw is not None:
            return self.sections_to_draw
        self.sections_to_draw = [
            self.previous_section.previous_section.previous_section,
            self.previous_section.previous_section,
            self.previous_section,
            self,
        ]
        next_section = self.get_next_section()
        for i in range(0, config.DISPLAYED_ROAD_SECTIONS - 2):
            self.sections_to_draw.append(next_section)
            next_section = next_section.get_next_section()
        return self.sections_to_draw

    def get_next_section(self):
        if self.next_section is None:
            self.road_section_manager.generate_sections(1)
        return self.next_section

    def add_player(self, player: Player):
        self.players_on_section.add(player)

    def remove_player(self, player: Player):
        self.players_on_section.remove(player)

    @abc.abstractmethod
    def draw(self, surface: pygame.surface.Surface, y_offset: int):
        surface.blit(self.image, (0, self.rect[1] - y_offset))

    def move_possible(self, player: Player, move: tuple[int, int]):
        return True
