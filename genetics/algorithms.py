import random
import numpy as np

from .network import Network


class Subject:

    def __init__(self):
        self.network = Network(12, 5)
        self.fitness = 0

    def SetFitness(self, val):
        self.fitness = val

    def GetFitness(self):
        return self.fitness

    def MovementPrediction(self, model_input):
        model_input = np.array([model_input])
        response = self.network.Predict(model_input)[0].tolist()
        return response.index(max(response))


def Mutation(layers, mutation_factor: float):
    i = random.randrange(0, len(layers))
    j = random.randrange(0, len(layers[i]))
    k = random.randrange(0, len(layers[i][j]))
    if random.random() <= mutation_factor:
        layers[i][j][k] += random.uniform(-10, 10)

    return layers


def TwoPointsCrossover(subject1: Subject, subject2: Subject):
    subject1_layers = subject1.network.GetLayers()
    subject2_layers = subject2.network.GetLayers()
    child_layers = []

    for i in range(len(subject1_layers)):
        child_layer = []
        for j in range(len(subject1_layers[i])):
            subject1_neuron = subject1_layers[i][j].tolist()
            subject2_neuron = subject2_layers[i][j].tolist()

            slice_point1 = int(len(subject1_neuron) / 3)
            slice_point2 = slice_point1 * 2
            child_neuron = subject1_neuron[:slice_point1] + \
                           subject2_neuron[slice_point1:slice_point2] + \
                           subject1_neuron[slice_point2:]

            child_layer.append(np.array(child_neuron))

        child_layers.append(np.array(child_layer))

    return np.array(child_layers)


def UniformCrossover(subject1: Subject, subject2: Subject):
    subject1_layers = subject1.network.GetLayers()
    subject2_layers = subject2.network.GetLayers()
    child_layers = []

    for i in range(len(subject1_layers)):
        child_layer = []
        for j in range(len(subject1_layers[i])):
            child_neuron = []

            for k in range(len(subject1_layers[i][j])):
                weight1 = subject1_layers[i][j][k]
                weight2 = subject2_layers[i][j][k]
                child_weight = random.uniform(weight1, weight2)

                child_neuron.append(child_weight)

            child_layer.append(np.array(child_neuron))

        child_layers.append(np.array(child_layer))

    return np.array(child_layers)


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
        population[i].network.SetLayers(child_layers)

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
