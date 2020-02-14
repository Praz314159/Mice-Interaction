'''
This is meant to be a model of two mice interacting in a bounded region. There are a few goals for this the progression of this project: 
    1. Visualize two or more mice moving in a bounded region (smoothly dealing with boundary conditions) 
    2. Realistically modelling the movement of mice, with built in randomness
    3. Realistically modelling the interaction between two mice, again with built in randomness
    4. Capturing information on a frame by frame basis about what area in the bounded region each mouse occupies

Review of methods architecture: 
    We have a window class and a mouse class. The window is the bounded region in which the mice move. Window has the following
    methods: 

    1. init()
    2. create_mice()
    3. update_mice_movement()
    4. draw() 

    And mouse has the following methods: 

    1. init()
    2. set_initial_state()
    3. do_turn()
    4. do_turn_relaxed()
    5. do_turn_in_buffer()
    6. in_buffer()
    7. direction_to_point()
    8. edit_parameters_after_doing_turn()
    9. update_position()
    10. draw() 

    There are some problems that this architecture has with respect to our end goals, however. Right now, the model is such that
    multiple mice will move randomly and independently within the window. There is no structure intereaction between the mice 
    that maps onto real mouse behavior. Next, we want to define a few modes of interaction: 

    1. Aggression --> in this case, we have one agressor and one victim
    2. Curiosity --> both mice are mutually exploring each other 
    3. Dominance --> one mouse is asserting its dominance over the other, we therefore have one dominant and one subbordinate mouse

    We also have not stored the regions of the window occupied by each mouse in each frame. This is a simple matter though. 
    Finally, there should be a more realistic physiological modelling of the mice. Right now, mice are just circles moving 
    in a particular manner. We want them to be at least a body and a head... 


''' 

import pygame
import random
import math 

#some globals 

#Window parameters -- for simulation ease, we eventually want to set these parameters using CLI  

FRAME_RATE = 30
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
WINDOW_BUFFER = 100
MICE_NUMBER = 2
WINDOW_BORDER_WIDTH = 5 

#Defaul mouse behavior 

MOUSE_BEHAVIOR = dict(
        SPEED_MIN = 0,
        SPEED_MAX = 70,
        SPEED_CHANGE_MIN = 0,
        SPEED_CHANGE_MAX = 40,
        ACCELERATION_MIN =10,
        ACCELERATION_MAX = 100,
        TURN_ANGLE_MIN = 0.1*math.pi,
        TURN_ANGLE_MAX = 0.8*math.pi,
        TURN_SPEED_MIN = 1*math.pi,
        TURN_SPEED_MAX = 3*math.pi,
        TURN_TIME_MIN = 0.3,
        TURN_TIME_MAX = 0.6,
        TURN_ANGLE_TOLERANCE_BUFFER = 0.2*math.pi,
        COLOR = (108, 110, 107),
        RADIUS = 10
) 

#We could include here a set of parameters for panic mode. That is, how will a mouse behave when it 
#percieves a threat? Right now, all mice will more or less be the same size. Perhaps it's the case that
#smaller mice pereive threats from larger mice who enter a "aggressive mode" and, subsequently, enter a 
#"panic mode"... 


class Window:

    mice = None 

    def __init__(self, mouse_behavior):
        self.frame_rate = FRAME_RATE 
        self.size_horizontal = WINDOW_WIDTH
        self.size_vertical = WINDOW_HEIGHT 
        self.size_buffer = WINDOW_BUFFER 
        self.line_width_border = WINDOW_BORDER_WIDTH 
        self.mice_number = MICE_NUMBER 

        Window.mice = []
        self.program_window = pygame.display.set_mode((self.size_horizontal, self.size_vertical)) 
        self.clock = pygame.time.Clock()

        self.create_mice(mouse_behavior) 
         

    def create_mice(self, mouse_behavior):
        for i in range(self.mice_number):
            Window.mice.append(Mouse(mouse_behavior)) 

        Window.mice[0].color = (75, 139, 190) 
        

    def update_mice_movement(self): 
        for mouse in Window.mice:
            mouse.update_pos()
            if mouse.frame_number_current >= mouse.frame_number_end_of_turn:
                mouse.do_turn()

        self.clock.tick(FRAME_RATE) 
         

    def draw(self):
        #pygame.draw.rect(self.program_window, self.size_buffer, self. --> working this kink 
        for mouse in Window.mice:
            mouse.draw()
        pygame.display.flip() 
         

