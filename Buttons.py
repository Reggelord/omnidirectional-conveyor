import pygame_gui, pygame

class Buttons():
    def __init__(self,window,clock,clock_speed,buttons_location = [[150,40],10],buttons_size = [5,280]):

        self.window = window
        self.UI = pygame_gui.UIManager((800, 600), 'data/themes/quick_theme.json')
        self.buttons_names = ['Start/Stop','Gen_path_points','Reset','Draw path']
        self.buttons={} #dictionary of buttons objects
        self.setup_buttons(buttons_location[0],buttons_location[1],buttons_size)

        self.clock = clock
        self.clock_speed = clock_speed
        #Buttons state
        self.is_sim_run = 0 #is simulaion running, 'Start/Stop' buttons
        self.is_reset = 0
        self.gen_path_points = 0 #if generating new path points, 'Gen_path_points' button
        self.drawing_path = 0 #if path is drawn, 'Draw path' button
        

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

            ## Path Gen ##
            if event.ui_element == self.buttons['Gen_path_points']:
                self.gen_path_points = not self.gen_path_points

            ## Draw path ##
            if event.ui_element == self.buttons['Draw path']:
                try:
                    self.box_path.generate_path(1)
                    self.drawing_path = not self.drawing_path
                
                except: 
                    print("Could not generate path")

            ## Reset ##
            if event.ui_element == self.buttons['Reset']:
                
                self.is_reset = 1
                self.is_sim_run = 0
            else:
                self.is_reset = 0    
        
    def update_events(self,event):
        self.button_clicked(event)
        self.UI.process_events(event)
    
    def draw_buttons(self):
        self.UI.update(self.clock.tick(100))
        self.UI.draw_ui(self.window)

    def get_simulaion_state(self):
        return self.is_sim_run, self.is_reset