from charles.charles import Population, Individual
from charles.search import hill_climb, sim_annealing
from copy import deepcopy
from charles.selection import fps, tournament_sel, double_tournament
from charles.mutation import binary_mutation
from charles.crossover import single_point_co
from random import random
from operator import attrgetter

import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from tabulate import tabulate

def get_deaths(self):
        nr_dead = 0

    # transform into matrix (porque não tou a ver como se faz com os bits todos seguidos na parte de ver as rainhas mortas):
        n = int(math.sqrt(len(self.representation)))
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

# def get_queens(self):
#     return self.representation.count(1)

def get_fitness_regression(self):

    fitness = 5*self.deaths - 2.5*self.queens

    if self.deaths == self.queens:
        fitness *= self.n
    return fitness

def get_fitness_tuple(self):

     return (self.queens, self.deaths)


# monkey patching
Individual.get_fitness = get_fitness_regression



# print(Individual([1,1,1,0,
#                    0,0,0,1,
#                    0,1,0,0,
#                    0,1,0,1]).deaths)


def run_experiment(n, iterations, pop_size, crossover_prob, mutation_prob, selection, mutation, crossover, gens):

    df = pd.DataFrame()

    for run in range(iterations):
        print(run)
        df_temp = None
        df_temp = pd.DataFrame()

        best_indvs_fit = []
        best_indvs_queens = []
        best_indvs_deaths = []

        pop = None
    
        pop = Population(size = pop_size, optim="min", sol_size=n*n, valid_set=[0, 1], replacement=True)

        pop.evolve(gens=gens, xo_prob=crossover_prob, mut_prob=mutation_prob, select=selection,
                 mutate=mutation, crossover=crossover,
                 elitism=True)
        
        best_indvs_fit = [i.fitness for i in pop.bestindvs]
        best_indvs_queens = [i.queens for i in pop.bestindvs]
        best_indvs_deaths = [i.deaths for i in pop.bestindvs]

        df_temp['run'] = [run+1]*gens
        df_temp['gens'] = range(1,gens+1)
        df_temp['xo_prob'] = crossover_prob
        df_temp['mut_prob'] = mutation_prob
        df_temp['select'] = selection.__name__
        df_temp['mutate'] = mutation.__name__
        df_temp['crossover'] = crossover.__name__
        df_temp['best_fitness'] = best_indvs_fit
        df_temp['queens']= best_indvs_queens
        df_temp['deaths'] = best_indvs_deaths

        #print(df)

        #print('df_temp',df_temp['run'])

        df = pd.concat([df, df_temp])

    #print(len(df['run']))

    media_fitness = np.mean(best_indvs_fit)

    return df

  #  print(df)

    
   # df_full_results = 


    print('Experiment Finalized')


n = 8
exp1 = run_experiment(n = n,iterations = 10, pop_size = 50, crossover_prob=0.9, mutation_prob=0.9, 
                     selection=double_tournament, mutation = binary_mutation, crossover=single_point_co, gens=100)

print(tabulate(exp1, headers='keys', tablefmt='psql'))
# # exp2 = run_experiment(n = n,iterations = 30, pop_size = 30, crossover_prob=0.9, mutation_prob=0.9, 
# #                      selection=tournament_sel, mutation = binary_mutation, crossover=single_point_co

#print(type(exp1))

df_media = exp1.loc[:,['gens','queens', 'deaths', 'best_fitness']].groupby(by=["gens"]).mean()

print(tabulate(df_media, headers='keys', tablefmt='psql'))

#df_media  = exp1.loc[['queens', 'deaths','best_fitness']].
# # sns.lineplot(exp1)
# # sns.lineplot(exp2)
# # plt.show()