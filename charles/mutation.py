from random import randint, sample


def binary_mutation(individual):
    """Binary mutation for a GA individual

    Args:
        individual (Individual): A GA individual from charles.py

    Raises:
        Exception: When individual is not binary encoded.py

    Returns:
        Individual: Mutated Individual
    """

    # get a random index of the individual
    mut_index = randint(0, len(individual) - 1)

    # mutate the bit 0->1 or 0->1
    if individual[mut_index] == 0:
        individual[mut_index] = 1
    elif individual[mut_index] == 1:
        individual[mut_index] = 0
    else:
        raise Exception(
            f"Trying to do binary mutation on {individual}. But it's not binary.")
    return individual


def swap_mutation(individual):
    # get two indexes
    mut_indexes = sample(range(0, len(individual)), 2)
    # swap the values corresponding to those indexes
    individual[mut_indexes[0]], individual[mut_indexes[1]] = individual[mut_indexes[1]], individual[mut_indexes[0]]
    return individual


def inversion_mutation(individual):
    # get two indexes and sort them
    mut_indexes = sample(range(0, len(individual)), 2)
    mut_indexes.sort()

    # invert the portion of individual in between those indexes
    individual[mut_indexes[0]:mut_indexes[1]] = individual[mut_indexes[0]:mut_indexes[1]][::-1]

    return individual