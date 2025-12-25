import pygame
"""
TODO: Add render modes
- human
- play
- game
- none

TODO: Fix window size
TODO: Fix death logic

"""

# A helper class which renders the game environment
class Renderer:
    def __init__(self, render_mode=None, render_fps=5):
        # Rendering with pygame
        self.screen = None
        self.clock = None
        self.render_mode = render_mode
        self.render_fps = render_fps # Default 5 FPS

        self.last_action = 0

    def close(self): 
        # Shutdown pygame properly
        if self.screen != None:
            pygame.quit()

    def render_frame(self, grid, score, generation):
        # Initialize screen on first render call
        if self.screen == None: 
            # Start pygame
            pygame.init() 

            # Initialize window
            window_width = 800
            window_height = 850
            self.screen = pygame.display.set_mode((window_width, window_height))
            pygame.display.set_caption(f"Snake - {self.render_mode}")

            # Start clock
            self.clock = pygame.time.Clock()

            # Set font for score
            self.font = pygame.font.SysFont(None, 28)

        # Get grid dimensions
        self.size = grid.shape

        # Clear screen (white background)
        self.screen.fill((255, 255, 255))

        # Score info
        pygame.draw.rect(
            self.screen,
            (200, 200, 200),
            pygame.Rect(0, 0, self.screen.get_width(), 50)
        )

        score_text = self.font.render(f"SCORE: {score}", True, (0, 0, 0))
        generation_text = self.font.render(f"GENERATION: {generation}", True, (0, 0, 0))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(generation_text, (200, 10))

        # Colors for grid objects
        colors = {
            0: (220, 220, 220), # Empty = light gray
            1: (42, 165, 8), # Snake head = dark green
            2: (59, 226, 13), # Snake body = light green
            3: (226, 20, 13), # Food = red
            4: (40, 40, 40) # Wall = dark grey
        }

        cell_size = min(800 // self.size[1], 800 // self.size[0])

        # Draw the grid state
        for row in range(self.size[0]):
            for col in range(self.size[1]):
                value = grid[row, col]
                color = colors[value]

                # Draw each grid square to fit inside screen
                rect = pygame.Rect( 
                    col * cell_size,
                    row * cell_size + 50, # Moved down for score
                    cell_size,
                    cell_size
                )

                pygame.draw.rect(self.screen, color, rect)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, 1) # Grid lines
        
    def render_single(self, grid, score, generation):
        # TODO: Add label for current agent ID
        self.render_frame(grid, score, generation)

        for event in pygame.event.get():
            # Quit early if we click the X
            if event.type == pygame.QUIT:
                self.close()
            
        pygame.display.flip()

        # Move game forward
        self.clock.tick(self.render_fps)

    def render_play(self, env):
        self.render_frame(env.grid, env.score, 0)
        
        for event in pygame.event.get():
            # Quit early if we click the X
            if event.type == pygame.QUIT:
                self.close()

            # Handle user inputs
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: # Up
                    self.last_action = 0
                elif event.key == pygame.K_s: # Down
                    self.last_action = 1
                elif event.key == pygame.K_a: # Left
                    self.last_action = 2
                elif event.key == pygame.K_d: # Right
                    self.last_action = 3

        alive = env.step(self.last_action)

        pygame.display.flip()

        # Move game forward
        self.clock.tick(self.render_fps)

        if not alive:
            self.close()
            return False

        return True