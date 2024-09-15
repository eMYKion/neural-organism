from population import Population
from genome import Genome
import numpy as np
from enum import Enum
from typing import List, Dict
from tqdm import tqdm
import matplotlib.pyplot as plt
import numpy as np
import logging
import json
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
    def __init__(self, config, population: Population, display: bool, verbose: bool):

        self.config = config
        self.population = population
        self.display_freq = 5 # num generations to display
        self.display = display
        self.verbose = verbose

        plt.ion()
        plt.show(block=False)

    def run(self) -> List:

        logging.info('stat_headers=' + json.dumps(self.stat_display_headers))

        population = self.population

        if (population.size < 2):
            logging.warn("Population is extinct!")
            return []

        stat_list = []
        gen_range = range(self.config.num_generations)
        if not self.verbose: gen_range = tqdm(gen_range) # give user chance to see progress
        
        for gen_i in gen_range:

            stat_dict = population.get_default_stats()

            # TODO how do you want to evaluate an entity?
            

            select_dict = population.select(self.fitness)
            stat_dict.update(select_dict)

            # stats = {k:stat_dict[k] for k in self.config.statistics}

            # update population
            evolve_stats = population.evolve() # crossover
            stat_dict.update(evolve_stats)
            stat_list.append(stat_dict)

            # "housekeeping"

            if self.display and (gen_i % self.display_freq == 0):
                self.display_fitness(stat_dict['fitness_list'])

            # a string of key=value pairs
            row = ' '.join(["{}={}".format(k,stat_dict[k]) for k in self.stat_display_headers])
            logging.info(row)

            if (population.size < 2):
                logging.warn("Population went extinct!")
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



    def display_fitness(self, fitness_list, n_bins=12):
    
        plt.cla()
    
        plt.hist(fitness_list, bins=n_bins)
        plt.xlim(xmin=-2, xmax = 0.0)
        plt.ylim(ymin=0, ymax = 20)

        plt.draw()
        plt.pause(1e-1)