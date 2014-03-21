import sys
import os
import time
import random

import pygame
import pygame.midi
from pygame.locals import *

try:  # Ensure set available
    set
except NameError:
    from sets import Set as set

midi_c3 = 48
note_names = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

#Scales are defined by half steps from the root note
scales =    [[[0, 2, 4, 5, 7, 9, 11, 12, 14, 16], "Major"],
             [[0, 2, 3, 5, 7, 8, 11, 12, 14, 15], "Harmonic Minor"],
             [[0, 3, 5, 7, 10, 12, 15, 17, 19, 22], "Minor Pentatonic"],
             [[0, 2, 4, 7, 9, 12, 14, 16, 19, 21], "Major Pentatonic"]]

#2D List of rules with a tuple for born and stay alive rules, whether to include diagonals, and their names
rules_list = [[(3,),(2, 3), True, "Conway"], [(1, 3), (0, 2, 4), False, "Parity"], [(2,), (), True, "Seeds"]]
 
class Button:
    def __init__(self, image_off_up, image_off_down, image_on_up, image_on_down, pos_x, pos_y):
        self.image = image_off_up
        self.off_up = image_off_up
        self.off_down = image_off_down
        self.on_up = image_on_up
        self.on_down = image_on_down
        self.pos = self.image.get_rect().move(pos_x, pos_y)
        self.down = False
        self.alive = False
        self.playing = False
    
    #Handle image updating if the mouse clicks this cell
    def check_mouse(self, mouse_pos):
        if (pygame.mouse.get_pressed()[0] == 1 and self.pos.collidepoint(mouse_pos)):
            if (self.down == False):
                self.down = True
                if (self.alive):
                    self.alive = False
                    self.image = self.off_down
                else:
                    self.alive = True
                    self.image = self.on_down
        elif (self.down == True):
            self.down = False
            if self.alive:
                self.image = self.on_up
            else:
                self.image = self.off_up
        elif (self.down == False):
            if self.alive:
                self.image = self.on_up
            else:
                self.image = self.off_up
    
    #Randomly set cell to alive or dead
    def randomize(self):
        if (random.getrandbits(1) == 1):
            self.image = self.off_up
        else:
            self.image = self.on_up
        
#Count the number of neighbors a cell has
def count_neighbors(grid, x, y):
    sum = 0
    #hackish way to add wrap-around -- Must change if altering size of CA --
    left = (x-1 if x-1 >= 0 else 9)
    down = (y-1 if y-1 >= 0 else 9)
    right = (x+1 if x+1 <= 9 else 0)
    up =    (y+1 if y+1 <= 9 else 0)
    
    if (diagonals):
        if (grid[left][up].alive):
            sum += 1
        if (grid[right][up].alive):
            sum += 1
        if (grid[left][down].alive):
            sum += 1
        if (grid[right][down].alive):
            sum += 1

    if (grid[x][up].alive):
        sum += 1
    if (grid[left][y].alive):
        sum += 1
    if (grid[right][y].alive):
        sum += 1
    if (grid[x][down].alive):
        sum += 1
    return sum
        
#Given a cell, count its neighbors and return the next state of the cell
def update_cells(current_state, x, y):
    neighbors = count_neighbors(current_state, x, y)
    
    if current_state[x][y].alive and neighbors in stay_rule:
        return True
    elif not current_state[x][y].alive and neighbors in born_rule:
        return True
    else:
        return False

#Triggers MIDI notes based on whether the given cell is alive as well as the current play_probability value
def cell_to_midi(button, x, y, midi):
    if button.alive and not button.playing:
        if random.random() < play_probability:
            midi.note_on(current_root + current_scale[y], 110, ((x + y) % 5))
        #Set playing even if we're not playing so that we can see that we've decided to not play this cell
        button.playing = True
    elif not button.alive and button.playing:
        midi.note_off(current_root + current_scale[y], None, ((x + y) % 5))
        button.playing = False

#Takes alive state from a 2d list of Buttons and saves it to a 2D list of bools
def save_to_list(cells, list):
    i = 0
    for o in cells:
        j = 0
        for l in o:
            list[i][j] = l.alive
            j += 1
        i += 1

