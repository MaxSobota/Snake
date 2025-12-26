import numpy as np

# Decides how offspring are created from parent weights
def genetic_operator(parent_a, parent_b):
    # Flatten weights for easier editing
    weights_a = parent_a.weights
    weights_b = parent_b.weights

    # Pick each weight from a parent with 50% chance
    mask = np.random.rand(len(weights_a)) < 0.5
    child_weights = np.where(mask, weights_a, weights_b)

    return child_weights

# Randomly alters an agent's weights
def mutate(child_weights):
    # Add some random noise 
    mutated_weights = child_weights.copy()
    mask = np.random.rand(len(mutated_weights)) < 0.1
    mutated_weights[mask] += np.random.normal(0, 0.05, size=np.sum(mask))
    
    return mutated_weights

# Softmax function for creating a probability distribution
def softmax(scores):
    # Subtract the maximum value to prevent overflow
    stabilized = np.exp(scores - np.max(scores))

    # Softmax equation
    return stabilized / np.sum(stabilized) 

# Creates offspring from the current agents
def reproduce(population, num_offspring):
    # Take parents using probability based on fitness (score)
    scores = np.array([agent.score for agent in population])

    # Get probability distribution from scores
    probabilities = softmax(scores)

    # List of child weights
    children = []

    # Create offspring
    for _ in range(num_offspring):
        # Drawn with replacement, this can result in cloning, but that might be beneficial
        parent_a = np.random.choice(population, p=probabilities)
        parent_b = np.random.choice(population, p=probabilities)
        
        # Create offspring based on parents
        child_weights = genetic_operator(parent_a, parent_b)
        
        # Mutate the child!!!
        mutated_weights = mutate(child_weights)

        children.append(mutated_weights)

    return children

# Kill off population according to worst performers
def cull(population, num_offspring):
    cull_amount = len(population) - num_offspring

    # Remove worst players
    population_sorted = sorted(population, key=lambda a: a.score, reverse=True)[:cull_amount]

    weights = []
    for agent in population_sorted:
        weights.append(agent.weights)
    # Return surviving population's weights
    return weights

# Takes in old population and produces new population
def repopulate(agents, num_offspring):
    # Copy so we can edit 
    population = agents.copy()

    # Make new offspring weights
    children = np.array(reproduce(population, num_offspring))

    # Cull worst of the old weights
    survived = np.stack(cull(population, num_offspring))

    # Stack survived weights and new offspring weights
    population = np.vstack((survived, children))

    return population