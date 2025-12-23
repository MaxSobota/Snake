from queue import Queue
import numpy as np
import pygame

class SnakeEnv():
    def __init__(self, size = [10, 10], max_food = 1, render_mode = None, render_fps = 5): # Will replace with kwargs later?
        # Bounds checking
        if size[0] <= 4 or size[1] <= 4:
            raise ValueError("Error: Grid size must be at least 5x5.")
        
        if max_food <= 0:
            raise ValueError("Error: Max food must be at least 1.")
        
        # Snake environment is a gridworld, size is defined by user
        self.size = size

        # Number of food can be set by user too
        self.max_food = max_food

        # Can run without a visual if needed
        self.render_mode = render_mode

        # Rendering with pygame
        self.cell_size = 64 # Pixels per grid cell
        self.screen = None
        self.clock = None
        self.render_fps = render_fps # Default 5 FPS

    def close(self): 
        # Shutdown pygame properly
        if self.screen != None:
            pygame.quit()

    def reset(self, seed = None):
        # Set seed for random numbers
        np.random.seed(seed)

        # Initialize empty grid
        self.grid = np.zeros((self.size[0], self.size[1]))

        # Add walls
        self.grid[0, :] = 1
        self.grid[-1, :] = 1
        self.grid[:, 0] = 1
        self.grid[:, -1] = 1

        # TODO: Spawn snake in random place or in same place each episode?
        self.head_pos = [np.random.randint(1, self.size[0] - 1), np.random.randint(1, self.size[1] - 1)]
        self.body = Queue() # A snake is literally a queue, with head and tail

        self.render()
        return 

    def step(self, action):
        # TODO: If moving snake head to new location hits wall/itself, end episode
        # TODO: If not, add current head position to body queue
        # TODO: Move head based on action
        # TODO: Remove last body segment location

        self.render()
        return 
    
    def render(self):
        # Use pygame to display the grid state
        if self.render_mode == "human":
            if self.screen == None: # Initialize screen on first render call
                # Start pygame
                pygame.init() 

                # Initialize window
                window_width = self.size[1] * self.cell_size
                window_height = self.size[0] * self.cell_size
                self.screen = pygame.display.set_mode((window_width, window_height))
                pygame.display.set_caption("Snake")

                # Start clock
                self.clock = pygame.time.Clock()

        # Clear screen (white background)
        self.screen.fill((255, 255, 255))

        # Colors for grid objects
        colors = {
            0: (220, 220, 220), # Empty = light gray
            1: (42, 165, 8), # Snake head = dark green
            2: (59, 226, 13), # Snake body = light green
            3: (226, 20, 13), # Food = red
            4: (40, 40, 40) # Wall = dark grey
        }

        # Draw the grid state
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                value = self.grid[row, col]
                color = colors[value]

                # Draw each grid square
                rect = pygame.Rect( 
                    col * self.cell_size,
                    row * self.cell_size,
                    self.cell_size,
                    self.cell_size
                )

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1) # Grid lines

        # Quit early if we click the X
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit(0)

        pygame.display.flip()

        # Move game forward
        self.clock.tick(self.render_fps)
			
    def fitness(self):
        # Function defining how well a species performs
        fitness = self.food_eaten - 0.1 * self.survival_time
        return fitness
