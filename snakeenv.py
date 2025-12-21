import gymnasium as gym
import pygame

class SnakeEnv(gym.Env):
    def __init__(self, size = 10, render_mode = None):
        self.size = size

        # Snake environment is a gridworld, observation space size is defined by user
        self.observation_space = gym.spaces.Box()

        # Snake can move in 4 directions
        self.action_space = gym.spaces.Discrete(4)

        self.render_mode = render_mode
        self.window = None
        self.clock = None

    def reset(self, seed = None, options = None):
        return observation, reward, terminated, truncated, info

    def step(self, action):

        return observation, reward, terminated, truncated, info
    
    def render(self):
        # Use pygame or something similar to display the grid
        if self.render_mode == "human":
            print()
			