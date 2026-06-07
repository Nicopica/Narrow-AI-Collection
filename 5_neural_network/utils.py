import numpy as np

def relu(z):
    return np.maximum(0, z)

# turns probabilities into final result
def softmax(z):
    expZ = np.exp(z - np.max(z, axis=0))
    return expZ / np.sum(expZ, axis=0)

def relu_derivative(z):
    return z > 0

def one_hot_encode(y):
    # converts 3 into [0, 0, 0, 1, 0, 0, 0, 0, 0, 0]
    one_hot = np.zeros((y.size, 10))
    one_hot[np.arange(y.size), y] = 1
    return one_hot.T

def get_predictions(a2):
    return np.argmax(a2, axis=0)


def get_accuracy(predictions, y):
    return np.sum(predictions == y) / y.size