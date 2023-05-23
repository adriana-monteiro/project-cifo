from random import shuffle, choice, sample, random
from operator import attrgetter
from copy import deepcopy
import math


class Individual:
    def __init__(
        self,
        representation=None,
        size=None,
        replacement=True,
        valid_set=None,
    ):
        if representation == None:
            if replacement == True:
                self.representation = [choice(valid_set) for i in range(size)]
            elif replacement == False:
                self.representation = sample(valid_set, size)
        else:
            self.representation = representation
        

        self.n = int(math.sqrt(len(self.representation)))

        self.queens = representation.count(1)

        self.deaths = self.get_deaths()

        self.fitness = self.get_fitness()
    def get_deaths(self):
        nr_dead = 0

    # transform into matrix (porque não tou a ver como se faz com os bits todos seguidos na parte de ver as rainhas mortas):
        n = self.n
        rep = [[self.representation[i*n+j] for j in range(n)] for i in range(n)] # [0,0,1,0] --> [[0,0],[1,0]]
    
    # print(rep)

        for line in range(n):
            for col in range(n):
                    
                dead = False # if our current queen has threats, dead will become true and count one in the end for the nr of dead queens count

                if rep[line][col] == 1:

                    # let's search for this point's diagonal
                    diagonal_indexes = []
                    for i in range(1, n):
                        
                        if line >= i and col >= i:
                            diagonal_indexes.append((line-i,col-i))

                        if line >= i and col+i < n:
                            diagonal_indexes.append((line-i,col+i)) 
                            
                        if line+i < n and col+i < n:
                            diagonal_indexes.append((line+i, col+i))

                        if line+i < n and col >= i:
                            diagonal_indexes.append((line+i, col-i))

                    diagonal = [rep[i[0]][i[1]] for i in diagonal_indexes]

                    # let's search the queens line for other queens
                    if sum(rep[line]) > 1: #if the sum of the line is bigger than 1, it contains more than one queen
                        dead = True
                    
                    # let's search the queens column for other queens
                    elif sum([rep[l][col] for l in range(n)]) > 1: #this will see each line for the same column col and do the same logic as above
                        dead = True   
                    
                    # the way it searches for the diagonal excludes the starting point itself so if the sum of the diagonal list is bigger than one 
                    # that indicates theres at least one queen diagonally positioned from our position
                    elif sum(diagonal) > 0:
                        dead = True
                    
                if dead:
                    nr_dead +=1
        
        return nr_dead

    def get_fitness(self):
        raise Exception("You need to monkey patch the fitness path.")

    # def get_neighbours(self, func, **kwargs):
    #     raise Exception("You need to monkey patch the neighbourhood function.")

    # def queens(self):
    #     raise Exception("You need to monkey patch the dead_queens path.")
    

    def index(self, value):
        return self.representation.index(value)

    def __len__(self):
        return len(self.representation)

    def __getitem__(self, position):
        return self.representation[position]

    def __setitem__(self, position, value):
        self.representation[position] = value

    def __repr__(self):
        n = int(math.sqrt(len(self.representation)))

        s='\n'
        for i in range(n):
            s+=str([self.representation[i*n+j] for j in range(n)])+'\n'

        return f"Individual(size={len(self.representation)}); Fitness: {self.fitness};\nRep: {s} "



class Population:
    def __init__(self, size, optim, **kwargs):
        self.individuals = []
        self.size = size
        self.optim = optim
        self.bestindvs = []

        for _ in range(size):
            self.individuals.append(
                Individual(
                    size=kwargs["sol_size"],
                    replacement=kwargs["replacement"],
                    valid_set=kwargs["valid_set"],
                )
            )

    def evolve(self, gens, xo_prob, mut_prob, select, mutate, crossover, elitism):
        best_ind = []
        for i in range(gens):
            new_pop = []

            if elitism:
                if self.optim == "max":
                    elite = deepcopy(max(self.individuals, key=attrgetter("fitness")))
                elif self.optim == "min":
                    elite = deepcopy(min(self.individuals, key=attrgetter("fitness")))

            while len(new_pop) < self.size:
                parent1, parent2 = select(self), select(self)

                if random() < xo_prob:
                    offspring1, offspring2 = crossover(parent1, parent2)
                else:
                    offspring1, offspring2 = parent1, parent2

                if random() < mut_prob:
                    offspring1 = mutate(offspring1)
                if random() < mut_prob:
                    offspring2 = mutate(offspring2)

                new_pop.append(Individual(representation=offspring1))
                if len(new_pop) < self.size:
                    new_pop.append(Individual(representation=offspring2))

            if elitism:
                if self.optim == "max":
                    worst = min(new_pop, key=attrgetter("fitness"))
                    if elite.fitness > worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

                elif self.optim == "min":
                    worst = max(new_pop, key=attrgetter("fitness"))
                    if elite.fitness < worst.fitness:
                        new_pop.pop(new_pop.index(worst))
                        new_pop.append(elite)

            self.individuals = new_pop

            if self.optim == "max":
                print(f'Best Individual: {max(self, key=attrgetter("fitness"))}')
            elif self.optim == "min":
                best_ind.append(deepcopy(min(self.individuals, key=attrgetter("fitness"))))
        
        self.bestindvs = best_ind
               # print(f'Best Individual: {min(self, key=attrgetter("fitness"))}') 

    def __len__(self):
        return len(self.individuals)

    def __getitem__(self, position):
        return self.individuals[position]
