import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def tanh(x):
    return np.tanh(x)


class Layer:
    def __init__(self):
        self.input = None
        self.output = None

    def forward_propagation(self, input_data):
        raise NotImplementedError


class FCLayer(Layer):

    def __init__(self, input_size, output_size):
        super().__init__()
        self.weights = np.random.rand(input_size, output_size) - 0.5
        self.bias = np.random.rand(1, output_size) - 0.5

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = np.dot(self.input, self.weights) + self.bias
        return self.output


class ActivationLayer(Layer):

    def __init__(self, activation):
        super().__init__()
        self.activation = activation

    def forward_propagation(self, input_data):
        self.input = input_data
        self.output = self.activation(self.input)
        return self.output


class Network:

    def __init__(self):
        self.layers = []

    def add(self, layer):
        self.layers.append(layer)

    def predict(self, input_data):
        output = input_data

        for layer in self.layers:
            output = layer.forward_propagation(output)

        return output

    def get_weights(self):
        weights = []

        for layer in self.layers:
            if type(layer).__name__ == "FCLayer":
                weights.append(layer.weights)

        return weights

    def set_weights(self, weights):
        i = 0
        for layer in self.layers:
            if type(layer).__name__ == "FCLayer":
                layer.weights = weights[i]
                i += 1


def CreateNetwork():
    network = Network()

    network.add(FCLayer(2, 20))
    network.add(ActivationLayer(tanh))
    network.add(FCLayer(20, 10))
    network.add(ActivationLayer(tanh))
    network.add(FCLayer(10, 2))
    network.add(ActivationLayer(tanh))

    return network
