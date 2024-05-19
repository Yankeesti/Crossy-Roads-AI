from __future__ import annotations
from typing import TYPE_CHECKING
import pygame

from game.player.player import Player
if TYPE_CHECKING:
    import game.player.controller as controller
    from ..map.road_sections.road_section_base import RoadSectionBase

class PlayerManager:

    def __init__(self,controllers: list[controller.Controller],first_section : RoadSectionBase) -> None:
        self.players : pygame.sprite.Group = pygame.sprite.Group()
        for controller in controllers:
            self.players.add(Player(first_section,controller,self))