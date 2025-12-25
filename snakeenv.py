from collections import deque
import numpy as np

class SnakeEnv:
    def __init__(self, dimensions=[15, 15], max_food=1): # Will replace with kwargs later?
        # Bounds checking
        if dimensions[0] <= 4 or dimensions[1] <= 4:
            raise ValueError("Error: Grid size must be at least 5x5.")
        
        if max_food <= 0:
            raise ValueError("Error: Max food must be at least 1.")
        
        # Snake environment is a gridworld, size can be defined by user
        self.dimensions = dimensions

        # Number of food can be set by user too
        self.max_food = max_food
        self.food_positions = []

    def reset(self):
        self.head_pos = [self.dimensions[0] // 2, self.dimensions[1] // 2]
        self.body = deque()

        self.food_positions = []
        self.steps = 0

        # Remake the grid state
        self.update_grid()

        # Spawn initial food
        self.spawn_food(self.max_food)

        self.score = 0
        self.previous_direction = [0, 0]
    
    def action_to_direction(self, action): # Helper function for moving the snake's head
        if action == 0: # Up
            direction = [-1, 0]
        elif action == 1: # Down
            direction = [1, 0]
        elif action == 2: # Left
            direction = [0, -1]
        elif action == 3: # Right
            direction = [0, 1]

        # Prevent snake moving backwards into itself
        if self.previous_direction[0] == (direction[0] * -1) and self.previous_direction[1] == (direction[1] * -1):
            direction = self.previous_direction

        self.previous_direction = direction

        return direction
        
    def update_grid(self):
        # Initialize empty grid
        self.grid = np.zeros((self.dimensions[0], self.dimensions[1]))

        # Add walls
        self.grid[0, :] = 4
        self.grid[-1, :] = 4
        self.grid[:, 0] = 4
        self.grid[:, -1] = 4

        # Add snake parts
        self.grid[self.head_pos[0], self.head_pos[1]] = 1
        for part in self.body:
            self.grid[part[0], part[1]] = 2

        # Add food
        for pos in self.food_positions:
            self.grid[pos[0], pos[1]] = 3

    def spawn_food(self, num_food):
        # Spawn food in open positions
        for _ in range(num_food):
            open = np.argwhere(self.grid == 0)

            row, col = open[np.random.choice(len(open))]

            self.food_positions.append([row, col])

    def step(self, action):
        self.steps += 1

        # Timer to stop going in circles
        if self.steps >= 100:
            return False

        action_pos = self.action_to_direction(action)

        # Get new head position
        new_pos = [self.head_pos[0] + action_pos[0], self.head_pos[1] + action_pos[1]]

        # If moving snake head to new location hits wall, end episode
        if self.grid[new_pos[0], new_pos[1]] == 4:
            return False

        # If moving snake head to new location hits itself, end episode
        if new_pos in self.body:
            return False

        # If not, add current head position to body
        self.body.appendleft(self.head_pos)

        # Move head based on action
        self.head_pos = new_pos

        # If snake eats food, spawn 1 new food and don't remove last body segment
        if self.head_pos in self.food_positions:
            self.food_positions.remove(self.head_pos)
            self.spawn_food(1)
            self.score += 1

            # Reset timer
            self.steps = 0

            # Check for win condition
            if self.score == len(self.grid) - 1:
                exit(0)
        else:
            # Remove last body segment location
            self.body.pop()

        self.update_grid()

        return True