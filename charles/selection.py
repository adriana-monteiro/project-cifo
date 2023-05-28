from random import uniform, choice, sample, Random
from operator import attrgetter
from .charles import Individual



# tournament selection
def tournament_sel(population, tournament_size=9):
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
    tournament = [choice(population.individuals) for _ in range(tournament_size)]

    # with sample, there is no repetition of choices
    # tournament = sample(population.individuals, size)
    if population.optim == "max":
        return max(tournament, key=attrgetter("fitness"))
    if population.optim == "min":
        return min(tournament, key=attrgetter("fitness"))
    


# double tournament
def double_tournament(population, tournament_size=10, deaths_tournament_size=6, queens_tournament_size=2, switch=False):
    rng = Random()

    # switch means perform nr queens -> nr deaths
    if switch and deaths_tournament_size <= queens_tournament_size:
        queens_winners = []

        # perform queens_tournament_size tournaments with tournament_size with the nr of queens as a criteria
        for i in range(queens_tournament_size):
            queens_candidates = [rng.randint(0, len(population) - 1) for i in range(tournament_size)]
            queens_winners.append(max([population[i] for i in queens_candidates], key=lambda x: x.get_queens())) #criteria: queens

        # perform a final tournament with deaths_tournament_size size  with the nr of deahths as a criteria
        death_candidates = [rng.randint(0, len(queens_winners) - 1) for i in range(queens_tournament_size)]
        winner = min([queens_winners[i] for i in death_candidates], key=lambda x: x.get_deaths()) #criteria: deaths

        return winner

    # not switch means perform nr deaths -> nr queens
    elif not switch and queens_tournament_size <= deaths_tournament_size:
        death_winners = []

        # perform deaths_tournament_size tournaments with tournament_size with the nr of deaths as a criteria
        for i in range(deaths_tournament_size):
            death_candidates = [rng.randint(0, len(population) - 1) for i in range(tournament_size)]
            death_winners.append(min([population[i] for i in death_candidates], key=lambda x: x.get_deaths())) #criteria: deaths

        # perform a final tournament with queens_tournament_size size with the nr of queens as a criteria
        queens_candidates = [rng.randint(0, len(death_winners) - 1) for i in range(deaths_tournament_size)]
        winner = max([death_winners[i] for i in queens_candidates], key=lambda x: x.get_queens()) # criteria:queens
        return winner

    # double tournament is not eligble if the size of the second (final) tournament is bigger than the number of tournaments of the inital phase
    else:
        if switch and deaths_tournament_size > queens_tournament_size:
            raise ValueError("Switch is True so deaths size can't be bigger queens than deaths size")
        else:
            raise ValueError("Switch is False so queens size can't be bigger than deaths size")



def ranking(population):

    if population.optim == "max":

        # Sum acumulated rank nrs
        total_rank_sum = sum([rank for rank in range(1, population.size+1)]) 
      
        # make a sorted list of fitness - because it is maximization it is not inverted so the best is the last as it should
        fitness_rank = sorted([individual for individual in population], key = lambda ind : ind.fitness, reverse = False) 

        # Get a 'position' on the wheel
        spin = uniform(0, total_rank_sum)
        position = 0

        # Find individual in the position of the spin
        for individual in population:
            position += fitness_rank.index(individual)+1 # sum the individual's rank, given by the fitness rank list
            if position > spin:
                return individual


    elif population.optim == "min":

        # Sum acumulated rank nrs
        total_rank_sum = sum([rank for rank in range(1, population.size+1)])

        # make a sorted list of fitness - because it is minimization it is inverted so the best is the last
        fitness_rank = sorted([individual for individual in population], key = lambda ind : ind.fitness, reverse = True)

        # Get a 'position' on the wheel
        spin = uniform(0, total_rank_sum)
        position = 0

        # Find individual in the position of the spin
        for individual in population:
            position += fitness_rank.index(individual)+1 #  sum the individual's rank, given by the fitness rank list
            if position > spin:
                return individual

    else:
        raise Exception("No optimization specified (min or max).")

