import neat
import neat.genome
import game
import itertools


class NeuralNetworkController(game.player.controller.Controller):
    def __init__(self, genome:neat.genome.DefaultGenome, config):
        self.genome = genome
        self.config = config
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.fitnesses = []

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
        return game.player_action.PlayerAction(output.index(max(output)))

    def set_fitness(self, fitness):
        self.fitnesses.append(fitness)

    def calc_fitness(self):
        self.genome.fitness = sum(self.fitnesses) / len(self.fitnesses)

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
            game_indexes = [game_index for game_index, x in enumerate(self.fitnesses) if x == i]
            if len(game_indexes) > 0:
                out_put += f"{i} in Game(s) {[game_index for game_index, x in enumerate(self.fitnesses) if x == i]}, "
        return out_put

    def __str__(self):
        return f"Genome({self.genome.key}),Species ({self.genome.s}),fitness ({self.genome.fitness}), Score distribution ({self.get_score_distribution()})"
