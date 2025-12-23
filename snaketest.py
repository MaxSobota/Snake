from snakeenv import SnakeEnv
from snakeagent import SnakeAgent

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
"""

def evaluate():
    try:
        num_agents = int(input("Enter number of agents: "))
    except Exception as e:
        print(f"Error, {e}")

    if num_agents <= 0:
        print("Number of agents should be >= 1.")
        exit(1)

    agents = []
    for i in range(num_agents):
        agents.append(SnakeAgent())

    env = SnakeEnv(render_mode="human") # TODO: Change inputting parameters to be easier

    # How many iterations to train
    num_episodes = 1000 
    env.reset()

    for i in range(num_episodes):
        for agent in agents:
            # Each agent takes an action according to their gene policy
            action = agent.take_action()
            env.step(action)

if __name__ == "__main__":
    evaluate()