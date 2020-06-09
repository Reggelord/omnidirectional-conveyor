from Platform import Platform
import pygame
import copy
import numpy as np
from Box import Box

class Controller:

    def __init__(self,platform,objects,goal,mode,window):
        
        self.platform = platform #Platform object
        self.objects = objects #all the objects
        self.end_goal = goal #area that is considereda goal, Propably Rect object
        
        self.mode = mode #1.Depalletization 2.Palletization ?3.Manual
        self.states = [0,0,0] # states of the controller. It helps to shedue the controller work
        self.window = window
        self.border_line = self.platform.pos[1] + self.platform.size[1]*self.platform.cell_size/2  # y_pos of border line for stage 1 movement
### Common operations ###
    def move_objects(self):
        self.platform.check_all_contacts(self.objects)
        self.reset_velocities()
        for box in self.objects:

            if box.task == 1: #move box out of pallete
                self.move_out_pallete(box)
                if box.position[1] >= self.border_line: #if box out of pallete
                    self.states[1] = 1
                    box.task = 2
                    self.states[0] = 0

            if box.task == 2:
                if self.states[1] == 1:
                    self.set_pre_pickup_path(box)
                    box.task = 3
                    self.states[1] = 0

            if box.task == 3 :
                self.move_to_pre_pickup(box)

            if box.task == 4:
                self.objects.remove(box)
                    

            box.new_move_obj()
        
        
    def update_states(self): #update boxes state and move them
        if self.states[0] == 0:
            self.chose_box_to_remove()

        if self.states[1] == 1:
            self.set_pre_pickup_path()
        
    def reset_velocities(self):
        self.platform.setup_all_cells_vel([0,0,0])

    
### Stage 1 operations ###

    def chose_box_to_remove(self):
            #find closest box without task
            closest_box = None
            min_distance = 1000000000
            no_boxes_left = 1
           
            
            for box in self.objects:
                if box.task == 0 and box.one_contact_cell():   #if there is no task was assigned
                    if no_boxes_left:
                        no_boxes_left = 0
                    
                    b_pos = box.get_position()
                    distance = ((b_pos[0]-self.end_goal.centerx)**2 + (b_pos[1]-self.end_goal.centery)**2)**0.5
                    if distance < min_distance:
                        min_distance = distance
                        closest_box = box
            
            if no_boxes_left:
                return 0

            closest_box.task = 1
            self.states[0] = 1

    def move_out_pallete(self,box):
        for cell in box.contact_cells:
            if len(cell.obj_contacts) == 1:
                cell.set_velocity([0,0.5,0])

### Stage 2 operations ###

    def set_pre_pickup_path(self,box): #set path close to pickup platform
        start_pos=box.position[0:2] # Rigth now only position
        end_position = [self.end_goal.centerx,self.end_goal.centery-80]
        no_points = 10
        steps = [(end_position[0]-start_pos[0])/(no_points),(end_position[1]-start_pos[1])/(no_points-1)]
        for i in range(no_points):
            box.trajectory.append([start_pos[0]+steps[0]*(i+1),start_pos[1] + steps[1]*(i+1)])

    def move_to_pre_pickup(self,box):
        if box.check_goal() == 1:
                    box.task = 4
        else:
            for cell in box.contact_cells:
                if len(cell.obj_contacts) == 1:
                    vector = [box.get_current_goal()[0] - box.position[0],box.get_current_goal()[1] - box.position[1],0]
                    cell.set_velocity(vector)
                
### Stage 3 operations ###

### Draw ###
    def draw_border_line(self):
        start_point = (self.platform.pos[0]-self.platform.cell_size/2,self.border_line)
        end_point = (self.platform.pos[0] + (self.platform.size[0]-0.5)*self.platform.cell_size,self.border_line)
        pygame.draw.line(self.window,(255,255,0),start_point,end_point,5)