class Mouse: 
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
        self.turn_speed_min = mouse_behavior["TURN_SPEED_MIN"] #min angular velocity of dir change (rad/s) 
        self.turn_speed_max = mouse_behavior["TURN_SPEED_MAX"] #max angular velocity of dir change (rad/s) 
        self.turn_time_min = mouse_behavior["TURN_TIME_MIN"] #min time to next turn (s) 
        self.turn_time_max = mouse_behavior["TURN_TIME_MAX"] #max time to next turn (s) 
        self.turn_angle_tolerance_buffer = mouse_behavior["TURN_ANGLE_TOLERANCE_BUFFER"] #allowed dir dif to center of 
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
        self.speed_current = random.uniform(self.speed_min, self.speed_max)
        self.direction_current = random.uniform(-math.pi, math.pi) 
        self.position_horizontal = random.uniform(WINDOW_BUFFER, WINDOW_WIDTH - WINDOW_BUFFER) 
        self.position_vertical = random.uniform(WINDOW_BUFFER, WINDOW_HEIGHT - WINDOW_BUFFER) 
        pass 

    def do_turn(self): 
        if self.in_buffer():
            self.do_turn_in_buffer()
        else: 
            self.do_turn_relaxed() 

        self.update_params_post_turn() #updating after turn 
        pass 

    def do_turn_relaxed(self): 
        #randomly increase/decrease speed 
        self.speed_end_of_turn = self.speed_current + random.choice([1,-1])*random.uniform(self.speed_change_min,\
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
        self.turn_time = random.uniform(self.turn_time_min, self.turn_time_max) 
        pass 

    def do_turn_in_buffer(self): 
        self.speed_end_of_turn = self.speed_max 
        self.direction_end_of_turn = self.direction_to_point(WINDOW_WIDTH/2, WINDOW_HEIGHT/2) + random.uniform(\
                -self.turn_angle_tolerance_buffer, self.turn_angle_tolerance_buffer)
        self.acceleration = self.acceleration_max
        self.turn_speed = self.turn_speed_max
        self.turn_time = self.turn_time_max 
        pass 

    def in_buffer(self): 
        if self.position_horizontal < WINDOW_BUFFER or self.position_horizontal > WINDOW_WIDTH - WINDOW_BUFFER or \
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
        self.direction_current = math.remainder(self.direction_current, 2*math.pi)
        self.direction_end_of_turn = math.remainder(self.direction_end_of_turn, 2*math.pi) 

        if self.speed_current < self.speed_end_of_turn: 
            self.is_accelerating = True 
        else: 
            self.is_accelerating = False 

        if math.remainder(self.direction_current - self.direction_end_of_turn, 2*math.pi) < 0: 
            self.is_turning_clockwise = True 
        else: 
            self.is_turning_clockwsie = False 

        self.speed_change_per_frame = self.acceleration/FRAME_RATE
        self.direction_change_per_frame = self.turn_speed/FRAME_RATE 
        self.frame_number_end_of_turn = self.turn_time*FRAME_RATE 
        self.frame_number_current = 0
        pass 

    def update_pos(self):
        if self.is_accelerating and self.speed_current < self.speed_end_of_turn: 
            self.speed_current += self.speed_change_per_frame
        elif not self.is_accelerating and self.speed_current > self.speed_end_of_turn: 
            self.speed_current -= self.speed_change_per_frame 

        if self.is_turning_clockwise: 
            if self.direction_end_of_turn > 0 and self.direction_current < self.direction_end_of_turn: 
                self.direction_current += self.direction_change_per_frame
            elif self.direction_end_of_turn < 0 and self.direction_current < self.direction_end_of_turn + math.pi*(\
                    abs(self.direction_current) + self.direction_current)/abs(self.direction_current): 
                self.direction_current += self.direction_change_per_frame 

        else: 
            if self.direction_end_of_turn < 0 and self.direction_current > self.direction_end_of_turn: 
                self.direction_current -= self.direction_change_per_frame 
            elif self.direction_end_of_turn > 0 and self.direction_current > self.direction_end_of_turn - \
                    math.pi * (abs(self.direction_current)-self.direction_current)/abs(self.direction_current): 
                self.direction_current -= self.direction_change_per_frame 

        #update horizontal pos
        self.position_horizontal += math.cos(self.direction_current)*self.speed_current/FRAME_RATE
        #update vertical pos 
        self.position_vertical += math.sin(self.direction_current)*self.speed_current/FRAME_RATE
        #increment frame count 
        self.frame_number_current += 1 
        pass 

    def draw(self): 
        pygame.draw.circle(window.program_window, self.color, (round(self.position_horizontal), round(self.position_vertical)), self.radius, 0)

if __name__ == "__main__":
    pygame.init()
    window = Window(MOUSE_BEHAVIOR)
    running = True 
    while running: 
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
        window.update_mice_movement()
        window.draw() 


