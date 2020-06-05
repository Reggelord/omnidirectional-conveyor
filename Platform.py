import pygame
from Cell import Cell


class Platform:

    def __init__(self,start_position,size,cell_size,window,font,sim_speed,cell_max_vel=[1,1,0.2],cell_acc = [0.1,0.1,0.01]):
        self.size = size #size of the platform. Height and width
        self.window = window
        self.font = font
        self.cell_size = cell_size
        self.properties = [cell_max_vel,cell_acc,sim_speed] # 
        
        self.pos = start_position # (0,0) position of platform
        self.cell_array = pygame.sprite.Group()
        self.update_cell_array(self.size[0],self.size[1])
        self.contact_cells = []
        self.click_shape = pygame.Rect(self.pos[0]-cell_size, self.pos[1]-cell_size, self.size[0]*cell_size, self.size[1]*cell_size)

        


    def update_cell_array(self,width,height):
        for row in range(width):
            for column in range(height):
                x_pos = self.pos[0]+self.cell_size*row
                y_pos = self.pos[1]+self.cell_size*column
                self.cell_array.add(Cell(self.cell_size,[row,column],[x_pos,y_pos],self.window,self.font,self.properties))
        

    def draw_platform(self,debug=0):
        
        for cell in self.cell_array:
            
            if debug == 1:
                cell.draw_cell(1)
            else:
                cell.draw_cell(0)



    def check_contact(self,obj):
        self.contact_cells = pygame.sprite.spritecollide(obj, self.cell_array, False,pygame.sprite.collide_mask )
        for cell in self.cell_array:
            cell.change_contact_color(0)

        for cell in self.contact_cells:
            cell.change_contact_color(1)
            

    def get_contact_cell_list(self):
        return self.contact_cells

    def setup_all_cells_vel(self,vector):
        for cell in self.cell_array:
            cell.set_velocity(vector)

    def update_cells_vel(self,cell_list,vel_list):
        if isinstance(vel_list[0],(float,int)):
            vel_list = [vel_list for i in range(len(cell_list))]

        if len(cell_list) != len(vel_list):
            print("Error, not enough parameters")

        for i,cell in enumerate(cell_list):
            if isinstance(cell_list[0],list):
                cell_coordinates = [cell[0],cell[1]]
                self.get_cell_by_number(cell_coordinates).set_velocity(vel_list[i])
            if isinstance(cell_list[0],Cell):
                cell_coordinates = cell.get_cell_number
                cell.set_velocity(vel_list[i])
            
    
    def get_cell_vel(self,cells):
        velocities =[]
        for cell in cells:

            if isinstance(cells[0],list): #List of cell coordinates 
                cell_coordinates = [cell[0],cell[1]]
                cell_vell = self.get_cell_by_number(cell_coordinates).get_velocity()
                velocities.append(cell_vell)

            if isinstance(cells[0],Cell):
                velocities.append(cell.get_cell_vel())
        if len(velocities) == 1:
            velocities = velocities[0]
        return velocities
        
        
    def get_cell_by_number(self,cell_number):
        for cell in self.cell_array:
            temp_coordinate = cell.get_cell_number()
            if temp_coordinate == cell_number:
                return cell

