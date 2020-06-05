import pygame,copy


class Box(pygame.sprite.Sprite):
    
    def __init__(self,size,position,sim_speed,window):
        pygame.sprite.Sprite.__init__(self)
        # Main parameters
        self.window = window
        self.size = size # box size
        self.position = position #Center postion of square [x,y,omega]
        self.velocity = [0, 0, 0] #velocity of the platform [V_x,V_y,omega]
        self.box_color = (0,0,255)
        self.sim_speed = sim_speed
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
        self.position[0] +=  vector[0]/self.sim_speed
        self.position[1] +=  vector[1]/self.sim_speed
        self.position[2] +=  vector[2]/self.sim_speed


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
        




