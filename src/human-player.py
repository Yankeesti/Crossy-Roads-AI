import pygame
import game


class HumanController(game.player.controller.Controller):
    def __init__(self):
        pass

    def get_action(self, inputs):
        pass

    def set_fitness(self, fitness):
        pass

pygame.init()
gameManager = game.game_manager.GameManager([HumanController()], None)
camera = game.camera.CameraBase(gameManager)
camera.y_offset = -1000
while True:
    camera.draw()

