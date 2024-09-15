# neural-organism (incomplete)

A simulation playground implementing Neural Evoluion of Augmenting Topologies (NEAT).
Please note that I used ChatGPT to help me get started with the outlines of the 
`Genome` and `Population` classes.

Also, please note that the terminology used in this software project
does not yet align with biological/A.I. definitions as this is an incomplete project.

## How it works

Each organism is represented by a `Genome` class.
Each `Genome` is a set of nodes/neurons, and a matrix of weights/biases between them.

A population of organisms is the `Population` class.
Each `Population` has a list of `Genomes` and a generation number.

A Simulation proceeds in rounds. each round (generation), fitness is calculated,
and the population keeps the most fit genomes. Then the population 'evolves' 
(mixes genomes and makes offspring).


# TODO
- replace placeholder fitness function
- use an Environment with a 2D grid for entities to move
- control movement with neural network outputs

## Setup
- anaconda or miniconda/python3.9: `$ conda env create -f environment.yml`
- Make (optional, only needed for development: commands in Makefile)

## Running

To run an expriment:
```bash
$ conda activate neat
(neural-org)$ python run.py experiment.yaml -s -v
```

