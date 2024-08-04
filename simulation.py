from population import Population
from genome import Genome
import numpy as np
from enum import Enum
from typing import List, Dict
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
# from gui.pygame_gui import PygameGui

class Simulation:
    """class for an simulation"""

    stat_display_headers = ('generation', 'population', 'avg_fitness',
        "avg_nodes", "avg_enabled_genes",
        'avg_added_nodes', "avg_added_conns", 
        "avg_mutated_weights", "avg_mutated_biases",
    )

    '''
    "avg_added_nodes"
    "avg_added_conns"
    "avg_mutated_weights"
    "avg_mutated_biases"
    '''


    # TODO add an Environment class that serves as simulation grounds
    def __init__(self, config, population: Population):

        self.config = config
        self.population = population

        plt.ion()
        plt.show(block=False)

    def run(self, verbose=False) -> List:

        if verbose:
            print(self.stat_display_headers)

        population = self.population

        stat_list = []
        for gen_i in tqdm(range(self.config.num_generations)):

            stat_dict = population.get_default_stats()

            # TODO how do you want to evaluate an entity?
            

            select_dict = population.select(self.fitness)
            stat_dict.update(select_dict)

            # stats = {k:stat_dict[k] for k in self.config.statistics}

            # update population
            evolve_stats = population.evolve() # crossover
            stat_dict.update(evolve_stats)


            stat_list.append(stat_dict)

            if gen_i % 10 == 0 and verbose:
                self.show_stats(stat_dict)

            if (population.size < 2):
                print("[NOTE]: Population went extinct!")
                break
        
        return stat_list
    

    '''
    static environment
    '''
    def fitness(self, genome: Genome):
        # TODO rewrite for dynamic environment

        # return average fitness over a set of placeholder input-output pairs
        N = 100
        inputs = np.random.rand(N, genome.inputs)

        # targets is a one-hot encoding vector of the max input node
        targets = np.zeros(inputs.shape) 
        targets[np.arange(N), np.argmax(inputs, axis=1)] = 1

        outputs = np.zeros(targets.shape)

        for i in range(N):
            outputs[i,:] = genome.forward(inputs[i,:])
        
        return np.mean(-np.sum((outputs - targets)**2, axis=1))  # Example fitness function



    def show_stats(self, stat_dict, n_bins=12):
        
        row = ("{}\t" * len(self.stat_display_headers))\
            .format(*[stat_dict[s] for s in self.stat_display_headers])
        print(row)
        #print("\ngeneration {generation:04}, avg_fit {avg_fitness}:\n".format(**stat_dict))

        plt.cla()
    
        plt.hist(stat_dict['fitness_list'], bins=n_bins)
        plt.xlim(xmin=-2, xmax = 0.0)
        plt.ylim(ymin=0, ymax = 20)

        plt.draw()
        plt.pause(1e-1)