from typing import Dict, Tuple
import neat
import neat.genome
import game
import itertools
import math


def weight_scores(min_score: float, score: int) -> float:
    if score < min_score:
        return score
    return min_score + 0.5*(math.log(score - min_score + 1))


class NeuralNetworkController(game.player.controller.Controller):
    def __init__(
        self,
        genome: neat.genome.DefaultGenome,
        config,
        alpha_value: int = 1,
        color: Tuple[int, int, int] = (255, 0, 0),
    ):
        super().__init__(alpha_value, color)
        self.genome = genome
        self.config = config
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.fitnesses = []
        self.moves: Dict[game.player_action.PlayerAction, int] = {
            game.player_action.PlayerAction.STAY: 0,
            game.player_action.PlayerAction.UP: 0,
            game.player_action.PlayerAction.DOWN: 0,
            game.player_action.PlayerAction.LEFT: 0,
            game.player_action.PlayerAction.RIGHT: 0,
        }

    def get_action(self, inputs):
        flat_list = list(
            itertools.chain.from_iterable(
                (i if isinstance(i, list) else [i] for i in inputs)
            )
        )
        flat_list = list(
            itertools.chain.from_iterable(
                (i if isinstance(i, tuple) else [i] for i in flat_list)
            )
        )
        output = self.net.activate(tuple(flat_list))
        move = game.player_action.PlayerAction(output.index(max(output)))
        self.moves[move] += 1
        return move

    def set_fitness(self, fitness):
        self.fitnesses.append(fitness)

    def calc_fitness(self):
        min_score = self.calculate_weighted_average_of_worst_games()
        total_fitness: float = 0
        for fitness in self.fitnesses:
            total_fitness += weight_scores(min_score, fitness)
        self.genome.fitness = total_fitness / len(self.fitnesses)

    def calculate_weighted_average_of_worst_games(self) -> float:
        """ "this is used so that minor improvements have a bigger impact on the fitness"""
        fitnesses = self.fitnesses.copy()
        worst_fitnesses: list[int] = []

        for _ in range(6):
            min_fitness = min(fitnesses)
            worst_fitnesses.append(min_fitness)
            fitnesses.remove(min_fitness)
        weighted_sum = worst_fitnesses[0] * 70
        weighted_sum = weighted_sum + worst_fitnesses[1] * 20
        weighted_sum = weighted_sum + worst_fitnesses[2] * 7
        weighted_sum = weighted_sum + worst_fitnesses[3] * 2
        weighted_sum = weighted_sum + worst_fitnesses[4]
        return weighted_sum / 100

    def get_max_score(self):
        max_value = max(self.fitnesses)
        return f"{max_value} in Game {[i for i, x in enumerate(self.fitnesses) if x == max_value]}"

    def get_min_value(self):
        min_value = min(self.fitnesses)
        return f"{min_value} in Game {[i for i, x in enumerate(self.fitnesses) if x == min_value]}"

    def get_score_distribution(self):
        max_value = max(self.fitnesses)
        out_put: str = ""
        for i in range(max_value, -1, -1):
            game_indexes = [
                game_index for game_index, x in enumerate(self.fitnesses) if x == i
            ]
            if len(game_indexes) > 0:
                out_put += f"{i} : {[game_index for game_index, x in enumerate(self.fitnesses) if x == i]}, "
        return out_put

    def __str__(self):
        avg_score = sum(self.fitnesses) / len(self.fitnesses)
        return f"Genome({self.genome.key}), fitness ({self.genome.fitness}), avg({avg_score}), Score distribution ({self.get_score_distribution()})"
