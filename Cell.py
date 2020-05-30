import pygame,copy

class Cell(pygame.sprite.Sprite):
    
    def __init__(self,size,number,position,window):

        pygame.sprite.Sprite.__init__(self)
        # Physic parameters
        self.window = window
        self.size = size # square platform heihgt
        self.position = position #Center postion of square
        self.number = number

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

    def get_cell_number(self):
        return self.number


    def change_contact_color(self,contact):
        if contact:
            self.box_color = (190,150,255,170)
        else:
            self.box_color = (100,100,100,0)