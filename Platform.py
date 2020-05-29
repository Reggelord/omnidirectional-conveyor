import pygame
from Cell import Cell


class Platform:

    def __init__(self,start_position,size,cell_size,window):
        self.size = size #size of the platform. Height and width
        self.window = window
        self.cell_size = cell_size
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
                self.cell_array.add(Cell(self.cell_size,[row,column],[x_pos,y_pos],self.window))
        

    def draw_platform(self,draw_velocity=0):
        
        for cell in self.cell_array:
            cell.draw_cell()
            if draw_velocity == 1:
                cell.draw_arrow()



    def check_contact(self,obj):
        self.contact_cells = pygame.sprite.spritecollide(obj, self.cell_array, False,pygame.sprite.collide_mask )
        for cell in self.cell_array:
            cell.change_contact_color(0)

        for cell in self.contact_cells:
            cell.change_contact_color(1)
            

    def get_contact_cell_list(self):
        return self.contact_cells

    def setup_all_cells_vel(self):
        for row in self.cell_array:
            for cell in row: 
                pass

    def update_cells_vel(self,cell_list,vel_list):
        if isinstance(vel_list[0],(float,int)):
            vel_list = [vel_list for i in range(len(cell_list))]

        if len(cell_list) != len(vel_list):
            print("Error, not enough parameters")

        for i,cell in enumerate(cell_list):
            
            cell_x = cell[0]
            cell_y = cell[1]
            self.cell_array[cell_x][cell_y].set_velocity(vel_list[i])
    
    def get_cell_vel(self,cell_coordinates):
        x = cell_coordinates[0]
        y = cell_coordinates[1]
        return self.cell_array[x][y].get_velocity()