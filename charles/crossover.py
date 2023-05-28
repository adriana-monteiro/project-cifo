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


# def pmx(p1, p2):

#     # get random sample without replacement of indexes
#     p1_indexes = sample(range(len(p1)), len(p1))
#     p2_indexes = sample(range(len(p2)), len(p2))

#     xo_points = sample(range(len(p1_indexes)+1), 2)
#     xo_points.sort()

#     window_p1 = {}
#     window_p2 = {}

#     for i in range(xo_points[0], xo_points[1]):
#        if p2_indexes[i] not in window_p1:
#             window_p1[p1_indexes[i]] = p2_indexes[i]
#        if p1_indexes[i] not in window_p2:
#             window_p2[p2_indexes[i]] = p1_indexes[i]

#     def get_off(indexes, parent):

#         ofspr = []
#         ofspr_index = []

#         for index,value in zip(indexes, parent):

#             print(index,value)

#             if index not in window_p1 and index not in window_p2 and index not in ofspr_index:
#                 ofspr_index.append(index)
#                 ofspr.append(value)

#             elif index in window_p1 and window_p1[index] not in ofspr_index:
#                 ofspr_index.append(window_p1[index])
#                 ofspr.append(p2[p2_indexes.index(window_p1[index])])

#             elif index in window_p2 and window_p2[index] not in ofspr_index:
#                 ofspr_index.append(window_p2[index])
#                 ofspr.append(p1[p1_indexes.index(window_p2[index])])
        
#         return ofspr

#     off1, off2 = get_off(p1_indexes,p1),get_off(p2_indexes, p2)

#     return off1,off2



def k_point_co(p1,p2):
    # we chose k = 3 
    k = 3

    # create offsprings
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    # generate k crossover points
    xo_points = sample(range(1,len(p1)), k)
    xo_points.sort()

    # crossover
    for i in range(xo_points[0]):
        offspring1[i]=p1[i]
        offspring2[i]=p2[i]
    switch=0
    for j in range(1,k):
        if switch==0:
            for i in range(xo_points[j-1],xo_points[j]):
                offspring1[i]=p2[i]
                offspring2[i]=p1[i]
            switch=1
        else:
            for i in range(xo_points[j-1],xo_points[j]):
                offspring1[i]=p1[i]
                offspring2[i]=p2[i]
            switch=0

    if switch==0:
        for i in range(xo_points[-1],len(p1)):
            offspring1[i]=p2[i]
            offspring2[i]=p1[i]
    else:
        for i in range(xo_points[-1],len(p1)):
            offspring1[i]=p1[i]
            offspring2[i]=p2[i]

    return offspring1, offspring2