from random import randint, sample, uniform, shuffle
import math


def single_point_co(p1, p2):
    """Implementation of single point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    co_point = randint(1, len(p1)-2)

    offspring1 = p1[:co_point] + p2[co_point:]
    offspring2 = p2[:co_point] + p1[co_point:]

    return offspring1, offspring2


def cycle_crossover(p1, p2):

    #Initializing empty lists for the offpsrings placeholders and their indexes
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p2)
    offspring1_indexes = [None] * len(p1)
    offspring2_indexes = [None] * len(p2)
    
    #Getting the indexes out of the parents and shuffling them for a random initiation
    p1_indexes = list(range(len(p1)))
    p2_indexes = list(range(len(p2)))
    shuffle(p1_indexes)
    shuffle(p2_indexes)

    start_index = p1_indexes[0]
    
    while None in offspring1:
        index = start_index
        val1 = p1_indexes[index]
        val2 = p2_indexes[index]

    #Initial loop of the cycle, that repeats until it gets to a repeated index already in the offspring
        while val1 != val2:
            #We save the indexes of the values added, to later reorder
            offspring1_indexes[index] = p1_indexes[index]
            #Adding the value from the parent to the offspring
            offspring1[index] = p1[p1_indexes[index]]
            offspring2_indexes[index] = p2_indexes[index]
            offspring2[index] = p2[p2_indexes[index]]
            val2 = p2_indexes[index]
            index = p1_indexes.index(val2)
    #After the first loop stops, we add the values of the second parent to the empty spots in the offspring
    #We save the indexes and add right the way the corresponding values to the offspring from the second parent
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1_indexes[index] = p2_indexes[index]
                    offspring1[index] = p2[p2_indexes[index]]
                    offspring2_indexes[index] = p1_indexes[index]
                    offspring2[index] = p1[p1_indexes[index]]
    
    #Reordering of the offsprings with the before saved indexes
    sorted_offspring1 = [offspring1 for _, offspring1 in sorted(zip(offspring1_indexes,offspring1))]
    sorted_offspring2 = [offspring2 for _, offspring2 in sorted(zip(offspring2_indexes,offspring2))]

    return sorted_offspring1,sorted_offspring2



def k_point_co(p1,p2):
    """Implementation of k-point crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """

    # Choose de number of crossover points
    # We choose k=3 because k=1 is single point crossover, k=2 is two point crossover
    # and more than 3 the offsprings lose the similarity with the parents
    k = 3

    #Initializing empty lists for the offpsrings 
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    # Generate k random crossover points
    xo_points = sample(range(1,len(p1)), k)
    xo_points.sort()

    # The Offspring will have the same values as their parent until the first crossover point
    for i in range(xo_points[0]):
        offspring1[i]=p1[i]
        offspring2[i]=p2[i]

    # Switch allows to alternate between parents
    switch=0

    #Initial loop of the cycle, that loops to every crossover window
    for j in range(1,k):
        if switch==0:
            # Looping to the crossover window and assigning the values of the other parent
            for i in range(xo_points[j-1],xo_points[j]):
                offspring1[i]=p2[i]
                offspring2[i]=p1[i]
            switch=1
            # Switch to alternate parent in the next crossover point
        else:
            for i in range(xo_points[j-1],xo_points[j]):
                offspring1[i]=p1[i]
                offspring2[i]=p2[i]
            switch=0

    #Looping to the remaining empty spots in the offspring and assigning them
    if switch==0:
        for i in range(xo_points[-1],len(p1)):
            offspring1[i]=p2[i]
            offspring2[i]=p1[i]
    else:
        for i in range(xo_points[-1],len(p1)):
            offspring1[i]=p1[i]
            offspring2[i]=p2[i]

    return offspring1, offspring2
