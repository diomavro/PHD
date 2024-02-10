import random
import numpy as np
from typing import Dict, Any, List, Tuple

# Genetic Algorithm parameters
POPULATION_SIZE: int = 100
GENERATIONS: int = 100
MUTATION_RATE: float = 0.01

class Portfolio:
    def __init__(self, yields: np.ndarray, prices: np.ndarray, strikes: np.ndarray):
        self.yields = yields
        self.prices = prices
        self.strikes = strikes
        self.weights = None

    def value_at_risk(self, returns: np.ndarray, alpha: float) -> float:
        """Calculates the value at risk (VaR) of a portfolio of returns at a given significance level.

        Args:
            returns: A numpy array of portfolio returns.
            alpha: The significance level (e.g. 0.05 for 5%).

        Returns:
            The value at risk of the portfolio.
        """
        option_values = np.maximum(self.strikes - returns, 0)
        portfolio_value_at_risk = np.percentile(option_values.dot(self.weights), 100 * alpha)
        return portfolio_value_at_risk

    def calculate_portfolio(self, weights: np.ndarray) -> float:
        """Calculates the value of a portfolio of options.

        Args:
            weights: A numpy array of weights for each option (i.e. how many of each option to buy).

        Returns:
            The value of the portfolio.
        """
        portfolio_value = (weights * self.prices).sum()
        self.weights = weights
        return portfolio_value

def fitness_function(
    individual: dict,
    yields: np.ndarray,
    prices: np.ndarray,
    strikes: np.ndarray,
    returns: np.ndarray,
    alpha: float = 0.05,
    min_var: float = 0.0,
) -> float:
    """
    Calculates the fitness value of an individual in a portfolio optimization problem.

    Args:
        individual (dict): A dictionary object containing the weights of the portfolio.
        yields (np.ndarray): An array of yield values for each asset in the portfolio.
        prices (np.ndarray): An array of current prices for each asset in the portfolio.
        strikes (np.ndarray): An array of strike prices for each option in the portfolio.
        returns (np.ndarray): An array of expected returns for each option in the portfolio.
        alpha (float, optional): The significance level used to calculate the portfolio value at risk.
            Defaults to 0.05.
        min_var (float, optional): The minimum value at risk required for an individual to be considered feasible.
            Defaults to 0.0.

    Returns:
        float: The fitness value of the individual in the portfolio optimization problem.
    """
    # Get the portfolio weights from the individual
    weights = individual['weights']

    # Calculate the portfolio value
    portfolio_value = (weights * prices).sum()

    # Reshape strikes to match the shape of returns
    strikes = strikes.reshape(-1, 1)

    # Calculate the option values
    option_values = np.maximum(strikes - returns, 0)

    # Calculate the portfolio value at risk
    var = np.percentile(option_values.dot(weights), 100 * alpha)

    # Check if the individual meets the minimum VAR requirement
    if var < min_var:
        return 0.0

    # Calculate the portfolio income
    income = yields.dot(weights) * portfolio_value

    # Calculate the penalty term
    penalty = max(0, min_var - var)

    # Calculate the fitness
    fitness = income + portfolio_value - penalty

    return fitness
    


def generate_population(strikes: np.ndarray, population_size: int) -> List[dict]:
    """Generates an initial population of individuals.
    
    Args:
        strikes: A numpy array of strike prices for each option.
        population_size: The number of individuals in the population.
    
    Returns:
        A list of dictionaries representing the initial population. Each dictionary has keys
        corresponding to the strike prices and values corresponding to the weights.
    """
    population = []
    for i in range(pop_size):
        individual = create_individual(num_assets)
        population.append(individual)
    return population


def evaluate_population(population: List[dict], yields: np.ndarray, prices: np.ndarray, strikes: np.ndarray, returns: np.ndarray, alpha: float) -> None:
    """Evaluates the fitness of each individual in the population.
    
    Modifies the given population list in place by adding a 'fitness' key to each individual dictionary.
    
    Args:
        population: A list of dictionaries representing the population.
        yields: A numpy array of yields for each option.
        prices: A numpy array of prices for each option.
        strikes: A numpy array of strike prices for each option.
        returns: A numpy array of portfolio returns.
        alpha: The significance level (e.g. 0.05 for 5%).
    """
    for individual in population:
        individual['fitness'] = fitness_function(individual, yields, prices, strikes, returns, alpha)


