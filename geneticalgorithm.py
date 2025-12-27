import numpy as np

# Decides how offspring are created from parent weights
def genetic_operator(parent_a, parent_b):
    layers_a = parent_a.brain.layers
    layers_b = parent_b.brain.layers

    child_weights = []

    # For each layer, pick each weight from a parent with 50% chance
    for i in range(parent_a.brain.num_layers - 1): # 4 layers = 3 sets of weights
        mask = np.random.rand(*layers_a[i].shape) < 0.5

        # If in mask, take from one parent, if not, take from the other parent
        child_layer = np.where(mask, layers_a[i], layers_b[i]).copy()
        child_weights.append(child_layer)

    return child_weights

# Randomly alters an agent's weights
def mutate(child_weights):
    mutated_weights = []

    # 10% chance to mutate a weight in each layer
    for layer in child_weights:
        mutated_layer = layer.copy()

        # 10% chance for any weight to be mutated
        mask = np.random.rand(*layer.shape) < 0.1

        # Add some noise to the layer
        mutated_layer[mask] += np.random.normal(0, 0.15, size=np.sum(mask))
        mutated_weights.append(mutated_layer)
    
    return mutated_weights

# Softmax function for creating a probability distribution
def softmax(scores):
    # Subtract the maximum value to prevent overflow
    stabilized = np.exp(scores - np.max(scores))

    # Softmax equation
    return stabilized / np.sum(stabilized) 

# Fitness of agent is based on their score/steps
def fitness(agent):
    if agent.steps_without_food >= 90:
        total_fitness = -9999999
    else:
        total_fitness = (agent.score * 50000) + (agent.steps * 5) - (agent.steps_without_food * 20)

    return total_fitness

# Creates offspring from the current agents
def reproduce(population, num_offspring):
    # Take parents using probability based on fitness (score)
    scores = np.array([fitness(agent) for agent in population])

    # Get probability distribution from scores
    probabilities = softmax(scores)

    # List of child weights
    children = []

    # Create offspring
    for _ in range(num_offspring):
        # Drawn with replacement, this can result in cloning, but that might be beneficial
        parent_a = np.random.choice(population, p=probabilities)
        parent_b = np.random.choice(population, p=probabilities)

        # parent_a = population[np.argmax([a.score for a in population])]
        # parent_b = parent_a
        
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

    layers = []
    for agent in population_sorted:
        layers.append(agent.brain.layers)

    # Return surviving population's weights
    return layers

# Takes in old population and produces new population
def repopulate(agents, num_offspring):
    # Copy so we can edit 
    population = agents.copy()

    # Make new offspring weights (returns list of children weights = list of list of np arrays)
    children = reproduce(population, num_offspring)

    # Cull worst of the old weights (list of list of np arrays)
    survived = cull(population, num_offspring)

    # Concatenate survived weights and new offspring weights
    population = survived + children

    return population