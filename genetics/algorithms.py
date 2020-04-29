import random
import numpy as np

from .network import CreateNetwork


class Subject:

    def __init__(self):
        self.network = CreateNetwork()
        self.fitness = 0

    def SetFitness(self, val):
        self.fitness = val

    def GetFitness(self):
        return self.fitness

    def MovementPrediction(self, model_input):
        model_input = np.array([model_input])
        response = self.network.predict(model_input)[0].tolist()
        return response.index(max(response))


def Mutation(layers, mutation_factor: float):
    i = random.randrange(0, len(layers))
    j = random.randrange(0, len(layers[i]))
    k = random.randrange(0, len(layers[i][j]))
    if random.random() <= mutation_factor:
        layers[i][j][k] += random.uniform(-10, 10)

    return layers


def UniformCrossover(parent1, parent2):
    subject1_layers = parent1.network.get_weights()
    subject2_layers = parent2.network.get_weights()
    child_layers = np.copy(subject1_layers)

    for layer in range(len(child_layers)):
        for neuron in range(len(child_layers[layer])):
            for weight in range(len(child_layers[layer][neuron])):
                child_layers[layer][neuron][weight] = random.uniform(subject1_layers[layer][neuron][weight],
                                                                     subject2_layers[layer][neuron][weight])

    return child_layers


def CreatePopulation(pop_size=5):
    population = []

    for i in range(pop_size):
        population.append(Subject())

    return population


def EvolvePopulation(population, mutation_factor=0.1):
    parent1 = population[-1]
    parent2 = population[-2]

    print(" [i] Parent 1 fitness: %i" % parent1.GetFitness())
    print(" [i] Parent 2 fitness: %i" % parent2.GetFitness())

    for i in range(len(population) - 2):
        child_layers = Mutation(UniformCrossover(parent1, parent2), mutation_factor)
        population[i].network.set_weights(child_layers)

    population[-1] = parent1

    return population


def SortPopulation(population, boards):
    def GetFitness(item):
        return item[0].GetFitness()

    z = sorted(zip(population, boards), key=GetFitness)

    sorted_population = []
    sorted_boards = []

    for pop, board in z:
        sorted_population.append(pop)
        sorted_boards.append(board)

    return sorted_population, sorted_boards
