import numpy as np


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


class Network:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.weights1 = np.random.uniform(-10, 10, (x, 12))
        self.weights2 = np.random.uniform(-10, 10, (12, 50))
        self.weights3 = np.random.uniform(-10, 10, (50, 25))
        self.weights4 = np.random.uniform(-10, 10, (25, 5))
        self.output = np.zeros(y)

    def GetLayers(self):
        return [self.weights1, self.weights2, self.weights3, self.weights4]

    def SetLayers(self, layers):
        self.weights1 = layers[0]
        self.weights2 = layers[1]
        self.weights3 = layers[2]
        self.weights4 = layers[3]

    def Predict(self, net_input):
        layer1 = sigmoid(np.dot(net_input, self.weights1))
        layer2 = sigmoid(np.dot(layer1, self.weights2))
        layer3 = sigmoid(np.dot(layer2, self.weights3))

        self.output = sigmoid(np.dot(layer3, self.weights4))
        return self.output


if __name__ == "__main__":
    net = Network(15, 5)

    print(net.Predict(np.array([562,566,45,3,5,6,8,1,6,4,7,8,2,6,9])))
    print(net.Predict(np.array([0, 0, 0, 3, 5, 6, 8, 1, 8, 4, 7, 8, 2, 6, 9])))