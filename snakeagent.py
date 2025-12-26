import numpy as np

# The neural network which powers each snake's decision making

"""
NN setup:
- 28 neuron input layer (8 way vision with 3 values each + 4 neurons for head direction)
- 10 neuron hidden layer
- 3 neuron output layer (turn left, turn right, go straight)
"""

class SnakeAgent:
    def __init__(self):
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
    
    # Helper which returns T/F whether the item is the closest thing to the snake head
    def first_found(self, grid, row, col, direction, item):
        drow = direction[0]
        dcol = direction[1]

        rows, cols = grid.shape
        i, j = row + drow, col + dcol
        distance = 1

        while 0 <= i < rows and 0 <= j < cols:
            val = grid[i, j]

            # If not an empty square
            if val != 0:
                if val == 4:
                    return distance
                return val == item
            i += drow
            j += dcol
            distance += 1

        # Not the item we're looking for
        return False
    
    # Takes in grid state and returns vision inputs
    def deconstruct_grid(self, env):
        compass = [
            (-1, 0), # North
            (1, 0), # South
            (0, 1), # East
            (0, -1), # West
            (-1, -1), # Northwest
            (-1, 1), # Northeast
            (1, -1), # Southwest
            (1, 1) # Southeast
        ]
        
        grid = env.grid
        head_row = env.head_pos[0]
        head_col = env.head_pos[1]
        direction = env.previous_direction

        # 8 vision * (wall next to head y/n, food y/n, body y/n) + 4 directions
        inputs = np.zeros((28, ))

        # Once for each compass direction
        for i, dir in enumerate(compass):
            inputs[i] = self.first_found(grid, head_row, head_col, dir, 3) # Food
            inputs[i + 8] = self.first_found(grid, head_row, head_col, dir, 2) # Body
            inputs[i + 16] = self.first_found(grid, head_row, head_col, dir, 4) # Wall

        # Direction neurons (N, E, S, W)
        if direction == [-1, 0]: # North
            correct = 24
        elif direction == [0, 1]: # East
            correct = 25
        elif direction == [-1, 0]: # South
            correct = 26
        else: # West
            correct = 27
        inputs[correct] = 1

        return inputs

    # Make a prediction using the network
    def take_action(self, env):
        inputs = self.deconstruct_grid(env)

        # Multiply inputs with input neuron weights and use activation function to get inputs for hidden layer
        hiddens_1 = self.fire_neurons(inputs, self.hidden_weights_1, self.relu)

        hiddens_2 = self.fire_neurons(hiddens_1, self.hidden_weights_2, self.relu)

        # Multiply inputs with hidden neuron weights
        outputs = self.fire_neurons(hiddens_2, self.output_weights, self.softmax)

        action = np.argmax(outputs)

        self.steps += 1

        return action
    
    def init_network(self):
        # Randomly initialize weights
        # Inputs -> Hidden
        self.hidden_weights_1 = np.random.randn(28, 20) * 0.1
        self.hidden_weights_2 = np.random.randn(20, 10) * 0.1
        # Hidden -> Output
        self.output_weights = np.random.randn(10, 3) * 0.1

        self.weights = np.concatenate([self.hidden_weights_1.ravel(), self.hidden_weights_2.ravel(), self.output_weights.ravel()])

        # Environment stuff
        self.score = 0
        self.alive = True
        self.steps = 0

    # Sets the agent's weights to the new weights
    def set_weights(self, weights):
        self.weights = weights
        
        # Un-flatten weights (lol)
        self.hidden_weights_1 = weights[:self.hidden_weights_1.size].reshape(self.hidden_weights_1.shape[0], self.hidden_weights_1.shape[1])
        self.hidden_weights_2 = weights[self.hidden_weights_1.size:self.hidden_weights_1.size + self.hidden_weights_2.size].reshape(self.hidden_weights_2.shape[0], self.hidden_weights_2.shape[1])
        self.output_weights = weights[self.hidden_weights_1.size + self.hidden_weights_2.size:].reshape(self.output_weights.shape[0], self.output_weights.shape[1])
