from snakeenv import SnakeEnv
from snakeagent import SnakeAgent
from renderer import Renderer
from geneticalgorithm import repopulate

import pickle

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
    renderer = Renderer(render_mode, render_fps=6000)

    # Agent/Environment pairs
    pairs = {}
    for _ in range(num_agents):
        pairs[SnakeAgent()] = SnakeEnv(dimensions=env_dimensions)

    for gen in range(num_episodes):
        # Put agents into a list so we can remove them one by one
        agents = list(pairs.keys())
        
        # Reset each agent's environment and values
        for agent, env in pairs.items():
            env.reset()
            agent.score = 0
            agent.alive = True
            agent.steps = 0
            agent.steps_without_food = 0

        # All agents equal at the start
        best_agent = agents[0]

        while(True):
            if render_mode == "single":
                renderer.render_single(list(pairs.values())[0].grid, list(pairs.keys())[0].score, gen)
            elif render_mode == "overlay":
                renderer.render_overlay(pairs, gen)
            elif render_mode == "best":
                renderer.render_single(pairs[best_agent].grid, best_agent.score, gen)
            
            # Move to next episode when all agents die
            count = len(agents)
            for agent in agents:
                if not agent.alive:
                    count -= 1
            if count == 0:
                break

            for agent in agents:
                # Stop agent playing if dead
                if not agent.alive:
                    continue

                # Each agent takes an action according to their gene policy
                action = agent.take_action(pairs[agent])

                # Update agent's info
                agent.alive = pairs[agent].step(action)
                agent.score = pairs[agent].score
                agent.steps_without_food = pairs[agent].steps_without_food

                # Agent beat the game, and therefore has the optimal policy
                if agent.score == (env_dimensions[0] - 2) * (env_dimensions[1] - 2):
                    return agent
                
                # Best agent = highest score while still alive
                # if agent.score > best_agent.score or not best_agent.alive:
                #     best_agent = agent
                if agent.score > best_agent.score:
                    with open("brain.pkl", "wb") as f:
                        pickle.dump(best_agent.brain, f)

        # At the end of each episode, create the next generation of agents
        new_population = repopulate(agents, num_offspring)

        # Set the new weights for each agent
        for i in range(num_agents):
            agents[i].set_weights(new_population[i])

def run_trained(brain, env_dimensions, max_food):
    renderer = Renderer(render_mode, render_fps=6000)

    agent = SnakeAgent(brain)
    env = SnakeEnv(env_dimensions, max_food)

    while(True):
        env.reset()
        agent.score = 0
        agent.alive = True
        agent.steps = 0
        agent.steps_without_food = 0

        while(agent.alive):
            renderer.render_single(env.grid, agent.score, 0)

            action = agent.take_action(env)

            # Update agent's info
            agent.alive = env.step(action)
            agent.score = env.score
            agent.steps_without_food = env.steps_without_food

def play(env_dimensions, max_food):
    env = SnakeEnv(env_dimensions, max_food)
    renderer = Renderer()

    while(True):
        env.reset()
        while(renderer.render_play(env)):
            pass

def get_params_1():
    render_mode = input("Enter render mode (human, single, overlay, play, none): ")

    if render_mode not in ["human", "single", "best", "overlay", "play"]:
        print("Render mode set to none.")
        render_mode = None

    # Grid size
    try:
        env_dimensions = []
        rows, cols = input("Enter grid dimensions in the form rows, cols: ").split(",")
        env_dimensions.append(int(rows.strip()))
        env_dimensions.append(int(cols.strip()))
    except Exception as e:
        print(f"Error, {e}")
        exit(1)

    if env_dimensions[0] < 5 or env_dimensions[1] < 5:
        print("Grid should be at least 5x5.")
        exit(1)

    # Food
    try:
        max_food = int(input("Enter maximum amount of food: "))
    except Exception as e:
        print(f"Error, {e}")
        exit(1)

    if max_food <= 0:
        print("Amount of food should be >= 1.")
        exit(1)

    return render_mode, env_dimensions, max_food

def get_params_2():
    try:
        num_agents = int(input("Enter number of agents per generation: "))
    except Exception as e:
        print(f"Error, {e}")
        exit(1)

    if num_agents <= 0:
        print("Number of agents should be >= 1.")
        exit(1)

    # How many iterations to train
    try:
        num_episodes = int(input("Enter number of episodes: "))
    except Exception as e:
        print(f"Error, {e}")
        exit(1)

    if num_episodes <= 0:
        print("Number of episodes should be >= 1.")
        exit(1)

    # How many children to produce per generation
    try:
        num_offspring = int(input("Enter number of offspring per generation: "))
    except Exception as e:
        print(f"Error, {e}")
        exit(1)

    if num_episodes <= 0:
        print("Number of offspring should be >= 1.")
        exit(1)

    return num_agents, num_episodes, num_offspring

if __name__ == "__main__":
    render_mode = "trained"
    env_dimensions = [15, 15]
    max_food = 1

    # render_mode, env_dimensions, max_food = get_params_1()

    if render_mode == "play":
        play(env_dimensions, max_food)
    elif render_mode == "trained":
        with open("brain.pkl", "rb") as f:
            brain = pickle.load(f)
        run_trained(brain, env_dimensions, max_food)
    else:
        # num_agents, num_episodes, num_offspring = get_params_2()
        num_agents = 150

        num_episodes = 1000

        num_offspring = 125

        optimal_agent = evaluate(num_agents, num_episodes, num_offspring, env_dimensions, render_mode)

    
    