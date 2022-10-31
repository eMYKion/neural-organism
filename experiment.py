from gui.pygame_gui import PygameGui

class Experiment:
    """class for an experiment"""

    def __init__(self, id, desc):
        # TODO: load from yacs config
        self.id = id
        self.description = desc

        self.gui = PygameGui()


    def run(self):

        while self.gui.render():
            # TODO can calculations outside of render, 
            # e.g. world coords vs pygame window coords
            pass
        
        self.gui.quit()


def load_experiment(exp_num):
    """ loads and returns an experiment to run
    
    exp_num: experiment number
    """

    return Experiment(id=exp_num, desc="dummy experiment")


        