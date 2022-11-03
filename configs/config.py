from yacs.config import CfgNode as CN

_DEFAULT_CFG = CN()

# experiment metadata
_DEFAULT_CFG.meta = CN()
_DEFAULT_CFG.meta.name = ''
_DEFAULT_CFG.meta.description = ''

# data about organisms/agents
_DEFAULT_CFG.agents = CN()
_DEFAULT_CFG.agents.num_init = 1

def get_cfg_defaults():
  """Get a yacs CfgNode object with default values for my_project."""
  # Return a clone so that the defaults will not be altered
  # This is for the "local variable" use pattern
  return _DEFAULT_CFG.clone()