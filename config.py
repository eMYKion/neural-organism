from yacs.config import CfgNode as CN

_DEFAULT_CFG = CN()

# experiment metadata
_DEFAULT_CFG.meta = CN()
_DEFAULT_CFG.meta.name = ''
_DEFAULT_CFG.meta.description = ''

_DEFAULT_CFG.population = CN()
_DEFAULT_CFG.population.size = 50
_DEFAULT_CFG.population.inputs = 3
_DEFAULT_CFG.population.outputs = 3
_DEFAULT_CFG.population.add_node_prob = 0.03
_DEFAULT_CFG.population.add_conn_prob = 0.05

# data about organisms/agents
_DEFAULT_CFG.simulation = CN()
_DEFAULT_CFG.simulation.statistics = ["generation", "population", "avg_fitness"]
_DEFAULT_CFG.simulation.num_generations = 100

def get_default():
  """Get a yacs CfgNode object with default values for my_project."""
  # Return a clone so that the defaults will not be altered
  # This is for the "local variable" use pattern
  return _DEFAULT_CFG.clone()

def load_file(filename):
  config = get_default()
  config.merge_from_file(filename)
  config.freeze()
  return config