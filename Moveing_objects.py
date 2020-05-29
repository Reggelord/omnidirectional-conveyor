import pygame,copy


class Box(pygame.sprite.Sprite):
    
    def __init__(self,size,position,window):
        pygame.sprite.Sprite.__init__(self)
        # Main parameters
        self.window = window
        self.size = size # box size
        self.position = position #Center postion of square [x,y,omega]
        self.velocity = [0, 0, 0] #velocity of the platform [V_x,V_y,omega]
        self.box_color = (0,0,255)

        self.box_sprite = pygame.image.load('sprites/box.png')#size 10 * 10
        self.box_sprite =pygame.transform.scale(self.box_sprite,self.size)
        self.image = self.box_sprite
        self.rect = self.box_sprite.get_rect()
        self.draw_position = [self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2]
        self.rect.x = self.draw_position[0]
        self.rect.y = self.draw_position[1]

        self.updated_sprite = self.box_sprite
        


        #Sprite object move
        #Collision object

        self.ID = 0

    def move_obj(self,vector):
        #update positions
        self.position[0] +=  vector[0]
        self.position[1] +=  vector[1]
        self.position[2] +=  vector[2]


        #update display
        self.updated_sprite = pygame.transform.rotate(self.box_sprite,self.position[2])
        self.image = self.updated_sprite
        self.rect = self.updated_sprite.get_rect()
        self.draw_position = [self.position[0] - self.size[0]/2, self.position[1] - self.size[1]/2]
        self.rect.x = self.draw_position[0]
        self.rect.y = self.draw_position[1]
        self.size = self.rect.size


    def get_collision_shape(self):
        return self.box_sprite


    def draw_box(self):
        '''
        Function to draw cell

        '''
        self.window.blit(self.updated_sprite,self.rect)
    
    def get_position(self):
        copy.deepcopy(self.position)
        return copy.deepcopy(self.position)
        

class Cell(pygame.sprite.Sprite):
    
    def __init__(self,size,number,position,window):

        pygame.sprite.Sprite.__init__(self)
        # Physic parameters
        self.window = window
        self.size = size # square platform heihgt
        self.position = position #Center postion of square
        self.number = []

        self.image = pygame.transform.scale(pygame.image.load('sprites/cell.png'),(self.size,self.size))
        self.rect = self.image.get_rect()
        self.draw_position = [x - self.size/2 for x in position]
        self.rect.x = self.draw_position[0]
        self.rect.y = self.draw_position[1]

        self.velocity = [0, 0, 0] #velocity of the platform
        self.if_active = 0
        self.if_active = 0 # if cell is active
        self.if_box = 0 #if box on the cell

        #Drawing parameters

        self.box_color = (255,255,255)
        self.line_color = (0,255,0)
        self.ID = 0

    def get_velocity(self,print_vel = 0):
        '''
        Functin to get velocity of platform cell
        Input: 
            print_vel - print current velocity (optional)
        Output: None
        '''
        if print_vel == 1:
            print("Velocity of box: x = %.3f, y = %.3f" % (self.velocity[0], self.velocity[1],self.velocity[2]))
        return self.velocity

    def set_velocity(self,vector):
        '''
        Functin to set velocity of platform cell
        Input: 
            vector - list/vector [x_vel,y_vel,omega_vel]
        Output: None
        '''
        self.velocity = vector
        
    def draw_cell(self):
        '''
        Function to draw cell

        '''

        #Draw cell
        self.window.blit(self.image,self.rect)

        #Draw detected contact
        contact_surface = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        contact_surface.fill(self.box_color)
        self.window.blit(contact_surface,self.draw_position)
        
    def draw_arrow(self):
        start_point = (self.position)
        end_point = ([x + 100*vel for x,vel in zip(self.position, self.velocity)])
        pygame.draw.line(self.window,self.line_color,start_point,end_point,3)
    
    
    def get_collision_shape(self):
        return self.collision_mask

        
    def change_contact_color(self,contact):
        if contact:
            self.box_color = (190,150,255,170)
        else:
            self.box_color = (100,100,100,0)


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