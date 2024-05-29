from typing import Dict, Tuple
import neat
import neat.genome
import game
import itertools


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
        fitness_unweighted = sum(self.fitnesses) / len(self.fitnesses)
        # calc prozentual moves
        total_moves = sum(self.moves.values())
        percentage_moves = {
            action: count / total_moves * 100 for action, count in self.moves.items()
        }
        self.genome.fitness = 0
        if (
            percentage_moves[game.player_action.PlayerAction.STAY] > 25
            and percentage_moves[game.player_action.PlayerAction.STAY] < 55
        ):
            self.genome.fitness = fitness_unweighted * 0.2
        if (
            percentage_moves[game.player_action.PlayerAction.UP] > 25
            and percentage_moves[game.player_action.PlayerAction.UP] < 55
        ):
            self.genome.fitness += fitness_unweighted * 0.2
        if (
            percentage_moves[game.player_action.PlayerAction.DOWN] > 0.1
            and percentage_moves[game.player_action.PlayerAction.DOWN] < 2
        ):
            self.genome.fitness += fitness_unweighted * 0.2
        if (
            percentage_moves[game.player_action.PlayerAction.LEFT] > 3
            and percentage_moves[game.player_action.PlayerAction.LEFT] < 14
        ):
            self.genome.fitness += fitness_unweighted * 0.2
        if (
            percentage_moves[game.player_action.PlayerAction.RIGHT] > 3
            and percentage_moves[game.player_action.PlayerAction.RIGHT] < 14
        ):
            self.genome.fitness += fitness_unweighted * 0.2
        self.genome.fitness += fitness_unweighted

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
                out_put += f"{i} in Game(s) {[game_index for game_index, x in enumerate(self.fitnesses) if x == i]}, "
        return out_put

    def __str__(self):
        return f"Genome({self.genome.key}),fitness ({self.genome.fitness}), Score distribution ({self.get_score_distribution()})"
