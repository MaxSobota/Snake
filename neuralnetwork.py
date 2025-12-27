import numpy as np

# The 'brain' of each snake
class NeuralNetwork:
    def __init__(self, num_layers, neurons, activations):
        # Make sure the parameters match properly
        assert num_layers == len(neurons) == (len(activations) + 1)

        self.num_layers = num_layers
        self.neurons = neurons
        self.activations = self.map_activations(activations)

        self.init_network()

    # Helper function to map strings to activation functions
    def map_activations(self, activations):
        funcs = []
        for function in activations:
            if function == "relu":
                funcs.append(self.relu)
            else:
                funcs.append(self.softmax)

        return funcs

    # Hidden layer(s) activation function
    def relu(self, input):
        return np.maximum(0, input)

    # Output layer activation function
    def softmax(self, scores):
        stabilized = np.exp(scores - np.max(scores))
        return stabilized / np.sum(stabilized) 
    
    def fire_neurons(self, inputs, weights, activation):
        return activation(inputs @ weights)
    
    def init_network(self):
        self.layers = []

        # Randomly initialize neuron weights for each layer
        for i in range(self.num_layers - 1):
            neurons = np.random.normal(0, 1, (self.neurons[i], self.neurons[i + 1]))

            self.layers.append(neurons)

    def predict(self, inputs):
        values = inputs

        # Forward pass
        for i in range(len(self.layers)):
            # Multiply inputs with neuron weights and use activation function to get outputs
            values = self.fire_neurons(values, self.layers[i], self.activations[i])

        return values