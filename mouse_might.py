'''
This is meant to be a model of two mice interacting in a bounded region. There are a few goals for this the progression of this project: 
    1. Getting a point to move randomly in a bounded region
    2. Getting a circle, whose center is a randomly moving point, to move in a bounded region
    3. Dealing with boundary conditions --> that is, we want the circle to either bounce against the boundary
       once it meets it  
    4. We want to add a triangular head that attaches to the circle. Now, the center of the triangle directs the random 
       motion of the 

''' 

import pygame 

def class Window: 
    def __init__(self):
        pass 

    def create_mice(self):
        pass

    def update_mice_movement(self): 
        pass 

    def draw(self): 
        pass 

def class Mouse: 
    def __init__(self):
        pass 

    def set_initial_state(self):
        pass 

    def do_turn(self): 
        pass 

    def do_turn_relaxed(self): 
        pass 

    def do_turn_in_buffer(self): 
        pass 

    def in_buffer(self): 
        pass 

    def direction_to_point(self, x, y): 
        pass 

    def update_params_post_turn(self): 
        pass 

    def update_pos(self): 
        pass 

    def draw(self): 
        pass 

if __name__ == "__main__":



#creating pygame window (i.e, bounded region) 
(width, height) = (300, 300) 
window = pygame.display.set_mode((width, height)) 

#closing window at user discretion 
running = True 
while running: 
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: 
            running = False 
#pygame.display.flip() 

