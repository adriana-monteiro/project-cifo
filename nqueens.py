from charles.charles import Population, Individual
from copy import deepcopy
from charles.selection import tournament_sel, double_tournament, ranking
from charles.mutation import binary_mutation, swap_mutation, inversion_mutation
from charles.crossover import single_point_co, k_point_co, cycle_crossover
from random import random
from operator import attrgetter
from testfunctions import run_experiment, tournmanent_experiment, double_tournament_experiment, grid_search, elitism_test

import math
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from tabulate import tabulate
import matplotlib.patches as mpatches


def get_fitness_regression(self):

    fitness = 5*self.deaths - 2.5*self.queens

    if self.deaths == self.queens:
        fitness *= self.n
    return fitness

def get_fitness_tuple(self):

     return (self.queens, self.deaths)


# monkey patching
Individual.get_fitness = get_fitness_regression



# ################################################# first single tournament experiment #################################################

tournament_exp = tournmanent_experiment([2,4,6,8,10],
                                            n = 10, runs=100, pop_size=200, gens=30,
                                            crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)


tournament_exp_avg = tournament_exp[1]


## making plot

fig, ax = plt.subplots(figsize=(9,5))

# dictionary to keep track of the parameters
track_dic_tourn1 = {}
sizes_tourn1 = []
bf_tourn1 = []
f = open("results_final.txt", "a")
f.write("tournament results\n\n")
for i in range(len(tournament_exp_avg)):

    sizes_tourn1.append(tournament_exp_avg[i]['size'])
    bf_tourn1.append(min(tournament_exp_avg[i]['df'][('best_fitness','mean')]))

    
    ax.plot(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','mean')], label=tournament_exp_avg[i]['size'])
    ax.plot(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
    ax.plot(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
    ax.legend(title='Tournament Size')
    ax.fill_between(tournament_exp_avg[i]['df'].index, tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

track_dic_tourn1['sizes'] = sizes_tourn1
track_dic_tourn1['best_fitness_avg'] = bf_tourn1
f.write(str(track_dic_tourn1)+'\n\n')
track_dic_tourn1_df = pd.DataFrame(track_dic_tourn1)
track_dic_tourn1_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_tourn1_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')
plt.savefig('tournament_size2-10_2.png')
f.close()

# #plt.show()

################################################# second single tournament experiment #################################################

tournament_exp_2 = tournmanent_experiment([7,8,9,10,11],
                                              n = 10, runs=100, pop_size=200, gens=30,
                                            crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)


tournament_exp_avg_2 = tournament_exp_2[1]

# plot
fig, ax = plt.subplots(figsize=(9,5))

track_dic_tourn2 = {}
sizes_tourn2 = []
bf_tourn2 = []
f = open("results_final.txt", "a")
f.write("tournament results part 2\n\n")
for i in range(len(tournament_exp_avg)):

    sizes_tourn2.append(tournament_exp_avg_2[i]['size'])
    bf_tourn2.append(min(tournament_exp_avg_2[i]['df'][('best_fitness','mean')]))

    
    ax.plot(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','mean')], label=tournament_exp_avg_2[i]['size'])
    ax.plot(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
    ax.plot(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
    ax.legend(title='Tournament Size')
    ax.fill_between(tournament_exp_avg_2[i]['df'].index, tournament_exp_avg_2[i]['df'][('best_fitness','lower_bound')], tournament_exp_avg_2[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

track_dic_tourn2['sizes'] = sizes_tourn2
track_dic_tourn2['best_fitness_avg'] = bf_tourn2
f.write(str(track_dic_tourn2)+'\n\n')
track_dic_tourn2_df = pd.DataFrame(track_dic_tourn2).sort_values(by='best_fitness_avg')
track_dic_tourn2_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_tourn2_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')
plt.savefig('tournament_size7-11_2.png')
f.close()




# ######################################## making double tournament switch experiment ###########################################################

double_tournament_parameters = {"t_size": [2,4,6],
           "queens_t_size": [2, 4, 6] ,
           "deaths_t_size": [2, 4, 6],
           "switch":[True, False]
           }

double_tournament_exp = double_tournament_experiment(double_tournament_parameters,
                                              n = 10, runs=30, pop_size=200, gens=30,
                                            crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)


double_tournament_exp_avg = double_tournament_exp[1]

track_dic_dtourn1 = {}
t_sizes_dtourn1 = []
queens_t_sizes_dtourn1 = []
deaths_t_sizes_dtourn1 = []
switch_dtourn1 = []
bf_dtourn1 = []

# plot
fig, ax = plt.subplots(figsize=(9,5))

for i in range(len(double_tournament_exp_avg)):

    t_sizes_dtourn1.append(double_tournament_exp_avg[i]['parameters']['t_size'])
    queens_t_sizes_dtourn1.append(double_tournament_exp_avg[i]['parameters']['queens_t_size'])
    deaths_t_sizes_dtourn1.append(double_tournament_exp_avg[i]['parameters']['deaths_t_size'])
    bf_dtourn1.append(min(double_tournament_exp_avg[i]['df'][('best_fitness','mean')]))
    switch_dtourn1.append(double_tournament_exp_avg[i]['parameters']['switch'])

    color = 'blue'

    if double_tournament_exp_avg[i]['parameters']['switch'] == False:
        color = 'red'
    
    ax.plot(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','mean')], color = color)
    ax.plot(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], color=color, alpha=0.1)
    ax.plot(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], color=color, alpha=0.1)
    ax.fill_between(double_tournament_exp_avg[i]['df'].index, double_tournament_exp_avg[i]['df'][('best_fitness','lower_bound')], double_tournament_exp_avg[i]['df'][('best_fitness','upper_bound')], alpha=0.2, color = color)
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    red_patch = mpatches.Patch(color='red', label='False', linewidth=.1)
    blue_patch = mpatches.Patch(color='blue', label='True',linewidth=.1)
    ax.legend(handles=[red_patch, blue_patch], title = 'Switch')


track_dic_dtourn1['t_size'] = t_sizes_dtourn1
track_dic_dtourn1['deaths_t_size'] = deaths_t_sizes_dtourn1
track_dic_dtourn1['queens_t_size'] = queens_t_sizes_dtourn1
track_dic_dtourn1['switch'] = switch_dtourn1
track_dic_dtourn1['best_fitness_avg'] = bf_dtourn1


f = open("results_final.txt", "a")
f.write("double tournament switch testing results\n\n")
f.write(str(track_dic_dtourn1)+'\n\n')
track_dic_dtourn1_df = pd.DataFrame(track_dic_dtourn1).sort_values(by='best_fitness_avg')
track_dic_dtourn1_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_dtourn1_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')

plt.savefig('doubletournament_switch_2.png')
#plt.show()







# ########################################### making double tournament experiment parameters #######################################################
double_tournament_parameters_2 = {"t_size": [2,4,6,8,10],
           "queens_t_size": [2,4,6,8,10] ,
           "deaths_t_size": [2,4,6,8,10],
           "switch":[False]
           }

double_tournament_exp_2 = double_tournament_experiment(double_tournament_parameters_2,
                                              n = 10, runs=30, pop_size=200, gens=30,
                                            crossover_prob=0.9,mutation_prob=0.2, mutation=binary_mutation, crossover=single_point_co)

double_tournament_exp_avg_2 = double_tournament_exp_2[1]

#keeping track of the parameters
track_dic_dtourn2 = {}

t_sizes_dtourn2 = []
queens_t_sizes_dtourn2 = []
deaths_t_sizes_dtourn2 = []
bf_dtourn2 = []
switch_dtourn2 = []

for i in range(len(double_tournament_exp_avg_2)):

    t_sizes_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['t_size'])
    queens_t_sizes_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['queens_t_size'])
    deaths_t_sizes_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['deaths_t_size'])
    bf_dtourn2.append(min(double_tournament_exp_avg_2[i]['df'][('best_fitness','mean')]))
    switch_dtourn2.append(double_tournament_exp_avg_2[i]['parameters']['switch'])


track_dic_dtourn2['t_size'] = t_sizes_dtourn2
track_dic_dtourn2['deaths_t_size'] = deaths_t_sizes_dtourn2
track_dic_dtourn2['queens_t_size'] = queens_t_sizes_dtourn2
track_dic_dtourn2['switch'] = switch_dtourn2
track_dic_dtourn2['best_fitness_avg'] = bf_dtourn2


f = open("results_final.txt", "a")
f.write("double tournament grid testing results\n\n")
f.write(str(track_dic_dtourn2)+'\n\n')
track_dic_dtourn2_df = pd.DataFrame(track_dic_dtourn2).sort_values(by='best_fitness_avg')
track_dic_dtourn2_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_dtourn2_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')

f.close()




############################################### testing for different crossover probabilities ceteris paribus ###########################################################

grid_parameters_xo = {'mutation': [binary_mutation],
                   'mut_prob': [0.2],
                   'crossover': [single_point_co, k_point_co, cycle_crossover],
                   'xo_prob': [0.1,0.2,0.3,0.4,0.5, 0.6,0.7,0.8,0.9],
                   'selection': [tournament_sel]
                }

#grid_search_xo = grid_search(grid_parameters_xo, 10)[0] #done for 10x10 chessboard
grid_search_xo_avg = grid_search(grid_parameters_xo, 10)[1]

track_dic_xo= {}
#mutation_xo = []
#mut_prob_xo = []
crossover_xo = []
co_prob_xo = []
#selection_xo = []
bf_xo = []

fig, ax = plt.subplots(figsize=(12,7))
colors = {0.1:'blue',0.2:'blue',0.3:'blue',0.4:'green',0.5:'green', 0.6:'green',0.7:'red',0.8:'red',0.9:'red'}

for i in range(len(grid_search_xo_avg)):

    #mutation_xo.append(grid_search_xo_avg[i]['parameters']['mutation'].__name__)
    #mut_prob_xo.append(grid_search_xo_avg[i]['parameters']['mut_prob'])
    crossover_xo.append(grid_search_xo_avg[i]['parameters']['crossover'].__name__)
    co_prob_xo.append(grid_search_xo_avg[i]['parameters']['xo_prob'])
    #selection_xo.append(grid_search_xo_avg[i]['parameters']['selection'].__name__)
    bf_xo.append(min(grid_search_xo_avg[i]['df'][('best_fitness','mean')]))
    red_patch = mpatches.Patch(color='red', label='from 0.7 to 0.9', linewidth=.1)
    blue_patch = mpatches.Patch(color='blue', label='from 0.1 to 0.3',linewidth=.1)
    green_patch = mpatches.Patch(color='green', label='from 0.4 to 0.6',linewidth=.1)



    ax.plot(grid_search_xo_avg[i]['df'].index, grid_search_xo_avg[i]['df'][('best_fitness','mean')], color = colors[grid_search_xo_avg[i]['parameters']['xo_prob']])
    ax.plot(grid_search_xo_avg[i]['df'].index, grid_search_xo_avg[i]['df'][('best_fitness','lower_bound')], color=colors[grid_search_xo_avg[i]['parameters']['xo_prob']], alpha=0.1)
    ax.plot(grid_search_xo_avg[i]['df'].index, grid_search_xo_avg[i]['df'][('best_fitness','upper_bound')], color=colors[grid_search_xo_avg[i]['parameters']['xo_prob']], alpha=0.1)
    ax.fill_between(grid_search_xo_avg[i]['df'].index, grid_search_xo_avg[i]['df'][('best_fitness','lower_bound')], grid_search_xo_avg[i]['df'][('best_fitness','upper_bound')], alpha=0.2, color=colors[grid_search_xo_avg[i]['parameters']['xo_prob']])
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend(handles=[ blue_patch, green_patch, red_patch], title = 'probability')


# track_dic_xo['mutation'] = mutation_xo
# track_dic_xo['mut_prob'] = mut_prob_xo
track_dic_xo['crossover'] = crossover_xo
track_dic_xo['xo_prob'] = co_prob_xo
# track_dic_xo['selection'] = selection_xo
track_dic_xo['best_fitness_avg'] = bf_xo


f = open("cross_prob.txt", "a")
f.write("Crossover probability testing results\n\n")
f.write(str(track_dic_xo)+'\n\n')
track_dic_xo_df = pd.DataFrame(track_dic_xo).sort_values(by='best_fitness_avg')
track_dic_xo_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_xo_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')

f.close()

plt.savefig('xo_proba_test.png')
# plt.show()



########################################## grid search for the best crossover and mutation #######################################################

grid_parameters = {'mutation': [binary_mutation, swap_mutation, inversion_mutation],
                   'mut_prob': [0.2,0.4,0.6,0.8,0.9],
                   'crossover': [single_point_co, k_point_co, cycle_crossover],
                   'xo_prob': [0.7,0.8,0.9], #only high values
                   'selection': [tournament_sel]
                }

grid_search_exp = grid_search(grid_parameters, 10) #done for 10x10 chessboard
grid_search_exp_final = grid_search_exp[0]
grid_search_exp_avg = grid_search_exp[1]


# lets start a list where we have the first 5 solutions; we want to plot only the best solutions.
best_list = grid_search_exp_avg[:5]

# function to sort the list of dictionaries by the best fitness of each dataframe inside the dictionary
def get_min_fitness(dictionary):
    df = dictionary['df']
    min_fitness = df[('best_fitness','mean')].min()
    return min_fitness

# Sort the list of dictionaries based on the minimum fitness value of the dataframes inside it
best_list_sorted = sorted(best_list, key=get_min_fitness)

# print([get_min_fitness(best_list_sorted[i]) for i in range(len(best_list_sorted))])

# run in every dict in the list 
for i in range(5, len(grid_search_exp_avg)):

    # see if the current dictionary has better final fitness than the worst in our list (the last element)
    if get_min_fitness(grid_search_exp_avg[i]) < get_min_fitness(best_list_sorted[-1]):

        best_list_sorted[-1] = grid_search_exp_avg[i]

    best_list_sorted.sort(key=get_min_fitness)

# print([get_min_fitness(best_list_sorted[i]) for i in range(len(best_list_sorted))])

track_dic_grid = {}

mutation_grid = []
mut_prob_grid = []
crossover_grid = []
co_prob_grid = []
selection_grid = []
bf_grid = []

fig, ax = plt.subplots(figsize=(12,7))

for i in range(len(best_list_sorted)):

    mutation_grid.append(best_list_sorted[i]['parameters']['mutation'].__name__)
    mut_prob_grid.append(best_list_sorted[i]['parameters']['mut_prob'])
    crossover_grid.append(best_list_sorted[i]['parameters']['crossover'].__name__)
    co_prob_grid.append(best_list_sorted[i]['parameters']['xo_prob'])
    selection_grid.append(best_list_sorted[i]['parameters']['selection'].__name__)
    bf_grid.append(min(best_list_sorted[i]['df'][('best_fitness','mean')]))

    ax.plot(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','mean')], 
            label = f"{best_list_sorted[i]['parameters']['mutation'].__name__},prob={best_list_sorted[i]['parameters']['mut_prob']};{best_list_sorted[i]['parameters']['crossover'].__name__},prob={best_list_sorted[i]['parameters']['xo_prob']};{best_list_sorted[i]['parameters']['selection'].__name__}")
    ax.plot(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
    ax.plot(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
    ax.fill_between(best_list_sorted[i]['df'].index, best_list_sorted[i]['df'][('best_fitness','lower_bound')], best_list_sorted[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()


track_dic_grid['mutation'] = mutation_grid
track_dic_grid['mut_prob'] = mut_prob_grid
track_dic_grid['crossover'] = crossover_grid
track_dic_grid['xo_prob'] = co_prob_grid
track_dic_grid['selection'] = selection_grid
track_dic_grid['best_fitness_avg'] = bf_grid


f = open("results_final_grid.txt", "a")
f.write("Final grid search testing results\n\n")
f.write(str(track_dic_grid)+'\n\n')
track_dic_grid_df = pd.DataFrame(track_dic_grid).sort_values(by='best_fitness_avg')
track_dic_grid_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_grid_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')

f.close()

plt.savefig('final_grid.png')
# plt.show()

######################################## find out if other selection algorithms work better ##############################################

selection_parameters = {'mutation': [binary_mutation,],
                   'mut_prob': [0.6],
                   'crossover': [cycle_crossover],
                   'xo_prob': [0.9],
                   'selection': [tournament_sel, double_tournament, ranking]
                }

sel_search_exp = grid_search(selection_parameters, 10) #done for 10x10 chessboard
sel_search_exp_avg = sel_search_exp[1]


track_dic_sel= {}

selection_sel = []
bf_sel = []

fig, ax = plt.subplots(figsize=(12,7))

for i in range(len(sel_search_exp_avg)):

    selection_sel.append(sel_search_exp_avg[i]['parameters']['selection'].__name__)
    bf_sel.append(min(sel_search_exp_avg[i]['df'][('best_fitness','mean')]))

    ax.plot(sel_search_exp_avg[i]['df'].index, sel_search_exp_avg[i]['df'][('best_fitness','mean')], 
            label = f"{sel_search_exp_avg[i]['parameters']['selection'].__name__}")
    ax.plot(sel_search_exp_avg[i]['df'].index, sel_search_exp_avg[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
    ax.plot(sel_search_exp_avg[i]['df'].index, sel_search_exp_avg[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
    ax.fill_between(sel_search_exp_avg[i]['df'].index, sel_search_exp_avg[i]['df'][('best_fitness','lower_bound')], sel_search_exp_avg[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()

track_dic_sel['selection'] = selection_sel
track_dic_sel['best_fitness_avg'] = bf_sel


f = open("results_selection.txt", "a")
f.write("Results for testing different selection algorithms\n\n")
f.write(str(track_dic_sel)+'\n\n')
track_dic_grid_df = pd.DataFrame(track_dic_sel).sort_values(by='best_fitness_avg')
track_dic_grid_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_grid_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')

f.close()

plt.savefig('selection_grid.png')
# plt.show()



########################################################## test for elitism ##############################################################

elitism_exp = elitism_test(crossover=cycle_crossover,mutation=binary_mutation, mutation_prob=0.6, crossover_prob=0.9, selection=tournament_sel, t_size=9) #done for 10x10 chessboard
elitism_exp_avg = None
elitism_exp_avg = elitism_exp[1]


track_dic_elitism= {}
elitism = []
bf_elitism = []

fig, ax = plt.subplots(figsize=(12,7))

for i in range(len(elitism_exp_avg)):

    elitism.append(elitism_exp_avg[i]['elitism'])
    bf_elitism.append(min(elitism_exp_avg[i]['df'][('best_fitness','mean')]))

    ax.plot(elitism_exp_avg[i]['df'].index, elitism_exp_avg[i]['df'][('best_fitness','mean')], 
            label = f"{elitism_exp_avg[i]['elitism']}")
    ax.plot(elitism_exp_avg[i]['df'].index, elitism_exp_avg[i]['df'][('best_fitness','lower_bound')], color='tab:blue', alpha=0.1)
    ax.plot(elitism_exp_avg[i]['df'].index, elitism_exp_avg[i]['df'][('best_fitness','upper_bound')], color='tab:blue', alpha=0.1)
    ax.fill_between(elitism_exp_avg[i]['df'].index, elitism_exp_avg[i]['df'][('best_fitness','lower_bound')], elitism_exp_avg[i]['df'][('best_fitness','upper_bound')], alpha=0.2)
    ax.set_xlabel('Generation',size = 14)
    ax.set_ylabel('Best Fitness Found', size = 14)
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.legend()

track_dic_elitism['elitism'] = elitism
track_dic_elitism['best_fitness_avg'] = bf_elitism


f = open("results_elitism.txt", "a")
f.write("Results for testing elitism or not\n\n")
f.write(str(track_dic_elitism)+'\n\n')
track_dic_elitism_df = pd.DataFrame(track_dic_elitism).sort_values(by='best_fitness_avg')
track_dic_elitism_df.sort_values(by='best_fitness_avg', inplace=True)
f.write(tabulate(track_dic_elitism_df,tablefmt="github", headers='keys'))
f.write('\n\n\n')

f.close()

plt.savefig('results_elitism.png')
# plt.show()



################################################### final result #####################################################################



final_exp = run_experiment(n=10,
                           runs=100, 
                           pop_size=200, 
                           crossover_prob=0.9, 
                           mutation_prob=0.6, 
                           selection=tournament_sel, 
                           mutation=binary_mutation, 
                           crossover=cycle_crossover,
                           gens=30,
                           t_size=9,
                           )


# getting all unique representations found
f = open("results_final_indiv.txt", "a")
rep = set(tuple(x) for x in final_exp.loc[final_exp['best_fitness'] == -25, 'best_representation'])

f.write(str([Individual(representation = i) for i in rep]))

f.close()


##################################################### n=12 ####################################################

final_exp = run_experiment(n=12,
                           runs=30, 
                           pop_size=200, 
                           crossover_prob=0.9, 
                           mutation_prob=0.6, 
                           selection=tournament_sel, 
                           mutation=binary_mutation, 
                           crossover=cycle_crossover,
                           gens=50,
                           t_size=9,
                           )

# getting all unique representations found

f = open("results_final_indiv.txt", "a")

f.write('\n\n\n n=12')
rep = set(tuple(x) for x in final_exp.loc[final_exp['best_fitness'] == -12*2.5, 'best_representation'])

f.write(str([Individual(representation = i) for i in rep]))

f.close()
