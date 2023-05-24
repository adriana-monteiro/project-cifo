from random import uniform, choice, sample, Random
from operator import attrgetter
from charles import Individual


def fps(population):
    """Fitness proportionate selection implementation.

    Args:
        population (Population): The population we want to select from.

    Returns:
        Individual: selected individual.
    """

    if population.optim == "max":

        # Sum total fitness
        total_fitness = sum([i.fitness for i in population])
        # Get a 'position' on the wheel
        spin = uniform(0, total_fitness)
        position = 0
        # Find individual in the position of the spin
        for individual in population:
            position += individual.fitness
            if position > spin:
                return individual

    elif population.optim == "min":
        raise NotImplementedError

    else:
        raise Exception("No optimization specified (min or max).")


def tournament_sel(population, size=4):
    """Tournament selection implementation.

    Args:
        population (Population): The population we want to select from.
        size (int): Size of the tournament.

    Returns:
        Individual: The best individual in the tournament.
    """

    # Select individuals based on tournament size
    # with choice, there is a possibility of repetition in the choices,
    # so every individual has a chance of getting selected
    tournament = [choice(population.individuals) for _ in range(size)]

    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))

def double_tournament(population, tournament_size=10, fitness_tournament_size=10, parsimony_tournament_size=4, switch=False):
    rng = Random()

    if switch and parsimony_tournament_size >= fitness_tournament_size:
        queens_winners = []

        for i in range(parsimony_tournament_size):
            queens_candidates = [rng.randint(0, len(population) - 1) for i in range(tournament_size)]
            queens_winners.append(max([population[i] for i in queens_candidates], key=lambda x: x.get_queens()))

        death_candidates = [rng.randint(0, len(queens_winners) - 1) for i in range(fitness_tournament_size)]
        winner = min([population[i] for i in death_candidates], key=lambda x: x.get_deaths())

        return winner

    elif not switch and fitness_tournament_size >= parsimony_tournament_size:
        death_winners = []

        for i in range(fitness_tournament_size):
            death_candidates = [rng.randint(0, len(population) - 1) for i in range(tournament_size)]
            death_winners.append(min([population[i] for i in death_candidates], key=lambda x: x.get_deaths()))

        queens_candidates = [rng.randint(0, len(death_winners) - 1) for i in range(parsimony_tournament_size)]
        winner = max([population[i] for i in queens_candidates], key=lambda x: x.get_queens())
        return winner

    else:
        if switch and parsimony_tournament_size < fitness_tournament_size:
            raise ValueError("Switch is true so Sf can't be bigger than Sp")
        else:
            raise ValueError("Sp can't be bigger than Sf")

