import sys, pygame,pygame_gui,copy
import numpy as np

from pygame.locals import*
from Box import Box
from Platform import Platform

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
        #Setup GUI
        self.UI = pygame_gui.UIManager((800, 600), 'data/themes/quick_theme.json')
        self.buttons_names = ['Start/Stop','Gen_path_points','Reset','Draw path']
        self.buttons={} #dictionary of buttons objects
        self.setup_buttons([150,40],10,[5,280])
        #Buttons state
        self.is_sim_run = 0 #is simulaion running, 'Start/Stop' buttons
        self.gen_path_points = 0 #if generating new path points, 'Gen_path_points' button
        self.drawing_path = 0 #if path is drawn, 'Draw path' button
        #Objects 
        self.box = None #Box object
        self.platform = None #Platform object
        self.box_path = None #Box path object
        self.controler = None #Platform controler object
        if default:
            self.setup_objects_default()

    def setup_objects_default(self):
        '''
        Function for setting up default simulation parameters\n
        Input: None\n
        Output: None  
        '''
        self.platform = Platform((200,200),(10,10),50,self.screen,self.font)
        self.box = Box((40,80),[450,700,0],self.screen)      
        


    def setup_buttons(self,size,space,position):
        '''
        Function for setting up buttons\n
        Input: \n
            size - size of buttons [x,y]\n space - space between buttons \nposition - position of buttons [x,y]
        Output: None 
        '''
        #Create buttons object and add them to 'buttons' dictionary
        for i,button_name in enumerate(self.buttons_names):
            location = pygame.Rect((position[0], position[1]+i*(space+size[1])), (size[0], size[1]))
            self.buttons[button_name] = pygame_gui.elements.UIButton(location,button_name,self.UI)


    def button_clicked(self,event):
        '''
        Function that handles button clicks\n
        Input: \n
            event - pygame event object
        Output: None
        '''
        if (event.type == pygame.USEREVENT and event.user_type == pygame_gui.UI_BUTTON_PRESSED): 
            ## Start/Stop ##
            if event.ui_element == self.buttons['Start/Stop']:
                chenage_text = ["Start","Stop"]
                self.is_sim_run = not self.is_sim_run
                self.buttons['Start/Stop'].set_text(chenage_text[self.is_sim_run])

            ######## Must add other buttons ######
        
       

    def run_sim(self):
        '''
        Function handling simulation\n
        Input: None\n
        Output: None
        '''
        try:
            self.platform.setup_all_cells_vel([0.5,-1,0.2]) #for testing purpose
            self.platform.check_contact(self.box)
            contact_list = self.platform.get_contact_cell_list()
            if contact_list:
                self.box.move_obj(self.platform.get_cell_vel(contact_list[0].get_cell_number()))
                
            
        
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
        self.platform.draw_platform()
        self.box.draw_box()
        self.UI.update(self.clock.tick(30))
        self.UI.draw_ui(self.screen)
        

def main():

    main_window = Main_window(900,800)

    pygame.display.update()
    while True:

        for events in pygame.event.get():
            if events.type == QUIT:

                sys.exit(0)
            
            main_window.UI.process_events(events)



        main_window.run_sim()
        pygame.display.update()
        

main()