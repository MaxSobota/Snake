from snakeenv import SnakeEnv
from snakeagent import SnakeAgent
from renderer import Renderer
from geneticalgorithm import repopulate

# Run this to train and evaluate the genetic algorithm
# TODO: Add separate training/evaluation functions
# TODO: Add stats for fun/graphing
# TODO: Add unique IDs/names to each pair
# TODO: Change inputting parameters to be easier

"""
Core loop:
- Evaluate species on game (rendered or not)
- Select top however many candidates
- Reproduce to create however many children
- Create n mutations of the children
- Repeat
"""

def evaluate(num_agents, num_episodes, num_offspring, env_dimensions, render_mode):
    renderer = Renderer(render_mode, render_fps=5)

    # Without wall padding
    env_size = (env_dimensions[0] - 2) * (env_dimensions[1] - 2)

    # Agent/Environment pairs
    pairs = {}
    for _ in range(num_agents):
        pairs[SnakeAgent(num_inputs=env_size)] = SnakeEnv(dimensions=env_dimensions)

    for gen in range(num_episodes):
        # Put agents into a list so we can remove them one by one
        agents = list(pairs.keys())
        alive_agents = agents.copy()
        
        # Reset each agent's environment
        for env in pairs.values():
            env.reset()

        # All agents equal at the start
        best_agent = agents[0]

        while(True):
            if render_mode == "single":
                renderer.render_single(pairs[best_agent].grid, pairs[best_agent].score, gen)
            elif render_mode == "overlay":
                renderer.render_overlay(pairs, gen)
            
            # Move to next episode when all agents die
            if len(alive_agents) == 0:
                break

            # Copy the agents list so we can remove agents while game is running
            for agent in alive_agents:
                # Pass grid without exterior walls
                unpadded_grid = pairs[agent].grid[1:-1, 1:-1]

                # Each agent takes an action according to their gene policy
                action = agent.take_action(unpadded_grid)

                # Update agent's info
                agent.alive = pairs[agent].step(action)
                agent.score = pairs[agent].score

                # Agent beat the game, and therefore has the optimal policy
                if agent.score == (env_dimensions[0] - 1) * (env_dimensions[1] - 1):
                    return agent
                
                # Stop agent playing if dead
                if not agent.alive:
                    alive_agents.remove(agent)

                # Best agent = highest score while still alive
                if agent.score > best_agent.score or not best_agent.alive:
                    best_agent = agent

        # At the end of each episode, create the next generation of agents
        new_population = repopulate(agents, num_offspring)

        # Set the new weights for each agent
        for i in range(num_agents):
            agents[i].set_weights(new_population[i])
            
def play(env_dimensions, max_food):
    env = SnakeEnv(env_dimensions, max_food)
    renderer = Renderer()

    env.reset()
    while(renderer.render_play(env)):
        pass

if __name__ == "__main__":
    # render_mode = input("Enter render mode (human, single, overlay, play, none): ")

    # if render_mode not in ["human", "single", "overlay", "play"]:
    #     print("Render mode set to none.")
    #     render_mode = None

    render_mode = "overlay"

    # # Grid size
    # try:
    #     env_dimensions = []
    #     rows, cols = input("Enter grid dimensions in the form rows, cols: ").split(",")
    #     env_dimensions.append(int(rows.strip()))
    #     env_dimensions.append(int(cols.strip()))
    # except Exception as e:
    #     print(f"Error, {e}")
    #     exit(1)

    # if env_dimensions[0] < 5 or env_dimensions[1] < 5:
    #     print("Grid should be at least 5x5.")
    #     exit(1)

    env_dimensions = [10, 10]

    # # Grid size
    # try:
    #     max_food = int(input("Enter maximum amount of food: "))
    # except Exception as e:
    #     print(f"Error, {e}")
    #     exit(1)

    # if max_food <= 0:
    #     print("Amount of food should be >= 1.")
    #     exit(1)
    
    max_food = 1

    if render_mode == "play":
        play(env_dimensions, max_food)
    else:
        # try:
        #     num_agents = int(input("Enter number of agents per generation: "))
        # except Exception as e:
        #     print(f"Error, {e}")
        #     exit(1)

        # if num_agents <= 0:
        #     print("Number of agents should be >= 1.")
        #     exit(1)

        num_agents = 5

        # How many iterations to train
        # try:
        #     num_episodes = int(input("Enter number of episodes: "))
        # except Exception as e:
        #     print(f"Error, {e}")
        #     exit(1)

        # if num_episodes <= 0:
        #     print("Number of episodes should be >= 1.")
        #     exit(1)
        num_episodes = 1000

        # How many children to produce per generation
        # try:
        #     num_offspring = int(input("Enter number of offspring per generation: "))
        # except Exception as e:
        #     print(f"Error, {e}")
        #     exit(1)

        # if num_episodes <= 0:
        #     print("Number of offspring should be >= 1.")
        #     exit(1)
        num_offspring = 3

        optimal_agent = evaluate(num_agents, num_episodes, num_offspring, env_dimensions, render_mode)
    

    
    