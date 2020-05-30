from Platform import Platform
import copy
import numpy as np
from Box import Box

class Controller:

    def __init__(self,platform,default_param = [5,5,5]):
        
        self.platform = platform #Platform object

        
        self.next_pos = 0
        self.achieved_path = [0 for x in range(len(self.path_trajectory))]

        self.max_vel = default_param[0]
        self.goal_radius = default_param[1] #distance at which goal is approved 
        self.reached_goal = 0


    def get_box_pos(self):

        return np.array(self.box.get_position())

    def set_platform_velocity(self,velocity):
        #!!!!!!! Should not depend on contact !!!!!!
        contact_list = self.platform.get_contact_cell_list()
        self.platform.update_cells_vel(contact_list,velocity.tolist())
        

    def calulate_vel(self):
        box_pos = self.get_box_pos()
        goal_pos  = np.array(self.path_trajectory[self.next_pos])
        direction = goal_pos - box_pos
        norm = np.linalg.norm(direction)
        
        return (direction/norm)*self.max_vel

    def path_update(self):
        self.path_trajectory = self.path.get_path()


    def check_goal(self):
        return self.reached_goal

    def update(self):
        try:
            distance = self.get_box_pos()-self.path_trajectory[self.next_pos]

            while np.linalg.norm(distance) <= self.goal_radius:
                self.next_pos += 1
                distance = self.get_box_pos()-self.path_trajectory[self.next_pos]

            self.set_platform_velocity(self.calulate_vel())
        except:
            print("Goal reached")
            self.reached_goal = 1
        