#Takes bools from a 2D list and sets a 2D list of Buttons to the values contained
def load_from_list(cells, list):
    i = 0
    for o in cells:
        j = 0
        for l in o:
            l.alive = list[i][j]
            j += 1
        i += 1

#Get the number of milliseconds between beats at a given beats per minute value
def bpm_to_ms(bpm):
    return 60000/bpm
    
#Stop every possible MIDI note for the 5 channels we use
def stop_all_midi(midi_out):
    for i in range(127):
        for j in range(5):
            midi_out.note_off(i, None, j)
            
#Copies alive state from one 2D list of Buttons to another
def copy_obj_state(obj_from, obj_to):
    i = 0
    for o in obj_from:
        j = 0
        for l in o:
            obj_to[i][j].alive = l.alive
            j += 1
        i += 1

def main_gen(device_id):
    pygame.init()
    pygame.midi.init()
    random.seed()
    
    #60 Hz display updating
    frame_update_time = 1000/60
    last_frame_time = 0
    
    current_bpm = 240
    state_update_time = bpm_to_ms(current_bpm)
    last_state_time = 0
    
    print("Outputting to device #%s" % device_id)
    
    midi_out = pygame.midi.Output(device_id, 0)
    midi_out.set_instrument(2)
    
    screen = pygame.display.set_mode((700, 700))
    background = pygame.Surface(screen.get_size())
    background.fill(Color('slategray'))
    font = pygame.font.Font(os.path.join('data', 'kenvector_future.ttf'), 30)
    screen.blit(background, (0, 0))
    
    button_off_up   = pygame.image.load(os.path.join('data', 'blue_button06.png')).convert_alpha()
    button_off_down = pygame.image.load(os.path.join('data', 'blue_button07.png')).convert_alpha()
    button_on_up    = pygame.image.load(os.path.join('data', 'blue_button09.png')).convert_alpha()
    button_on_down  = pygame.image.load(os.path.join('data', 'blue_button10.png')).convert_alpha()
    playing_icon    = pygame.image.load(os.path.join('data', 'shadedDark16.png')).convert_alpha()
    paused_icon     = pygame.image.load(os.path.join('data', 'shadedDark14.png')).convert_alpha()
    arrow_down      = pygame.image.load(os.path.join('data', 'red_sliderDown.png')).convert_alpha()
    arrow_up        = pygame.image.load(os.path.join('data', 'red_sliderUp.png')).convert_alpha()
    
    #Draw loading arrows to screen (un-animated, so we only have to blit them this once)
    screen.blit(arrow_down, (115, 285))
    screen.blit(arrow_up, (150, 285))
    #Collision rectangles for checking if the arrows are clicked
    down_mesh = pygame.Rect(115, 285, 28, 42)
    up_mesh = pygame.Rect(150, 285, 28, 42)
    
    play_pause = paused_icon
    playing = False
    
    #Globals for modifying play parameters
    #Could probably be moved to its own class, but this works without much grossness
    global diagonals
    global born_rule
    global stay_rule
    global current_scale
    global current_root
    global play_probability
    
    #Set up default values
    loop_value = 16
    loop_curr_val = 0
    looping = False
    
    scale_num = 0
    current_scale = scales[scale_num][0]
    current_root = midi_c3
    
    rule_num = 0
    born_rule = rules_list[rule_num][0]
    stay_rule = rules_list[rule_num][1]
    diagonals = rules_list[rule_num][2]
    
    play_probability = 0.2
    
    #Initialize text printouts
    rule_text = font.render("Rule: " + rules_list[rule_num][3], True, (240, 240, 240))
    scale_text = font.render(scales[scale_num][1], True, (240, 240, 240))
    scale_label = font.render("Scale:", True, (240, 240, 240))
    key_text = font.render("Key: " + note_names[current_root - midi_c3], True, (240, 240, 240))
    tempo_text = font.render("Tempo: " + str(current_bpm), True, (240, 240, 240))
    prob_text = font.render("Prob: " + str(play_probability), True, (240, 240, 240))
    loop_label = font.render("Not looping", True, (240, 240, 240))
    loop_text = font.render("Count: " + str(loop_value), True, (240, 240, 240))
    
    # Initialize CA cells as well as a future state for updating the CA
    objects_input = []
    objects_sim = []
    future_state = []
    loop_init = []
    for x in range(10):
        objects_sim.append([])
        objects_input.append([])
        future_state.append([])
        loop_init.append([])
        for y in range(10):
            future_state[x].append(False)
            loop_init[x].append(False)
            o = Button(button_off_up, button_off_down, button_on_up, button_on_down, 10+x*27, 330+y*27)
            objects_sim[x].append(o)
            o = Button(button_off_up, button_off_down, button_on_up, button_on_down, 10+x*27, 10+y*27)
            objects_input[x].append(o)

    # Main loop
    while 1:
        for event in pygame.event.get():
            #Check mouse click on up/down arrows
            if event.type == MOUSEBUTTONDOWN and event.button == 1:
                if down_mesh.collidepoint(event.pos):
                    copy_obj_state(objects_input, objects_sim)
                    save_to_list(objects_input, loop_init)
                elif up_mesh.collidepoint(event.pos):
                    copy_obj_state(objects_sim, objects_input)
            elif event.type == KEYDOWN:
                #Quit pygame
                if event.key == K_ESCAPE:
                    stop_all_midi(midi_out)
                    sys.exit()
                #Toggle between paused and playing
                elif event.key == K_SPACE:
                    playing = not playing
                    
                    if not playing:
                        stop_all_midi(midi_out)
                        play_pause = paused_icon
                    else:
                        play_pause = playing_icon
                        
                #Clear sim (lower) cells
                elif event.key == K_v:
                    stop_all_midi(midi_out)
                    for l in objects_sim:
                        for o in l:
                            o.alive = False
                
                #Clear input (upper) cells
                elif event.key == K_c:
                    for l in objects_input:
                        for o in l:
                            o.alive = False
                            
                #Switch ruleset down
                elif event.key == K_q:
                    rule_num -= 1
                    if rule_num < 0:
                        rule_num = len(rules_list) - 1
                    born_rule = rules_list[rule_num][0]
                    stay_rule = rules_list[rule_num][1]
                    diagonals = rules_list[rule_num][2]
                    rule_text = font.render("Rule: " + rules_list[rule_num][3], True, (240, 240, 240))
                    
                #Switch ruleset up
                elif event.key == K_w:
                    rule_num += 1
                    if rule_num >= len(rules_list):
                        rule_num = 0
                    born_rule = rules_list[rule_num][0]
                    stay_rule = rules_list[rule_num][1]
                    diagonals = rules_list[rule_num][2]
                    rule_text = font.render("Rule: " + rules_list[rule_num][3], True, (240, 240, 240))
                    
                #Switch between scales
                elif event.key == K_a:
                    stop_all_midi(midi_out)
                    scale_num += 1
                    if scale_num >= len(scales):
                        scale_num = 0
                    scale_text = font.render(scales[scale_num][1], True, (240, 240, 240))
                
                #Cycle through keys downwards
                elif event.key == K_s:
                    stop_all_midi(midi_out)
                    
                    if current_root == midi_c3:
                        current_root = midi_c3 + 11
                    else:
                        current_root -= 1
                    key_text = font.render("Key: " + note_names[current_root - midi_c3], True, (240, 240, 240))
                        
                #Cycle through keys upwards
                elif event.key == K_d:
                    stop_all_midi(midi_out)
                    
                    if current_root == midi_c3 + 11:
                        current_root = midi_c3
                    else:
                        current_root += 1
                    key_text = font.render("Key: " + note_names[current_root - midi_c3], True, (240, 240, 240))
                
                #Decrease tempo
                elif event.key == K_z:
                    if current_bpm > 40:
                        current_bpm -= 40
                        state_update_time = bpm_to_ms(current_bpm)
                        tempo_text = font.render("Tempo: " + str(current_bpm), True, (240, 240, 240))
                
                #Increase tempo
                elif event.key == K_x:
                    if current_bpm < 1000:
                        current_bpm += 40
                        state_update_time = bpm_to_ms(current_bpm)
                        tempo_text = font.render("Tempo: " + str(current_bpm), True, (240, 240, 240))
                
                #Decrease probability
                elif event.key == K_f:
                    if play_probability > 0.04:
                        play_probability -= 0.04
                        prob_text = font.render("Prob: " + str(play_probability), True, (240, 240, 240))
                        
                #Increase probability
                elif event.key == K_g:
                    if play_probability < 1:
                        play_probability += 0.04
                        prob_text = font.render("Prob: " + str(play_probability), True, (240, 240, 240))
                        
                #Toggle looping
                elif event.key == K_l:
                    looping = not looping
                    
                    if looping:
                        loop_curr_val = 0
                        loop_label = font.render("Looping", True, (240, 240, 240))
                    else:
                        loop_label = font.render("Not looping", True, (240, 240, 240))
                #Decrease loop size
                elif event.key == K_o:
                    if loop_value > 2:
                        loop_value -= 1
                        loop_text = font.render("Count: " + str(loop_value), True, (240, 240, 240))
                #Increase loop size
                elif event.key == K_p:
                    loop_value += 1
                    loop_text = font.render("Count: " + str(loop_value), True, (240, 240, 240))
                        
        #State update check
        if playing and time.time() * 1000 - last_state_time > state_update_time:
            last_state_time = time.time() * 1000
            
            # Calculate the cells' next state
            i = 0
            for l in objects_sim:
                j = 0
                for o in l:
                    future_state[i][j] = update_cells(objects_sim, i, j)
                    j += 1
                i += 1
            #Copy new state over
            i =  0
            for l in objects_sim:
                j = 0
                for o in l:
                    o.alive = future_state[i][j]
                    cell_to_midi(o, i, j, midi_out)
                    j += 1
                i += 1
            
            #If we're looping, check to see if we need to reset
            if looping:
                loop_curr_val += 1
                if loop_curr_val >= loop_value:
                    loop_curr_val = 0
                    load_from_list(objects_sim, loop_init)
        
        #Frame update check
        if time.time() * 1000 - last_frame_time > frame_update_time:
            last_frame_time = time.time() * 1000
            # Clear current display stuff
            screen.blit(background, (300, 70), pygame.Rect(300, 70, 400, 600))
            for l in objects_sim:
                for o in l:
                    o.check_mouse(pygame.mouse.get_pos())
                    screen.blit(background, o.pos, o.pos)
            for l in objects_input:
                for o in l:
                    o.check_mouse(pygame.mouse.get_pos())
                    screen.blit(background, o.pos, o.pos)
            
            # Redraw updated image
            screen.blit(play_pause, (300, 10))
            screen.blit(rule_text, (300, 70))
            screen.blit(scale_label, (300, 110))
            screen.blit(scale_text, (320, 140))
            screen.blit(key_text, (300, 180))
            screen.blit(tempo_text, (300, 220))
            screen.blit(prob_text, (300, 260))
            screen.blit(loop_label, (300, 310))
            screen.blit(loop_text, (320, 340))
            for l in objects_sim:
                for o in l:
                    screen.blit(o.image, o.pos)
            for l in objects_input:
                for o in l:
                    screen.blit(o.image, o.pos)
            pygame.display.update()

#Scan current MIDI devices, print out their information
def print_device_info():
    pygame.midi.init()
    for i in range( pygame.midi.get_count() ):
        r = pygame.midi.get_device_info(i)
        (interf, name, input, output, opened) = r

        in_out = ""
        if input:
            in_out = "(input)"
        if output:
            in_out = "(output)"

        print ("%2i: interface :%s:, name :%s:, opened :%s:  %s" %
               (i, interf, name, opened, in_out))
    pygame.midi.quit()

#Print out possible command line flags
def print_usage():
    print("Usage:")
    print("-o [device_id] - main program, define MIDI output device")
    print("-l             - list current MIDI devices")

if __name__ == "__main__":
    if "-o" in sys.argv:
        try:
            dev_id = int(sys.argv[-1])
        except: #default to device 1 (Windows MIDI device)
            dev_id = 1
        main_gen(dev_id)
    elif "-l" in sys.argv:
        print_device_info()
    else:
        print_usage()