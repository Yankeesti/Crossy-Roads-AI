import pygame
import neat
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import game

from neural_network_controller import NeuralNetworkController
import neat_road_section_manager

gameManager: game.game_manager.GameManager = None
road_section_manager: neat_road_section_manager.NeatRoadSectionManager = (
    neat_road_section_manager.NeatRoadSectionManager()
)

played_games_per_generation: int = 20


def eval_genomes(genomes, config):
    global gameManager, road_section_manager
    controllers = [
        NeuralNetworkController(genome, config) for genome_id, genome in genomes
    ]
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
            # Run game Loop
            while True:
                if gameManager.update() == False:
                    break
                if (
                    road_section_manager.generated_sections == True
                ):  # when section were generated the this game needs to be replayed, so all genomes after this generation have the same game
                    repeat = True
                    break
    for controller in controllers:
        controller.calc_fitness()


def run_neat(config, check_point: str = None) -> None:
    if check_point is not None:
        p = neat.Checkpointer.restore_checkpoint(check_point)
    else:
        # generate new road_sections
        neat_road_section_manager.generate_starting_road_sections(
            played_games_per_generation, 10
        )
        p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    pygame.init()
    p.run(eval_genomes, 1000)


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
