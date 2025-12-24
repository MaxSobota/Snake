from snakeenv import SnakeEnv
from snakeagent import SnakeAgent
from renderer import Renderer

# Run this to train and evaluate the genetic algorithm
# TODO: Add separate training/evaluation functions
# TODO: Add stats for fun

"""
Core loop:
- Evaluate species on game (rendered or not)
- Select top however many candidates
- Reproduce to create however many children
- Create n mutations of the children
- Repeat


population = [random_genome() for _ in range(N)]
for genome in population:
    fitness = play_game(genome)
    genome.fitness = fitness

"""

def evaluate(num_agents, num_episodes, render_mode):
    renderer = Renderer()

    for _ in range(num_episodes):
        # TODO: Add unique IDs/names to each pair
        # TODO: Change inputting parameters to be easier

        # Agent/Environment pairs
        pairs = {}
        for _ in range(num_agents):
            pairs[SnakeAgent()] = SnakeEnv(max_food=20)
            
        # Put agents into a list so we can remove them one by one
        agents = list(pairs.keys())
        for env in pairs.values():
            env.reset()

        best_agent = agents[0]

        while(True):
            if render_mode == "single":
                renderer.render_single(pairs[best_agent].grid, pairs[best_agent].score)
            
            # Move to next episode when all agents die
            if len(agents) == 0:
                break

            # Copy the agents list so we can remove agents while game is running
            for agent in agents:
                # Each agent takes an action according to their gene policy
                action = agent.take_action()
                agent.alive = pairs[agent].step(action)
                
                # Stop agent playing if dead
                if not agent.alive:
                    agents.remove(agent)

def play():
    env = SnakeEnv()
    renderer = Renderer()

    env.reset()
    while(renderer.render_play(env)):
        pass

if __name__ == "__main__":
    render_mode = input("Enter render mode (human, single, play, none): ")

    if render_mode not in ["human", "single", "play"]:
        print("Render mode set to none.")
        render_mode = None

    if render_mode == "play":
        play()
    else:
        try:
            num_agents = int(input("Enter number of agents: "))
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

        evaluate(num_agents, num_episodes, render_mode)
    

    
    