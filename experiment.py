from agent import Agent
from gui.pygame_gui import PygameGui

class Experiment:
    """class for an experiment"""

    def __init__(self, cfg):
        # TODO: load from yacs config
        self.cfg = cfg

        self.gui = PygameGui()
        
        # TODO create method to initialize agents
        self.agent_list = []
        for i in range(self.cfg.agents.num_init):
            self.agent_list.append(Agent())

    def run(self):

        while self.gui.render(self.agent_list):
            # TODO can do calculations outside of render, 
            # e.g. population size, world coords (vs pygame window coords)
            # nn reactions
            pass
        
        self.gui.quit()


def load_experiment(exp_cfg):
    """ loads and returns an experiment to run
    
    exp_num: experiment number
    """

    return Experiment(cfg=exp_cfg)


        