import numpy as np

class Agent:

    def __init__(self):
        # these are in world coords
        self.position = np.array([50.0, 50.0])
        self.normal = np.array([0.0, 1.0])

        #self.stored_energy = 10.0

        # senses
        #self.hunger = SenseHunger()

        # nondirectional eyes for now
        self.eyes_rel_pos = np.array([[-5.0,8.66],[0.0,10.0],[5.0,8.66]])
        #self.eyes_rel_normal = np.array([[-0.5,0.866],[0.0,1.0],[0.5,0.866]])
        #self.eye0 = SenseFoodEye(rel_pos=np.array([-5.0,8.66]))
        #self.eye1 = SenseFoodEye(rel_pos=np.array([0.0,10.0]))
        #self.eye2 = SenseFoodEye(rel_pos=np.array([5.0,8.66]))

        self.sense_activations = np.array([0.0, 0.0, 0.0]) # for three eyes

        # actions
        #self.forward = ActionForward(step=2.0)
        #self.rot_cw = ActionRotate(step=-15.0/360 * 2 * np.pi)
        #self.rot_ccw = ActionRotate(step=15.0/360 * 2 * np.pi)

        # neural network
        # self.nn = MLP()
    
    def update(self, food_pos_list):
        """Given world state, get senses, and perform actions
        params:
            food_pos_list: [N,2] array of N food positions
        """
        # TODO test an update step
        
        num_eyes = self.eyes_rel_pos.shape[0]
        distances = self.eyes_rel_pos.copy() * 0
        eyes_pos = self.eyes_rel_pos + self.position
        S = 100 # base food light intensity
        for i in range(num_eyes):
            squared_distances = np.sum((food_pos_list - eyes_pos[i])**2, axis=1)

            self.sense_activations[i] = np.sum(1 / squared_distances) * S / (4 * np.pi)


