import numpy as np
import pandas as pd

from ArtificialNeuralNetwork import ArtificialNeuralNetwork
from convert_img import convert_images_to_csv

HIDDEN_NEURONS = 64



def main():
    data = pd.read_csv('data/assignment5.csv')
    data = np.array(data)

    my_neural_network = ArtificialNeuralNetwork(
                            data=data,
                            epochs=50,
                            learning_rate=0.15,
                            neuron_layers=[784, 64, 10],
                            training_percentage=0.70,
                            validation_percentage=0.10
    )

    my_neural_network.run()

if __name__ == "__main__":
    main()