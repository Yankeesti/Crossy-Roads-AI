from __future__ import annotations
from typing import TYPE_CHECKING, Callable
import pygame

from .. import config
from game.player.player_action import PlayerAction

if TYPE_CHECKING:
    from ..map.road_sections.base_road_section import BaseRoadSection
    from game.player.controller import Controller
    import game.player.player_manager as player_manager


class Player(pygame.sprite.Sprite):
    def __init__(
        self,
        current_section: BaseRoadSection,
        controller: Controller,
        manager: player_manager.PlayerManager,
    ) -> None:
        super().__init__()
        self.image: pygame.surface.Surface = pygame.Surface(
            (config.BLOCK_SIZE, config.BLOCK_SIZE)
        )
        self.image.fill(controller.get_player_color())

        self.rect: pygame.rect.Rect = self.image.get_rect()
        self.rect.midbottom = (config.WINDOW_WIDTH / 2, 0)

        # list of road sections that the player is currently on
        self.sections: list[BaseRoadSection] = [
            current_section
        ]  # on index 1 is alway the section from which player should be removed after move is finished
        current_section.add_player(self)

        self.manager: player_manager.PlayerManager = manager
        self.controller: Controller = controller
        self.highest_section: BaseRoadSection = current_section
        # the y point where the player will be killed
        self.killing_y_point: float = config.MAX_BLOCKS_BACK * config.BLOCK_SIZE
        # Stores the amount of frames where no input was fetched, when its higher then INPUT_FETCH_INTERVAL input is fetched  from controller and value is set back to 0
        self.last_input_fetch: int = config.INPUT_FETCH_INTERVAL
        self.moves: list[Callable, int] = [PlayerAction.STAY, -1]
        self.last_input_fetch = config.INPUT_FETCH_INTERVAL

    def update(self):
        self.killing_y_point -= config.BLOCK_SIZE * config.KILLING_POINT_SPEED
        if self.moves[1] > 0:  # When move is not ended yet first finish it
            if self.moves[0] == PlayerAction.STAY:
                self.moves[1] -= 1
            else:
                self.moves[0]()
                self.moves[1] -= 1
                if self.moves[1] == 0:
                    self.sections.pop(1).remove_player(self)
                    self.moves = [PlayerAction.STAY, config.PLAYER_PAUSE_AFTER_MOVE]
        elif self.last_input_fetch >= config.INPUT_FETCH_INTERVAL:
            controller_input: PlayerAction = self.controller.get_action(None)
            if controller_input == PlayerAction.UP:
                self.init_up()
            elif controller_input == PlayerAction.DOWN:
                self.init_down()
            elif controller_input == PlayerAction.LEFT:
                self.init_left()
            elif controller_input == PlayerAction.RIGHT:
                self.init_right()
            self.last_input_fetch = -1
        self.last_input_fetch += 1

    def init_up(self):
        if (
            self.sections[0]
            .get_next_section()
            .move_possible(self, (0, -config.BLOCK_SIZE))
        ):
            self.sections.insert(0, self.sections[0].next_section)
            self.moves = [self.up, config.PLAYER_SPEED]

    def up(self):
        self.rect[1] -= config.BLOCK_SIZE // config.PLAYER_SPEED

    def init_down(self):
        if self.rect.bottom < 0 and self.sections[0].previous_section.move_possible(
            self, (0, config.BLOCK_SIZE)
        ):
            self.sections.insert(0, self.sections[0].previous_section)
            self.moves = [self.down, config.PLAYER_SPEED]

    def down(self):
        self.rect[1] += config.BLOCK_SIZE // config.PLAYER_SPEED

    def init_left(self):
        if self.rect.left - config.BLOCK_SIZE * (
            config.UNSTEPABLEE_COLUMNS + 1
        ) >= 0 and self.sections[0].move_possible(self, (-config.BLOCK_SIZE, 0)):
            self.sections.insert(0, self.sections[0])
            self.moves = [self.left, config.PLAYER_SPEED]

    def left(self):
        self.rect[0] -= config.BLOCK_SIZE // config.PLAYER_SPEED

    def init_right(self):
        if (
            self.rect.right + config.BLOCK_SIZE
            <= config.WINDOW_WIDTH - config.BLOCK_SIZE * config.UNSTEPABLEE_COLUMNS
            and self.sections[0].move_possible(self, (config.BLOCK_SIZE, 0))
        ):
            self.sections.insert(0, self.sections[0])
            self.moves = [self.right, config.PLAYER_SPEED]

    def right(self):
        self.rect[0] += config.BLOCK_SIZE // config.PLAYER_SPEED
