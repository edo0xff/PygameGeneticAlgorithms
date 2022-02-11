import random
import numpy as np


class Genome:

    def __init__(self, network):
        self.network = network
        self.fitness = 0

    def SetFitness(self, val):
        self.fitness = val

    def GetFitness(self):
        return self.fitness

    def Inference(self, model_input):
        response = self.network.Predict(np.array([model_input]))[0].tolist()
        return response.index(max(response))


def Mutation(layers, mutation_factor: float):
    i = random.randrange(0, len(layers))
    j = random.randrange(0, len(layers[i]))
    k = random.randrange(0, len(layers[i][j]))
    if random.random() <= mutation_factor:
        print(" [i] A mutation has appeared in gnoma (%s/%s/%s)" % (i,j,k))
        layers[i][j][k] += random.uniform(-10, 10)

    return layers


def UniformCrossover(parent1, parent2):
    subject1_layers = parent1.network.GetWeights()
    subject2_layers = parent2.network.GetWeights()
    child_layers = np.copy(subject1_layers)

    for layer in range(len(child_layers)):
        for neuron in range(len(child_layers[layer])):
            for weight in range(len(child_layers[layer][neuron])):
                child_layers[layer][neuron][weight] = random.choice([subject1_layers[layer][neuron][weight],
                                                                     subject2_layers[layer][neuron][weight]])

    return child_layers


def CreatePopulation(network, pop_size=5):
    return [Genome(network) for _ in range(pop_size)]


def SortPopulation(population):
    def GetFitness(item):
        return item.GetFitness()

    return sorted(population, key=GetFitness)


def EvolvePopulation(population, mutation_factor=0.1):
    population = SortPopulation(population)

    parent1 = population[-1]
    parent2 = population[-2]

    print(" [i] Parent 1 fitness: %i" % parent1.GetFitness())
    print(" [i] Parent 2 fitness: %i" % parent2.GetFitness())

    for i in range(len(population) - 2):
        child_layers = Mutation(UniformCrossover(parent1, parent2), mutation_factor)
        population[i].network.SetWeights(child_layers)

    return population
