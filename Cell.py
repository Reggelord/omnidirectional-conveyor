import pygame,copy

class Cell(pygame.sprite.Sprite):
    
    def __init__(self,size,number,position,window,font,properties,cell_type=0):

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

        self.sim_speed = properties[2]
        self.max_vel = properties[0]
        self.max_acc = properties[1]
        

        self.velocity = [0, 0, 0]#velocity of the platform

        self.type = cell_type

        self.if_active = 0
        self.if_active = 0 # if cell is active
        self.if_box = 0 #if box on the cell

        #Drawing parameters
        self.box_color = (255,255,255)
        self.line_color = (0,255,0)
        self.ID = 0

        #Debug
        self.font = font
        self.text_position = self.draw_position

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
        #if requested velocity higher than max set it to max
        higher_than_max = 0 
        for i,x in enumerate(vector):
            if abs(x) > abs(self.max_vel[i]):

                x = self.max_vel[i]
                if higher_than_max == 0:
                    higher_than_max = 1
        #print information
        if higher_than_max:
            print("Requested velocity higher than max" + str(self.max_vel) + "\nMax velocity have been set" )
        

        if self.type == 0:
            for i,x in enumerate(vector):
                sign = lambda x: x and (1, -1)[x < 0]
                if abs(self.velocity[i]) < abs(x):
                    self.velocity[i] += sign(x)*self.max_acc[i]/ self.sim_speed
                    
                if abs(self.velocity[i]) > abs(x):
                    self.velocity[i] =x

        
        
    def draw_cell(self,debug=0):
        '''
        Function to draw cell

        '''

        #Draw cell
        self.window.blit(self.image,self.rect)

        #Draw detected contact
        contact_surface = pygame.Surface((self.size,self.size),pygame.SRCALPHA)
        contact_surface.fill(self.box_color)
        self.window.blit(contact_surface,self.draw_position)
        if debug == 1:
            self.draw_arrow()
            self.draw_text() #draw
        
    def draw_arrow(self):
        start_point = (self.position)
        end_point = ([x + 100*vel for x,vel in zip(self.position, self.velocity)])
        pygame.draw.line(self.window,self.line_color,start_point,end_point,3)
    
    
    def get_collision_shape(self):
        return self.collision_mask

    def get_cell_number(self):
        return self.number

    def draw_text(self):
        self.text_background = pygame.Rect(self.draw_position[0], self.draw_position[1], 40, 15) #Create shape 
        pygame.draw.rect(self.window,(0,0,0),self.text_background)
        text_to_print = str(self.velocity[0]) + ' ;' + str(self.velocity[1]) + ' ;' + str(self.velocity[2])
        text = self.font.render(str(text_to_print), False, (255, 255, 255))
        self.window.blit(text,self.text_position)


    def change_contact_color(self,contact):
        if contact:
            self.box_color = (190,150,255,170)
        else:
            self.box_color = (100,100,100,0)