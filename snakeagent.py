# The neural network which powers each snake's decision making
# import torch
import numpy as np

# Add direction snake was moving for better learning?

class SnakeAgent():
    def __init__(self, learning_rate = 1e-3, seed = None):
        self.learning_rate = learning_rate

        # Set seed for random numbers
        np.random.seed(seed)

    def take_action(self):
        action = np.random.randint(0, 4)
        return action