import numpy as np

from utils import relu, softmax, one_hot_encode, relu_derivative


class Layer:
    def __init__(self, input_neurons, output_neurons, is_output_layer=False):
        self.weight = np.random.randn(output_neurons, input_neurons) * np.sqrt(2. / input_neurons)
        self.bias = np.zeros((output_neurons, 1))

        self.is_output_layer = is_output_layer

        self.active = None
        self.raw = None
        self.size_set = None

        self.d_weight = None
        self.d_bias = None
        self.d_raw = None

    def forward_propagation(self, x_train):
        raw = self.weight.dot(x_train) + self.bias

        if self.is_output_layer:
            active = softmax(raw)
        else:
            active = relu(raw)

        self.active = active
        self.raw = raw
        self.size_set = x_train.shape[1]

        return active

    def calculate_error(self, expected_y=None, next_weight=None, next_d_raw=None, prev_active=None):

        if self.is_output_layer:
            one_hot_expected = one_hot_encode(expected_y)

            self.d_raw = self.active - one_hot_expected
            self.d_weight = (1 / self.size_set) * self.d_raw.dot(prev_active.T)
            self.d_bias = (1 / self.size_set) * np.sum(self.d_raw, axis=1, keepdims=True)

        else:
            self.d_raw = next_weight.T.dot(next_d_raw) * relu_derivative(self.raw)
            self.d_weight = (1 / self.size_set) * self.d_raw.dot(prev_active.T)
            self.d_bias = (1 / self.size_set) * np.sum(self.d_raw, axis=1, keepdims=True)

    def update_weights(self, learning_rate, d_weight, d_bias):
        self.weight = self.weight - learning_rate * d_weight
        self.bias = self.bias - learning_rate * d_bias


