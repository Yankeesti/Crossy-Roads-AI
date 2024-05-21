import pygame
import game

navigation_action: game.player_action.PlayerAction = (
    game.player_action.PlayerAction.STAY
)
print_input = False


def handle_key_press():
    global navigation_action, print_input
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                navigation_action = game.player_action.PlayerAction.LEFT
            if event.key == pygame.K_d:
                navigation_action = game.player_action.PlayerAction.RIGHT
            if event.key == pygame.K_w:
                navigation_action = game.player_action.PlayerAction.UP
            if event.key == pygame.K_s:
                navigation_action = game.player_action.PlayerAction.DOWN
            if event.key == pygame.K_p:
                print_input = True
    return True


class HumanController(game.player.controller.Controller):
    def __init__(self):
        pass

    def get_action(self, inputs):
        global navigation_action, print_input
        out_put = navigation_action
        navigation_action = game.player_action.PlayerAction.STAY
        if print_input:
            print(inputs)
            print_input = False
        return out_put

    def set_fitness(self, fitness):
        print("score: ", fitness)


pygame.init()
clock = pygame.time.Clock()
gameManager = game.game_manager.GameManager(
    [HumanController()], game.map.road_section_manager.RoadSectionManager()
)
camera = game.camera.PlayerCamera(gameManager)


while True:
    clock.tick(60)
    if handle_key_press() == False or gameManager.update() == False:
        break
    camera.draw(gameManager.player_manager.sprites()[0])
