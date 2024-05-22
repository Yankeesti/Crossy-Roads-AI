import neat
import game


class NeuralNetworkController(game.player.controller.Controller):
    def __init__(self, genome, config):
        self.genome = genome
        self.config = config
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)
        self.fitneses = []

    def get_action(self, inputs):
        output = self.net.activate(inputs)
        return game.player_action.PlayerAction(output.index(max(output)))

    def set_fitness(self, fitness):
        self.fitnesses.append(fitness)

    def calc_fitness(self):
        self.genome.fitness = sum(self.fitnesses) / len(self.fitnesses)
