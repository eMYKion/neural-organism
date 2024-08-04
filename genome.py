import random
import numpy as np

# Activation function
def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def softmax(x : np.ndarray):
    return np.exp(x) / np.sum(np.exp(x), axis=0)


# TODO this class is too long. Consider making code shorter
class Genome:
    def __init__(self, inputs, outputs):
        self.inputs = inputs
        self.outputs = outputs
        self.hidden = 0
        self.nodes = np.array([i for i in range(inputs + outputs)])
        # initialize random weights with gaussian distribution with mean 0 and std dev 1
        self.weights = np.random.normal(0, 1.0, (inputs + outputs, inputs + outputs))
        self.biases = np.random.normal(0, 1.0, (inputs + outputs))
        self.enabled = np.ones((inputs + outputs, inputs + outputs), dtype=bool)

    def mutate_add_node(self, weight=1.0):
        if not np.any(self.enabled):
            return

        in_node, out_node = np.argwhere(self.enabled == True)[random.randint(0, np.sum(self.enabled) - 1)]
        self.enabled[in_node, out_node] = False

        new_node = self.inputs + self.outputs + self.hidden
        self.hidden += 1
        self.nodes = np.append(self.nodes, new_node)

        new_weights = np.random.normal(0, 1.0, (len(self.nodes), len(self.nodes)))
        new_weights[:len(self.weights), :len(self.weights)] = self.weights
        self.weights = new_weights

        new_biases = np.random.normal(0, 1.0, len(self.nodes))
        new_biases[:len(self.biases)] = self.biases
        self.biases = new_biases

        new_enabled = np.ones((len(self.nodes), len(self.nodes)), dtype=bool)
        new_enabled[:len(self.enabled), :len(self.enabled)] = self.enabled
        self.enabled = new_enabled

        self.weights[in_node, new_node] = weight
        self.weights[new_node, out_node] = self.weights[in_node, out_node]

        self.enabled[in_node, new_node] = True
        self.enabled[new_node, out_node] = True

    def mutate_add_connection(self): # if no connection, add it, else reset it
        if len(self.nodes) < 2:
            return

        in_node, out_node = random.choice(self.nodes), random.choice(self.nodes)
        if in_node == out_node:
            return

        self.weights[in_node, out_node] = random.uniform(-1, 1)
        self.enabled[in_node, out_node] = True

    def mutate_weights(self, prob_mutate=0.8, delta_std_dev=0.05): # returns how much were mutated, rest are reset
        # mutate
        delta = np.random.normal(0, delta_std_dev, self.weights.shape)

        mutate_mask = np.random.uniform(0, 1, self.weights.shape) < prob_mutate

        self.weights += mutate_mask * delta

        return np.sum(mutate_mask)

    def mutate_biases(self, prob_mutate=0.8, delta_std_dev=0.05):

        delta = np.random.normal(0, delta_std_dev, self.biases.shape)

        # which biases to mutate
        mutate_mask = np.random.uniform(0, 1, len(self.biases)) < prob_mutate

        self.biases += mutate_mask * delta

        return np.sum(mutate_mask)

    def crossover(self, other):
        child = Genome(self.inputs, self.outputs)
        child.hidden = max(self.hidden, other.hidden)
        child.nodes = np.unique(np.concatenate((self.nodes, other.nodes)))
        
        child.weights = np.zeros((len(child.nodes), len(child.nodes)))
        child.biases = np.zeros(len(child.nodes))
        child.enabled = np.zeros((len(child.nodes), len(child.nodes)), dtype=bool)

        # cross over the weights, 
        # if both parents have gene, (enabled) 50% chance from either parent
        # if only one parent has gene, take it from that parent
        # else no gene to inherit

        # resize to match
        tmp = np.zeros(child.weights.shape, dtype=bool)

        self_enabled=tmp.copy()
        self_enabled[:len(self.nodes), :len(self.nodes)] = self.enabled

        other_enabled = tmp.copy()
        other_enabled[:len(other.nodes), :len(other.nodes)] = other.enabled

        child.enabled = np.logical_or(self_enabled, other_enabled)
        both_enabled = np.logical_and(self_enabled, other_enabled)

        only_one_enabled = np.logical_xor(self_enabled, other_enabled)

        weights_choice = np.random.uniform(0.0, 1.0, child.weights.shape) < 0.5

        tmp = np.zeros(child.weights.shape, dtype=float)

        self_weights = tmp.copy()
        self_weights[:self.weights.shape[0], :self.weights.shape[1]] = self.weights

        other_weights = tmp.copy()
        other_weights[:other.weights.shape[0], :other.weights.shape[1]] = other.weights

        # a random choice between self and other
        weights_both = self_weights * weights_choice + other_weights * np.logical_not(weights_choice)

        child.weights = weights_both * both_enabled \
            + only_one_enabled * (self_weights * self_enabled + other_weights * other_enabled)


        # cross over the biases
        tmp = np.zeros(child.biases.shape, dtype=bool)
        
        where_self_bias = tmp.copy()
        where_self_bias[:len(self.biases)] = 1

        where_other_bias = tmp.copy()
        where_other_bias[:len(other.biases)] = 1

        tmp = np.zeros(child.biases.shape, dtype=float)

        self_biases = tmp.copy()
        self_biases[:len(self.biases)] = self.biases

        other_biases = tmp.copy()
        other_biases[:len(other.biases)] = other.biases

        where_both_bias = np.logical_and(where_self_bias, where_other_bias)
        biases_choice = np.random.uniform(0.0, 1.0, child.biases.shape) < 0.5
        biases_both = self_biases * biases_choice + other_biases * np.logical_not(biases_choice)

        child.biases = biases_both * where_both_bias \
            + np.logical_xor(where_self_bias, where_other_bias) \
            * (self_biases * where_self_bias + other_biases * where_other_bias)

        return child

    def forward(self, inputs, max_tries=10, tol=1e-4):
        # TODO make batched
        values = np.zeros(len(self.nodes))
        values[:self.inputs] = inputs
        '''
        convergence means stable network values after several propogations and "freezing" input values
        stable convergence not guarenteed(?) with arbitrary topology
        -> Hopfield Network paper says rapid convergence in 2-3 steps,
        which I do experimentally observe as well
        must choose from a set of evaluation techniques
        '''
        steps = 0

        diff = np.inf
        old_values = None
        while (diff > tol and steps < max_tries):
            # let input propogate to all nodes
            old_values = values.copy()

            values = values @ (self.weights * self.enabled) + self.biases

            # apply nonliearity

            # input and hidden nodes
            values[:self.inputs] = sigmoid(values[:self.inputs])
            values[self.inputs + self.outputs:] = sigmoid(values[self.inputs + self.outputs:])
            # output nodes get "special" nonlinearity
            values[self.inputs:self.inputs + self.outputs] = softmax(values[self.inputs:self.inputs + self.outputs])

            # simulates 'persistence of input within forward pass time step'
            values[:self.inputs] = inputs

            # TODO total or average?
            diff = sum((values - old_values)**2)
            steps += 1
        
        outputs = values[self.inputs:self.inputs + self.outputs]
        return outputs