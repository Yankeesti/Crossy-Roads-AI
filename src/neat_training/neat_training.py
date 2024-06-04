import pygame
import neat
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import game

from neural_network_controller import NeuralNetworkController
import neat_road_section_manager

gameManager: game.game_manager.GameManager = None
played_games_per_generation: int = 20
neat_road_section_manager.generate_starting_road_sections(played_games_per_generation, 10)
road_section_manager: neat_road_section_manager.NeatRoadSectionManager = (
    neat_road_section_manager.NeatRoadSectionManager()
)
clock: pygame.time.Clock = pygame.time.Clock()
best_genome_id: int = 1


def eval_genomes(genomes, config):
    global gameManager, road_section_manager
    controllers = [
        NeuralNetworkController(genome, config) for genome_id, genome in genomes
    ]
    print("Game: ",end="")
    for i in range(
        played_games_per_generation
    ):  # outer loop to run one Genereation through multiple games and calculate a avarage fitness
        print(i,end=", ")
        repeat = True
        while (
            repeat
        ):  # inner loop to replay the game if new Road Sections were generated
            repeat = False
            if gameManager is None:
                gameManager = game.game_manager.GameManager(
                    controllers, road_section_manager
                )
            else:
                road_section_manager.set_index(i)
                gameManager.reset(
                    controllers=controllers, road_section_manager=road_section_manager
                )
            # Run game Loop
            while True:
                if gameManager.update() == False:
                    break
                if (
                    road_section_manager.generated_sections == True
                ):  # when section were generated the this game needs to be replayed, so all genomes after this generation have the same game
                    print("repeat "+str(i),end=", ")
                    repeat = True
                    for controller in controllers:
                        if len(controller.fitnesses) > i:
                            controller.fitnesses.pop()
                    break
    for controller in controllers:
        controller.calc_fitness()

    controllers.sort(key=lambda controller: controller.genome.fitness, reverse=True)
    print()
    print(controllers[0])
    print(controllers[1])
    print(controllers[2])
    print(controllers[3])
    print(controllers[4])


def eval_genomes_draw_game(genomes, config):
    global gameManager, road_section_manager, best_genome_id
    controllers = []
    best_controller: NeuralNetworkController = None
    for genome_id, genome in genomes:
        if genome_id == best_genome_id:
            controllers.append(
                NeuralNetworkController(genome, config, 255, (0, 0, 255))
            )
            best_controller = controllers[-1]
        else:
            controllers.append(NeuralNetworkController(genome, config))
    camera: game.camera.PlayerCamera
    for i in range(
        played_games_per_generation
    ):  # outer loop to run one Genereation through multiple games and calculate a avarage fitness
        repeat = True
        while (
            repeat
        ):  # inner loop to replay the game if new Road Sections were generated
            repeat = False
            if gameManager is None:
                gameManager = game.game_manager.GameManager(
                    controllers, road_section_manager
                )
            else:
                road_section_manager.set_index(i)
                gameManager.reset(
                    controllers=controllers, road_section_manager=road_section_manager
                )
            camera = game.camera.PlayerCamera(gameManager)
            # Run game Loop
            while True:
                clock.tick(60)
                if gameManager.update() == False:
                    break
                if (
                    road_section_manager.generated_sections == True
                ):  # when section were generated the this game needs to be replayed, so all genomes after this generation have the same game
                    repeat = True
                    for controller in controllers:
                        if len(controller.fitnesses) > i:
                            controller.fitnesses.pop()
                camera.draw(best_controller.player)

    for controller in controllers:
        controller.calc_fitness()

    controllers.sort(key=lambda controller: controller.genome.fitness, reverse=True)
    best_genome = controllers[0].genome


def run_neat(config, check_point: str = None) -> None:
    if check_point is not None:
        p = neat.Checkpointer.restore_checkpoint(check_point)
    else:
        # generate new road_sections
        print("generating Sections")

        p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    pygame.init()
    p.run(eval_genomes, 10000)


if __name__ == "__main__":
    pygame.init()
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")

    config = neat.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )
    run_neat(config)
