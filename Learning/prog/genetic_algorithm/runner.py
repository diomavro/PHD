import numpy as np
from typing import Dict, Any, List
from functions import Portfolio

# Define the fitness function
def portfolio_fitness(portfolio, yields, prices, strikes, returns, alpha, min_var):
    # Calculate the portfolio value
    portfolio_value = sum(portfolio * prices)
    # Calculate the option values
    option_values = np.maximum(strikes - returns, 0)
    # Calculate the portfolio value at risk
    VaR = np.percentile(option_values @ portfolio, 100 * alpha)
    # Calculate the portfolio income
    income = yields @ portfolio * portfolio_value
    # Calculate the fitness
    fitness = income - VaR - min_var * np.sum(np.abs(portfolio))
    return fitness

# Define the genetic algorithm parameters
POPULATION_SIZE = 100
NUM_PARENTS = 20
NUM_OFFSPRING = 80
NUM_GENERATIONS = 100
MUTATION_RATE = 0.1
TOURNAMENT_SIZE = 5
ELITE_SIZE = 5
ALPHA = 0.05
MIN_VAR = 0.1

# Generate some example data
np.random.seed(123)
NUM_ASSETS = 10
yields = np.random.uniform(0.01, 0.1, size=NUM_ASSETS)
prices = np.random.uniform(5, 20, size=NUM_ASSETS)
strikes = np.linspace(10, 20, num=NUM_ASSETS)
returns = np.random.normal(15, 5, size=10000)

# Define the initial population
population = []
for i in range(POPULATION_SIZE):
    weights = np.random.uniform(size=NUM_ASSETS)
    portfolio = {'weights': weights}
    population.append(portfolio)

# Run the genetic algorithm
for generation in range(NUM_GENERATIONS):
    # Evaluate the fitness of the population
    for individual in population:
        individual['fitness'] = portfolio_fitness(individual['weights'], yields, prices, strikes, returns, alpha=ALPHA, min_var=MIN_VAR)

    # Sort the population by fitness
    population.sort(key=lambda x: x['fitness'], reverse=True)

    # Select the elite individuals
    elite = population[:ELITE_SIZE]

    # Select the parents for crossover
    parents = selection(population, NUM_PARENTS)

    # Generate offspring through crossover and mutation
    offspring = []
    for i in range(0, NUM_PARENTS, 2):
        parent1 = parents[i]
        parent2 = parents[i+1]
        offspring1, offspring2 = crossover(parent1['weights'], parent2['weights'])
        mutate(offspring1, MUTATION_RATE)
        mutate(offspring2, MUTATION_RATE)
        offspring.append({'weights': offspring1})
        offspring.append({'weights': offspring2})

    # Replace the old population with the combined elite and offspring
    population = elite + offspring

# Print the best portfolio
best_portfolio = population[0]['weights']
print('Best portfolio:', best_portfolio)
portfolio_value = (best_portfolio * prices).sum()
option_values = np.maximum(strikes - returns, 0)
value_at_risk = np.percentile(option_values.dot(best_portfolio), 100 * ALPHA)
income = yields.dot(best_portfolio) * portfolio_value
print('Portfolio value:', portfolio_value)
print('Portfolio income:', income)
print('Value at risk:', value_at_risk)
print('Fitness:', portfolio_fitness(best_portfolio, yields, prices, strikes, returns, alpha=ALPHA, min_var=MIN_VAR))