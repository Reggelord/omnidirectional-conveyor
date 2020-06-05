import sys, pygame,pygame_gui,copy
import numpy as np

from pygame.locals import*
from Box import Box
from Platform import Platform
from Buttons import Buttons

class Main_window():
    def __init__(self,height,width,default = 1):
        '''
        Initialize simulation
        Input:\n
            height,width - Height and width of the screen
            default - Set up platform and box init parameters (optional)
        Output: None
        '''
        ## Setup init Pygame ##
        pygame.init()
        # Initalize text
        pygame.font.init() 
        self.font = pygame.font.SysFont("arial", 10,bold = False)
        self.screen = pygame.display.set_mode((width,height))
        self.clock = pygame.time.Clock()
        #Buttons state
        self.is_sim_run = 0
        self.is_reset = 0
        #Objects 
        self.buttons = Buttons(self.screen,self.clock)
        self.box = None #Box object
        self.platform = None #Platform object
        self.box_path = None #Box path object
        self.controler = None #Platform controler object
        if default:
            self.setup_objects_default()

    def reset_sim(self):
        self.setup_objects_default()


    def setup_objects_default(self):
        '''
        Function for setting up default simulation parameters\n
        Input: None\n
        Output: None  
        '''
        self.platform = Platform((200,200),(10,10),50,self.screen,self.font)
        self.box = Box((40,80),[450,700,0],self.screen)       

    def run_sim(self):
        '''
        Function handling simulation\n
        Input: None\n
        Output: None
        '''
        #Update simulation state
        self.is_sim_run, self.is_reset = self.buttons.get_simulaion_state()

        if self.is_reset:
            self.reset_sim()

        if self.is_sim_run:
            try:
                #self.platform.setup_all_cells_vel([0.5,-1,0.2]) 
                self.platform.check_contact(self.box)
                contact_list = self.platform.get_contact_cell_list()
                if contact_list:
                    self.platform.update_cells_vel(contact_list,[0.5,-1,0.2]) #for testing purpose
                    
                    self.box.move_obj(self.platform.get_cell_vel([contact_list[0].get_cell_number()]))

            except:
                self.is_sim_run = 0
                self.buttons['Start/Stop'].set_text(chenage_text[self.is_sim_run])
                print('Cant run sim')
            
        self.draw_update_objects()

    def draw_update_objects(self):
        '''
        Function to draw all objects on\n
        Input: None\n
        Output: None
        '''
        self.screen.fill((0,0,0))
        self.platform.draw_platform(1)
        self.box.draw_box()
        self.buttons.draw_buttons()
        
        

def main():

    main_window = Main_window(900,800)
    pygame.display.update()
    while True:

        for events in pygame.event.get():
            main_window.buttons.update_events(events)

            if events.type == QUIT:
                sys.exit(0)
            

        

        main_window.run_sim()
        pygame.display.update()
        
main()