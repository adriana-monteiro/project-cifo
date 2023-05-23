from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from charles.selection import fps, tournament_sel
from charles.mutation import binary_mutation
from charles.crossover import single_point_co
from random import random
from operator import attrgetter

import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# def get_fitness(self):
#     """A function to calculate the number of dead queens and the total number of queens in the solution
#     Returns:
#         tuple: (number of dead queens, total number of queens in the board)
#     """
#     nr_queens = 0
#     nr_dead = 0

#     # transform into matrix (porque não tou a ver como se faz com os bits todos seguidos na parte de ver as rainhas mortas):
#     n = int(math.sqrt(len(self.representation)))
#     rep = [[self.representation[i*n+j] for j in range(n)] for i in range(n)] # [0,0,1,0] --> [[0,0],[1,0]]
    
#     # print(rep)

#     for line in range(n):
#         for col in range(n):
                
#             dead = False # if our current queen has threats, dead will become true and count one in the end for the nr of dead queens count

#             if rep[line][col] == 1:

#                 nr_queens += 1

#                 # let's search for this point's diagonal
#                 diagonal_indexes = []
#                 for i in range(1, n):
                    
#                     if line >= i and col >= i:
#                         diagonal_indexes.append((line-i,col-i))

#                     if line >= i and col+i < n:
#                         diagonal_indexes.append((line-i,col+i)) 
                        
#                     if line+i < n and col+i < n:
#                         diagonal_indexes.append((line+i, col+i))

#                     if line+i < n and col >= i:
#                         diagonal_indexes.append((line+i, col-i))

#                 diagonal = [rep[i[0]][i[1]] for i in diagonal_indexes]

#                 # let's search the queens line for other queens
#                 if sum(rep[line]) > 1: #if the sum of the line is bigger than 1, it contains more than one queen
#                     dead = True
                
#                 # let's search the queens column for other queens
#                 elif sum([rep[l][col] for l in range(n)]) > 1: #this will see each line for the same column col and do the same logic as above
#                     dead = True   
                
#                 # the way it searches for the diagonal excludes the starting point itself so if the sum of the diagonal list is bigger than one 
#                 # that indicates theres at least one queen diagonally positioned from our position
#                 elif sum(diagonal) > 0:
#                     dead = True
                
#             if dead:
#                 nr_dead +=1

#     fitness = 5*nr_dead - 2.5*nr_queens

#     if nr_dead == nr_queens:
#         fitness *= n
#     return fitness


def get_fitness_regression(self):

    fitness = 5*self.deaths - 2.5*self.queens

    if self.deaths == self.queens:
        fitness *= n
    return fitness

def get_fitness_tuple(self):

    return (self.queens, self.deaths)





Individual.get_fitness = get_fitness

# print(Individual([1,0,1,0,
#                   0,0,0,0,
#                   0,0,0,0,
#                   1,1,0,0]).fitness)


def run_experiment(n, iterations, pop_size, crossover_prob, mutation_prob, selection, mutation, crossover):

    best_indvs_fit = []
    for _ in range(iterations):

        pop = None

        pop = Population(size = pop_size, optim="min", sol_size=n*n, valid_set=[0, 1], replacement=True)

        pop.evolve(gens=100, xo_prob=crossover_prob, mut_prob=mutation_prob, select=selection,
                mutate=mutation, crossover=crossover,
                elitism=True)
        
        #print(pop.bestindvs[-1])
        best_indvs_fit = [i.fitness for i in pop.bestindvs]

        print(best_indvs_fit)

      #  print('individuals', pop.individuals)

        # best_indiv_fitness.append((pop.evolve(gens=200, xo_prob=crossover_prob, mut_prob=mutation_prob, select=selection,
        #         mutate=mutation, crossover=crossover,
        #         elitism=True)).fitness)
        
        print("Iteration done")

        #avg_fitness_df = pd.Dataframe()

    print('Experiment Finalized')

    #return best_indiv_fitness
    #### como é que vamos buscar o fitness e a solução para guardar? 


n = 10
exp1 = run_experiment(n = n,iterations = 30, pop_size = 30, crossover_prob=0.9, mutation_prob=0.9, 
                     selection=tournament_sel, mutation = binary_mutation, crossover=single_point_co)

# exp2 = run_experiment(n = n,iterations = 30, pop_size = 30, crossover_prob=0.9, mutation_prob=0.9, 
#                      selection=tournament_sel, mutation = binary_mutation, crossover=single_point_co

# sns.lineplot(exp1)
# sns.lineplot(exp2)
# plt.show()