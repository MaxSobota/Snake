import numpy as np
from neuralnetwork import NeuralNetwork
# The neural network which powers each snake's decision making

"""
NN setup:
- 28 neuron input layer (8 way vision with 3 values each + 4 neurons for head direction)
- 10 neuron hidden layer
- 3 neuron output layer (turn left, turn right, go straight)
"""

class SnakeAgent:
    def __init__(self, brain=None):
        neurons = [22, 40, 22, 3]
        activations = ["relu", "relu", "softmax"]

        if not brain:
            self.brain = NeuralNetwork(len(neurons), neurons, activations)
        else:
            self.brain = brain

        # Environment stuff
        self.score = 0
        self.alive = True
        self.steps = 0
        self.steps_without_food = 0
    
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
            if val == item:
                if item != 4:
                    return distance
                return 1.0
            i += drow
            j += dcol
            distance += 1

        # Not the item we're looking for
        return 0.0
    
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
        inputs = np.zeros((22, ), dtype=float)

        # Once for each compass direction
        for i, dir in enumerate(compass):
            inputs[i] = self.first_found(grid, head_row, head_col, dir, 3) # Food
            inputs[i + 8] = self.first_found(grid, head_row, head_col, dir, 4) # Wall

        dr = env.food_positions[0][0] - head_row
        dc = env.food_positions[0][1] - head_col

        # Normalize to -1, 0, or 1
        dr = 0 if dr == 0 else (1 if dr > 0 else -1)
        dc = 0 if dc == 0 else (1 if dc > 0 else -1)

        inputs[16] = dr
        inputs[17] = dc


        # Direction neurons (N, E, S, W)
        if direction == [-1, 0]: # North
            correct = 18
        elif direction == [0, 1]: # East
            correct = 19
        elif direction == [1, 0]: # South
            correct = 20
        else: # West
            correct = 21
        inputs[correct] = 1
        
        return inputs

    # Make a prediction using the network
    def take_action(self, env):
        inputs = self.deconstruct_grid(env)

        outputs = self.brain.predict(inputs)

        action = np.argmax(outputs)

        self.steps += 1

        return action

    # Sets the agent's weights to the new weights
    def set_weights(self, weights):
        # Convert from list of np arrays to each layer
        for i in range(len(weights)):
            self.brain.layers[i] = weights[i]