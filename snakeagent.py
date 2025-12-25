import numpy as np

# The neural network which powers each snake's decision making

"""
Possible inputs:
- 1 input for each grid square (excluding walls)
- 1 input for each snake segment (head + body)

Additional inputs:
- Last snake action
- Distance/direction to closest snake segment

NN setup:
- input layer (num neurons = num grid squares - walls)
- 1 hidden layer with 8 neurons for fun
- 4 neuron output layer
"""

class SnakeAgent:
    def __init__(self, num_inputs):
        # Number of input neurons
        self.num_inputs = num_inputs

        self.init_network()

    # Hidden layer activation function
    def relu(self, input):
        return np.maximum(0, input)

    # Output layer activation function
    def softmax(self, scores):
        stabilized = np.exp(scores - np.max(scores))
        return stabilized / np.sum(stabilized) 

    # Get the outputs for the layer by dot product and activation function on inputs/weights
    def fire_neurons(self, inputs, weights, activation):
        return activation(inputs @ weights)

    # Make a prediction using the network
    def take_action(self, inputs):
        # Flatten inputs to 1D numpy array
        inputs = np.array(inputs).ravel()

        # print(self.hidden_weights)

        # Multiply inputs with input neuron weights and use activation function to get inputs for hidden layer
        hiddens = self.fire_neurons(inputs, self.hidden_weights, self.relu)

        # Multiply inputs with hidden neuron weights
        outputs = self.fire_neurons(hiddens, self.output_weights, self.softmax)

        action = np.argmax(outputs)

        # print(f"action: {action}, probabilities: {outputs}, hiddens: {hiddens}")

        return action
    
    def init_network(self):
        # Randomly initialize weights
        # Inputs -> Hidden
        self.hidden_weights = np.random.randn(self.num_inputs, 8) * 0.1
        # Hidden -> Output
        self.output_weights = np.random.randn(8, 4) * 0.1

        self.weights = np.concatenate([self.hidden_weights.ravel(), self.output_weights.ravel()])

        # Environment stuff
        self.score = 0
        self.alive = True

    # Sets the agent's weights to the new weights
    def set_weights(self, weights):
        self.weights = weights
        
        # Un-flatten weights (lol)
        self.hidden_weights = weights[:self.hidden_weights.size].reshape(self.hidden_weights.shape[0], self.hidden_weights.shape[1])
        self.output_weights = weights[self.hidden_weights.size:].reshape(self.output_weights.shape[0], self.output_weights.shape[1])
