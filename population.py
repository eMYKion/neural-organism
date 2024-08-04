import random
import numpy as np
from genome import Genome

class Population:
    def __init__(self, size, inputs, outputs, add_node_prob=0.03, add_conn_prob=0.05):
        self.size = size
        self.inputs = inputs
        self.outputs = outputs
        self.add_node_prob = add_node_prob
        self.add_conn_prob = add_conn_prob

        self.genomes = [Genome(self.inputs, self.outputs) for _ in range(size)]
        self.generation = 0

    ''' genomes in the population mutate and crossover
    approximate DNA mixing for bearing offspring
    TODO change name
    multiply_rate: how many times to increase the population
    '''
    def evolve(self, multiply_rate=2.0):

        # mutates individual genomes
        stats = {
            "added_nodes" : [],
            "added_conns" : [],
            "mutated_weights" : [],
            "mutated_biases" : [],
        }
        for genome in self.genomes:
            if random.random() < self.add_node_prob:
                genome.mutate_add_node()
                stats["added_nodes"].append(1)
            else:
                stats["added_nodes"].append(0)

            if random.random() < self.add_conn_prob:
                genome.mutate_add_connection()
                stats["added_conns"].append(1)
            else:
                stats["added_conns"].append(0)

            stats["mutated_weights"].append(genome.mutate_weights(prob_mutate=0.8, delta_std_dev=0.05))
            stats["mutated_biases"].append(genome.mutate_biases(prob_mutate=0.8, delta_std_dev=0.05))

        # let the mutated genomes crossover
        next_gen = []
        for _ in range(int(self.size * multiply_rate)):
            parent1 = random.choice(self.genomes)
            parent2 = random.choice(self.genomes)
            child = parent1.crossover(parent2)
            next_gen.append(child)

        self.genomes = next_gen
        self.size = len(self.genomes)
        self.generation += 1

        return {
            "avg_added_nodes" : sum(stats["added_nodes"]) / len(stats["added_nodes"]),
            "avg_added_conns" : sum(stats["added_conns"]) / len(stats["added_conns"]),
            "avg_mutated_weights" : sum(stats["mutated_weights"]) / len(stats["mutated_weights"]),
            "avg_mutated_biases" : sum(stats["mutated_biases"]) / len(stats["mutated_biases"]),
        }

    ''' sccording to fitness_function, keeps top percentile of population alive (rest die)
    returns a list of all fitness scores for the generation before removal
    '''
    def select(self, fitness_function, percentile=0.50):
        
        fitnesses = [(genome, fitness_function(genome)) for genome in self.genomes]
        num_select = max(min(int(percentile * len(fitnesses)), len(fitnesses)), 1)
        selected = sorted(fitnesses, key=lambda x: x[1], reverse=True)[:num_select]

        self.genomes = [g for g,_ in selected]
        self.size = len(self.genomes)

        fitness_list = [x[1] for x in fitnesses]
        return {
            "fitness_list" : fitness_list,
            "avg_fitness" : sum(fitness_list) / len(fitness_list),
        }
    
    def get_default_stats(self):
        nodes = [g.inputs + g.outputs + g.hidden for g in self.genomes]
        enabled_genes = [np.sum(g.enabled) for g in self.genomes]
        return {
            'population': len(self.genomes),
            'generation': self.generation,
            "avg_nodes" : sum(nodes)/len(nodes),
            "avg_enabled_genes" : sum(enabled_genes)/len(enabled_genes),
        }