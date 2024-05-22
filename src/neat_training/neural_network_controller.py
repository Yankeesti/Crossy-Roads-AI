import neat
import game
import itertools


class NeuralNetworkController(game.player.controller.Controller):
    def __init__(self, genome, config):
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
