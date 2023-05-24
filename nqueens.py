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
import numpy as np
from tabulate import tabulate




def get_fitness_regression(self):

    fitness = 5*self.deaths - 2.5*self.queens

    if self.deaths == self.queens:
        fitness *= self.n
    return fitness

def get_fitness_tuple(self):

     return (self.queens, self.deaths)


# monkey patching
Individual.get_fitness = get_fitness_regression


def run_experiment(n, iterations, pop_size, crossover_prob, mutation_prob, selection, mutation, crossover, gens, tournament_size = None):

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
                 elitism=True, tournament_size=tournament_size)
        
        best_indvs_fit = [i.fitness for i in pop.bestindvs]
        best_indvs_queens = [i.queens for i in pop.bestindvs]
        best_indvs_deaths = [i.deaths for i in pop.bestindvs]

        df_temp['run'] = [run+1]*gens
        df_temp['gens'] = range(1,gens+1)
        df_temp['crossover'] = crossover.__name__
        df_temp['xo_prob'] = crossover_prob
        df_temp['mutate'] = mutation.__name__
        df_temp['mut_prob'] = mutation_prob
        df_temp['select'] = selection.__name__
        df_temp['tournament_size'] = tournament_size
        df_temp['best_fitness'] = best_indvs_fit
        df_temp['queens']= best_indvs_queens
        df_temp['deaths'] = best_indvs_deaths

        #print(df)

        #print('df_temp',df_temp['run'])

        df = pd.concat([df, df_temp])

    #print(len(df['run']))

    return df


def tournmanent_experiment(sizes):

    df_final = []

    df_final_med = []

    for size in sizes:

        #print(size)

        data = run_experiment(n = 8, iterations = 30, pop_size = 50, crossover_prob=0.9, mutation_prob=0.2, mutation = binary_mutation, crossover=single_point_co, gens=30, tournament_size=size, selection=tournament_sel)

        df_final.append({'tournament_size': size, 'data': data})
    
        df_med = data.loc[:,['gens','queens', 'deaths', 'best_fitness']].groupby(by=["gens"]).agg({'queens': ['min', 'mean', 'max','std'],'deaths': ['min', 'mean', 'max','std'], 'best_fitness': ['min', 'mean', 'max','std']})
        df_med[('queens', 'lower_bound')] = df_med[('queens', 'mean')] - (df_med[('queens', 'std')])/2
        df_med[('queens', 'upper_bound')] = df_med[('queens', 'mean')] + (df_med[('queens', 'std')])/2
        df_med[('deaths', 'lower_bound')] = df_med[('deaths', 'mean')] - (df_med[('deaths', 'std')])/2
        df_med[('deaths', 'upper_bound')] = df_med[('deaths', 'mean')] + (df_med[('deaths', 'std')])/2
        df_med[('best_fitness', 'lower_bound')] = df_med[('best_fitness', 'mean')] - (df_med[('best_fitness', 'std')])/2
        df_med[('best_fitness', 'upper_bound')] = df_med[('best_fitness', 'mean')] + (df_med[('best_fitness', 'std')])/2


        df_final_med.append({'size':size, 'df': df_med})

    return df_final_med

hello = tournmanent_experiment([2,4,6,7,8,9,10])

print(hello)
fig, ax = plt.subplots(figsize=(9,5))
for i in range(len(hello)):

    # ax.errorbar(hello[i]['df'].index, hello[i]['df'][('best_fitness','mean')], hello[i]['df'][('best_fitness','std')],label = hello[i]['size'] )

    
    ax.plot(hello[i]['df'].index, hello[i]['df'][('best_fitness','mean')], label=hello[i]['size'])
    ax.plot(hello[i]['df'].index, hello[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
    ax.plot(hello[i]['df'].index, hello[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
    ax.legend(title='tournament size')
    ax.fill_between(hello[i]['df'].index, hello[i]['df'][('best_fitness','lower_bound')], hello[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
    ax.set_xlabel('gens')
    ax.set_ylabel('best fitness')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
plt.show()

    






#print(run_experiment(n = 8, iterations = 30, pop_size = 50, crossover_prob=0.9, mutation_prob=0.2, mutation = binary_mutation, crossover=single_point_co, gens=100, tournament_size=7, selection=tournament_sel))

# n = 8
# exp1 = run_experiment(n = n,iterations = 30, pop_size = 50, crossover_prob=0.9, mutation_prob=0.9, 
#                      selection=tournament_sel, mutation = binary_mutation, crossover=single_point_co, gens=100)

# print(tabulate(exp1, headers='keys', tablefmt='psql'))
# # # exp2 = run_experiment(n = n,iterations = 30, pop_size = 30, crossover_prob=0.9, mutation_prob=0.9, 
# # #                      selection=tournament_sel, mutation = binary_mutation, crossover=single_point_co

# #print(type(exp1))

# df_media = exp1.loc[:,['gens','queens', 'deaths', 'best_fitness']].groupby(by=["gens"]).mean()

# print(tabulate(df_media, headers='keys', tablefmt='psql'))

#df_media  = exp1.loc[['queens', 'deaths','best_fitness']].
# # sns.lineplot(exp1)
# # sns.lineplot(exp2)
# # plt.show()