def selection(population: List[dict], num_parents: int) -> List[dict]:
    """Selects the specified number of parents from the population using tournament selection.
    
    Args:
        population: A list of dictionaries representing the population.
        num_parents: The number of parents to select.
        
    Returns:
        A list of dictionaries representing the selected parents.
    """
    parents = []
    for i in range(num_parents):
        tournament = random.sample(population, TOURNAMENT_SIZE)
        winner = max(tournament, key=lambda x: x['fitness'])
        parents.append(winner)
    return parents


def crossover(parent1: dict, parent2: dict) -> Tuple[dict, dict]:
    """Performs crossover between two parents to produce two offspring.
    
    Args:
        parent1: A dictionary representing the first parent.
        parent2: A dictionary representing the second parent.
    
    Returns:
        A tuple of dictionaries representing the two offspring.
    """
    offspring1, offspring2 = {}, {}
    for key in parent1.keys():
        if random.random() < 0.5:
            offspring1[key] = parent1[key]
            offspring2[key] = parent2[key]
        else:
            offspring1[key] = parent2[key]
            offspring2[key] = parent1[key]
    return offspring1, offspring2



def mutate(individual: dict, mutation_rate: float) -> None:
    """Applies mutation to an individual by randomly changing the weight of some options.
    
    Modifies the given individual dictionary in place.
    
    Args:
        individual: A dictionary representing the individual portfolio.
        mutation_rate: The probability of each weight being mutated.
    """
    for key in individual.keys():
        if random.random() < mutation_rate:
            individual[key] = random.uniform(0, 1)

from typing import List

def repeat_first_elements(original_list: List, num_elements_to_repeat: int) -> List:
    """
    Returns a modified version of the input list where the first 'num_elements_to_repeat'
    elements are repeated consecutively, followed by the remaining elements without 
    the last 'num_elements_to_repeat' elements.

    Args:
        original_list: A list of elements.
        num_elements_to_repeat: An integer specifying the number of elements to repeat.

    Returns:
        A list containing the modified version of the input list.
    """

    if num_elements_to_repeat <= 0:
        return original_list[:]

    else:
        repeated_elements = [original_list[0]] * min(len(original_list), num_elements_to_repeat)
        remaining_elements_start_index = max(0, len(original_list) - num_elements_to_repeat)
        remaining_elements = original_list[remaining_elements_start_index:]
        return repeated_elements + remaining_elements
def genetic_algorithm(yields: np.ndarray, prices: np.ndarray, strikes: np.ndarray, returns: np.ndarray, alpha: float) -> dict:
    """Optimizes a portfolio of options using a genetic algorithm.
    
    Args:
        yields: A numpy array of yields for each option.
        prices: A numpy array of prices for each option.
        strikes: A numpy array of strike prices for each option.
        returns: A numpy array of portfolio returns.
        alpha: The significance level (e.g. 0.05 for 5%).
    
    Returns:
        A dictionary representing the optimal portfolio. The keys are the strike prices and
        the values are the weights (i.e. how many options to buy).
    """
    # Initialize population
    population = generate_population(strikes, POPULATION_SIZE)

    # Evaluate initial population
    for individual in population:
        individual['fitness'] = fitness_function(individual, yields, prices, strikes, returns, alpha)

    # Evolution loop
    for generation in range(GENERATIONS):
        # Select parents for mating
        parents = random.choices(population, weights=[individual['fitness'] for individual in population], k=len(population))

        # Generate offspring through crossover
        offspring = []
        for i in range(0, len(parents), 2):
            parent1, parent2 = parents[i], parents[i+1]
            offspring1, offspring2 = crossover(parent1, parent2)
            offspring.append(offspring1)
            offspring.append(offspring2)

        # Mutate offspring
        for individual in offspring:
            mutate(individual, MUTATION_RATE)

        # Evaluate offspring
        for individual in offspring:
            individual['fitness'] = fitness_function(individual, yields, prices, strikes, returns, alpha)

        # Select survivors for next generation
        population = sorted(population + offspring, key=lambda x: x['fitness'], reverse=True)[:POPULATION_SIZE]

    # Return best individual
    return max(population, key=lambda x: x['fitness'])
