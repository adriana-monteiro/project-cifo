from random import randint, sample, uniform,seed

#se = 69
#seed(se)

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


def cycle_xo(p1, p2):
    """Implementation of cycle crossover.

    Args:
        p1 (Individual): First parent for crossover.
        p2 (Individual): Second parent for crossover.

    Returns:
        Individuals: Two offspring, resulting from the crossover.
    """
    # offspring placeholders
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)

    while None in offspring1:
        index = offspring1.index(None)
        val1 = p1[index]
        val2 = p2[index]

        # copy the cycle elements
        while val1 != val2:
            offspring1[index] = p1[index]
            offspring2[index] = p2[index]
            val2 = p2[index]
            index = p1.index(val2)

        # copy the rest
        for element in offspring1:
            if element is None:
                index = offspring1.index(None)
                if offspring1[index] is None:
                    offspring1[index] = p2[index]
                    offspring2[index] = p1[index]

    return offspring1, offspring2

def pmx_co(p1,p2):
    xo_points =  sample(range(len(p1)), 2)
    xo_points.sort() 

    def pmx_offspring(x,y):
        o = [None] * len(x)

        # offspring 2
        o[xo_points[0]:xo_points[1]] = x[xo_points[0]:xo_points[1]]
        z = set(y[xo_points[0]:xo_points[1]]) - set(x[xo_points[0]:xo_points[1]])
        for i in z:
            temp = i
            index = y.index(x[y.index(temp)])

            while o[index] is not None:
                temp = index
                index = y.index(x[temp])

            o[index] = i

        #nrs that do not exist in the segment
        while None in o:
            index = o.index(None)
            o[index] = y[index]

        return o


    o1,o2 = pmx_offspring(p1,p2), pmx_offspring(p2,p1)

    return o1,o2

def arithmetic_xo(p1,p2): #cant use it if we want only integers in the solutions

    alpha = uniform(0,1)
    o1 = [None] * len(p1)
    o2 = [None] * len(p2)

    for i in range(len(p1)):
        o1[i] = p1[i]*alpha + (1-alpha) * p2[i]
        o2[i] = p2[i]*alpha + (1-alpha) * p1[i]

    return o1,o2


def k_point_co(p1,p2,k):
    offspring1 = [None] * len(p1)
    offspring2 = [None] * len(p1)
    xo_points = sample(range(1,len(p1)), k)
    xo_points.sort()

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

if __name__ == '__main__':
    p1, p2 = [9,8,4,5,6,7,1,3,2,10], [8,7,1,2,3,10,9,5,4,6]
    p1,p2 = [1,2,3,4,5,6,7,8,9,10], [10,9,8,7,6,5,4,3,2,1]
    p1,p2 = [1,0,0,0,1,1,0,1,1,0,1], [1,1,1,1,0,0,0,0,1,0,0]
    o1, o2 = arithmetic_xo(p1, p2)
    o1, o2 = k_point_co(p1, p2,4)
    print(o1, o2)
    o1, o2 = k_point_co(p1, p2,1)
    print(o1, o2)
    o1, o2 = single_point_co(p1, p2)
    print(o1, o2)
    o1, o2 = pmx_co(p1, p2)
    print(o1, o2)