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
import random
import math 

#some globals 

#Window parameters -- for simulation ease, we eventually want to set these parameters using CLI  

FRAME_RATE = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 100
WINDOW_BUFFER = 100
MICE_NUMBER = 2

#Defaul mouse behavior 

MOUSE_BEHAVIOR = dict(
        SPEED_MIN = 0
        SPEED_MAX =70
        SPEED_CHANGE_MIN = 0
        SPEED_CHANGE_MAX = 40
        ACCELERATION_MIN =10
        ACCELERATION_MAX = 100
        TURN_ANGLE_MIN = 0.1*math.pi
        TURN_ANGLE_MAX = 0..8*math.pi
        TURN_SPEED_MIN = 1*math.pi
        TURN_SPEED_MAX = 3*math.pi
        TURN_TIME_MIN = 0.3
        TURN_TIME_MAX = 0.6
        TURN_ANGLE_TOLERANCE_BUFFER = 0.2*math.pi
        COLOR = (108, 110, 107)
        RADIUS = 10
) 

#We could include here a set of parameters for panic mode. That is, how will a mouse behave when it 
#percieves a threat? Right now, all mice will more or less be the same size. Perhaps it's the case that
#smaller mice pereive threats from larger mice who enter a "aggressive mode" and, subsequently, enter a 
#"panic mode"... 


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
    def __init__(self, mouse_behavior):
        #general 
        self.speed_min = mouse_behavior["SPEED_MIN"] #min move speed of mouse (px/s)
        self.speed_max = mouse_behavior["SPEED_MAX"] #max move speed of mouse (px/s) 
        self.speed_change_min = mouse_behavior["SPEED_CHANGE_MIN"] #min speed change from start to end of turn (px/s) 
        self.speed_change_max = mouse_behavior["SPEED_CHANGE_MAX"] #max speed change from start to end of turn (px/s) 
        self.acceleration_min = mouse_behavior["ACCELERATION_MIN"] #min acceleration when changing speed (px/s^2)
        self.acceleration_max = mouse_behavior["ACCELERATION_MAX"] #max acceleration when changing speed (px/s^2) 
        self.turn_angle_min =  mouse_behavior["TURN_ANGLE_MIN"] #min dir change during turn (rad) 
        self.turn_angle_max = mouse_behavior["TURN_ANGLE_MAX"] #max dir change during turn (rad) 
        self._turn_speed_min = mouse_behavior["TURN_SPEED_MIN"] #min angular velocity of dir change (rad/s) 
        self.turn_speed_max = mouse_behavior["TURN_SPEED_MAX"] #max angular velocity of dir change (rad/s) 
        self.turn_time_min = mouse_behavior["TURN_TIME_MIN"] #min time to next turn (s) 
        self.turn_time_max = mouse_behavior["TURN_TIME_MAX"] #max time to next turn (s) 
        self.turn_angle_to_tolerance_buffer = mouse_behavior["TURN_ANGLE_TOLERANCE_BUFFER"] #allowed dir dif to center of 
        #window during return from buffer zone 
        self.color = mouse_behavior["COLOR"] #mouse color 
        self.radius = mouse_behavior["RADIUS"] #radius of circle that represents mouse 
        

        #state specific 
        self.speed_current = None #current speed of mouse (px/s) 
        self.speed_end_of_turn = None #target speed at end of curr turn (px/s) 
        self.acceleration = None #accleration for current turn (px/s^2) 
        self.speed_change_per_frame = None #change in speed per fram --> self.acceleration/FRAME_RATE (px/s) 
        self.direction_current = None #current move direction of mouse (rad)
        self.direction_end_of_turn = None #target move direction of mouse at end of turn (rad) 
        self.turn_speed = None #angular velocity for current turn (rad/s) 
        self.turn_time = None #duration of current turn 
        self.direction_change_per_frame = None #dir change per fram --> self.turn_speex/FRAME_RATE [rad] 
        self.position_horizontal = None #current horizontal position
        self.position_vertical = None #current vertical position
        self.frame_number_current = None #frames elapsed since start of current turn 
        self.is_accelearting = None #is true if mouse's speed is increased during current turn 
        self.is_turning_clockwise = None #is true if mouse is turning clockwise in current turn 

        #setting initial conditions for mosue 
        self.set_initial_state() #sets mouse's intiial state
        self.do_turn() #defines mouse's first turn 
        pass 

    def set_initial_state(self):
        self.speed_current = rand.uniform(self.speed_min, self.speed_max)
        self.direction_current = random.uniform(-math.pi, math.pi) 
        self.position_horizontal = random.uniform(WINDOW_BUFFER, WINDOW_WIDTH - WINDOW_BUFFER) 
        self.position_vertical = random.uniform(WINDOW_BUFFER, WINDOW_HEIGHT - WINDOW_BUFFER) 
        pass 

    def do_turn(self): 
        if self.in_buffer():
            self.do_turn_in_buffer()
        else: 
            self.do_turn_relaxed() 

        self.edit_parameters_after_doing_turn() #updating after turn 
        pass 

    def do_turn_relaxed(self): 
        #randomly increase/decrease speed 
        self.speed_end_of_turn = self.speed_current + random.choise([1,-1])*random.uniform(self.speed_change_min,\
                self.speed_change_max)

        if self.speed_end_of_turn > self.speed_max: 
            self.speed_end_of_turn = self.speed_max 
        if self.speed_end_of_turn < self.speed_min: 
            self.speed_end_of_turn = self.speed_min 

        #randomly change direction 
        self.direction_end_of_turn = self.direction_current + random.choice([1,-1])*random.uniform(self.turn_angle_min,\
                self.turn_angle_max)
        self.acceleration = random.uniform(self.acceleration_min, self.acceleration_max) 
        self.turn_speed = random.uniform(self.turn_speed_min, self.turn_speed_max) 
        self.turn_time = random_uniform(self.turn_time_min, self.turn_time_max) 
        pass 

    def do_turn_in_buffer(self): 
        self.speed_end_of_turn = self.speed_max 
        self.direction_end_of_turn = self.direction_to_point(HOUSE_WIDTH/2, HOUSE_HEIGHT/2) + random.uniform(\
                -self.turn_angle_tolerance_buffer, self.turn_angle_tolerance_buffer)
        self.acceleration = self.acceleration_max
        self.turn_speed = self.turn_speed_max
        self.turn_time = self.turn_time_max 
        pass 

    def in_buffer(self): 
        if (self.position_horizontal < WINDOW_BUFFER or self.psoition_horizontal > WINDOW_WIDTH - WINDOW_BUFFER or \
                self.position_vertical < WINDOW_BUFFER or self.position_vertical > WINDOW_HEIGHT - WINDOW_BUFFER:
            return True 
        else: 
            return False 
        pass 

    def direction_to_point(self, x, y):
        direction = math.atan2(-self.position_vertical + y, -self.position_horizontal + x) 
        return direction 
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

