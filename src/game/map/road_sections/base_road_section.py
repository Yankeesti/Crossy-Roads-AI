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
    ) -> None:
        super().__init__()
        self.image = surface
        self.rect = self.image.get_rect()
        self.index = index
        self.rect.bottomleft = (0, -(index * config.BLOCK_SIZE))
        self.next_section = None
        self.previous_section = previous_section
        self.players_on_section = pygame.sprite.Group()
        self.sections_to_draw = None
        self.road_section_manager = road_section_manager
        self.inputs: dict[float, list[float]] = (
            {}
        )  # stores the inputs, the key value is the position of the player

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

    def get_next_section(self) -> BaseRoadSection:
        if self.next_section is None:
            self.road_section_manager.generate_sections(1)
        return self.next_section

    def add_player(self, player: Player):
        self.players_on_section.add(player)

    def remove_player(self, player: Player):
        self.players_on_section.remove(player)

    def move_possible(self, player: Player, move: tuple[int, int]):
        return True

    @abc.abstractmethod
    def draw(self, surface: pygame.surface.Surface, y_offset: int):
        surface.blit(self.image, (0, self.rect[1] - y_offset))

    @abc.abstractmethod
    def to_dict(self):
        pass

    @abc.abstractmethod
    def calculate_input_values(self, rect: pygame.rect.Rect) -> list[float]:
        pass

    def get_obstacle_positions_relative_to_player(self, player: Player) -> list[float]:
        player_rect = player.rect
        player_position = player_rect.left
        if player_position in self.inputs:
            return self.inputs[player_position]
        else:
            input_values = self.calculate_input_values(player_rect)
            self.inputs[player_position] = input_values
            return input_values
