import pygame

from .game_manager import GameManager



class CameraBase:
    def __init__(self, game_manager: GameManager) -> None:
        self.game_manager: GameManager = game_manager
        self.display_surface: pygame.surface.Surface = pygame.display.get_surface()
        self.y_offset: float = 0
 
        

    def draw(self) -> None:
        self.display_surface.fill((0, 0, 0))
        for player in self.game_manager.player_manager.players:
            self.display_surface.blit(
                player.image, (player.rect[0], player.rect[1] - self.y_offset)
            )
        pygame.display.flip()
