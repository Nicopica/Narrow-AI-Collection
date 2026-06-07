import numpy as np

from Layer import Layer
from utils import get_predictions, get_accuracy


class ArtificialNeuralNetwork:
    def __init__(self, data, epochs, learning_rate, neuron_layers,
                 training_percentage, validation_percentage, test_percentage=None, extra_data_set=None):

        np.random.seed(666)
        np.random.shuffle(data)

        m_total = data.shape[0]
        y_total = data.shape[1]

        train_end = int(m_total * training_percentage)
        val_end = train_end + int(m_total * validation_percentage)

        # split data and normalization
        data_train = data[0:train_end].T
        self.Y_train = data_train[0]
        self.X_train = data_train[1:y_total] / 255.0

        data_val = data[train_end:val_end].T
        self.Y_val = data_val[0]
        self.X_val = data_val[1:y_total] / 255.0

        data_test = data[val_end:m_total].T
        self.Y_test = data_test[0]
        self.X_test = data_test[1:y_total] / 255.0

        self.learning_rate = learning_rate
        self.epochs = epochs

        self.layers = []

        # self.last_layer = None

        self.set_up_layers(data.shape[1] - 1, neuron_layers)

        # self.extra_data_set = (extra_data_set[0][1:] / 255.0 ).reshape(784, 1)
    def set_up_layers(self, input_size, neuron_layers):
        self.layers = []
        last_layer_output = input_size

        for quantity_neurons in neuron_layers:
            new_layer = Layer(last_layer_output, quantity_neurons)
            self.layers.append(new_layer)

            last_layer_output = quantity_neurons

        self.layers[-1].is_output_layer = True

        self.layers = []
        last_layer_output = input_size

        for quantity_neurons in neuron_layers:
            new_layer = Layer(last_layer_output, quantity_neurons)
            self.layers.append(new_layer)

            last_layer_output = quantity_neurons

        self.layers[-1].is_output_layer = True


    def network_forward_propagation(self, input_data):
        current_input = input_data

        for layer in self.layers:
            current_input = layer.forward_propagation(current_input)

        return current_input

    def network_calculate_error(self):
        next_w = None
        next_d_raw = None

        for i in reversed(range(len(self.layers))):
            current_layer = self.layers[i]

            # take activations from layer behind it (or the raw image pixels)
            prev_a = self.layers[i - 1].active if i > 0 else self.X_train

            current_layer.calculate_error(
                expected_y=self.Y_train,
                next_weight=next_w,
                next_d_raw=next_d_raw,
                prev_active=prev_a
            )

            next_w = current_layer.weight
            next_d_raw = current_layer.d_raw


    def network_update_weights(self):
        for layer in self.layers:
            layer.update_weights(self.learning_rate, layer.d_weight, layer.d_bias)

    def print_progress(self, i):
        predictions = get_predictions(self.layers[-1].active)
        acc = get_accuracy(predictions, self.Y_train)
        print(f"Epoch: {i} | Training Accuracy: {acc * 100:.2f}%")

    def run(self):
        for i in range(self.epochs):
            self.network_forward_propagation(self.X_train)

            self.network_calculate_error()

            self.network_update_weights()

            # if i % 10 == 0 or i == self.epochs - 1:
            self.print_progress(i)

        self.evaluate_set(self.X_val, self.Y_val, "Validation")
        self.evaluate_set(self.X_test, self.Y_test, "Test")

        # for i in range(10):
        #     print(f"{i}:  {self.network_forward_propagation(self.extra_data_set)[i][0] * 100}")

    def evaluate_set(self, x_set, y_set, message="Set"):
        final_A = self.network_forward_propagation(x_set)
        val = get_accuracy(get_predictions(final_A), y_set)
        print(f"{message} Accuracy: {val * 100:.2f}%")