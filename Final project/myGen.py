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
note_names = ["C", "Db", "D", "Eb", "F", "F#", "G", "Ab", "A", "Bb", "B"]

#Scales are defined by half steps from the root note
scale_major =       [0, 2, 4, 5, 7, 9, 11, 12, 14, 16]
scale_harm_minor =  [0, 2, 3, 5, 7, 8, 11, 12, 14, 15]
scale_min_pent =    [0, 3, 5, 7, 10, 12, 15, 17, 19, 22]
scale_maj_pent =    [0, 2, 4, 7, 9, 12, 14, 16, 19, 21]

play_probability = 0.2

diagonals = False
born_rule = (1, 3)
stay_rule = (0, 2, 4)
    
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
    def randomize(self):
        if (random.getrandbits(1) == 1):
            self.image = self.off_up
        else:
            self.image = self.on_up
        

def count_neighbors(grid, x, y):
    sum = 0
    #Super-hackish way to add wrap-around -- Must change if altering size of CA --
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
        
def update_cells(current_state, x, y):
    neighbors = count_neighbors(current_state, x, y)
    
    if current_state[x][y].alive and neighbors in stay_rule:
        return True
    elif not current_state[x][y].alive and neighbors in born_rule:
        return True
    else:
        return False
    
def cell_to_midi(button, x, y, midi):
    if button.alive and not button.playing and random.random() < play_probability:
        midi.note_on(scale[y], 110, ((x + y) % 5))
        button.playing = True
    elif not button.alive and button.playing:
        midi.note_off(scale[y], None, ((x + y) % 5))
        button.playing = False
        
def save_to_list(cells, list):
    i = 0
    for o in cells:
        j = 0
        for l in o:
            list[i][j] = l.alive
            j += 1
        i += 1
        
def load_from_list(cells, list):
    i = 0
    for o in cells:
        j = 0
        for l in o:
            l.alive = list[i][j]
            j += 1
        i += 1

def main_gen(device_id):
    pygame.init()
    pygame.midi.init()
    random.seed()
    
    #60 Hz display updating
    frame_update_time = 1000/60
    state_update_time = 300
    last_frame_time = 0
    last_state_time = 0
    
    print("Outputting to device #%s" % device_id)
    
    midi_out = pygame.midi.Output(device_id, 0)
    midi_out.set_instrument(2)
    
    screen = pygame.display.set_mode((500, 297))
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
    
    play_pause = paused_icon
    playing = False
    
    rule_text = font.render("Parity", True, (255, 255, 255))
    
    global diagonals
    global born_rule
    global stay_rule
    
    #Array for saving/loading states on the fly
    save_array = []
    for i in range(10):
        save_array.append([])
        for j in range(10):
            save_array[i].append([])
            for k in range(10):
                save_array[i][j].append(False)
                
    # Initialize CA cells as well as a future state for updating the CA
    objects = []
    future_state = []
    for x in range(10):
        objects.append([])
        future_state.append([])
        for y in range(10):
            future_state[x].append(False)
            o = Button(button_off_up, button_off_down, button_on_up, button_on_down, 10+x*27, 10+y*27)
            objects[x].append(o)

    # Main loop
    while 1:
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.midi.quit()
                    sys.exit()
                elif event.key == K_SPACE:
                    playing = not playing
                    
                    # Mute current sounds
                    if not playing:
                        play_pause = paused_icon
                        for i in scale:
                            for j in range(5):
                                midi_out.note_off(i, None, j)
                    else:
                        play_pause = playing_icon
                #Clear current cells
                elif event.key == K_c:
                    for l in objects:
                        for o in l:
                            o.alive = False
                elif event.key == K_q:
                    rule_text = font.render("Conway", True, (240, 240, 240))
                    diagonals = True
                    born_rule = (3,)
                    stay_rule = (2, 3)
                elif event.key == K_w:
                    rule_text = font.render("Parity", True, (240, 240, 240))
                    diagonals = False
                    born_rule = (1, 3)
                    stay_rule = (0, 2, 4)
                #Who cares about readability?
                elif event.key == K_1:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[1])
                    else:
                        load_from_list(objects, save_array[1])
                elif event.key == K_2:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[2])
                    else:
                        load_from_list(objects, save_array[2])
                elif event.key == K_3:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[3])
                    else:
                        load_from_list(objects, save_array[3])
                elif event.key == K_4:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[4])
                    else:
                        load_from_list(objects, save_array[4])
                elif event.key == K_5:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[5])
                    else:
                        load_from_list(objects, save_array[5])
                elif event.key == K_6:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[6])
                    else:
                        load_from_list(objects, save_array[6])
                elif event.key == K_7:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[7])
                    else:
                        load_from_list(objects, save_array[7])
                elif event.key == K_8:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[8])
                    else:
                        load_from_list(objects, save_array[8])
                elif event.key == K_9:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[9])
                    else:
                        load_from_list(objects, save_array[9])
                elif event.key == K_0:
                    if event.mod & KMOD_LSHIFT != 0:
                        save_to_list(objects, save_array[0])
                    else:
                        load_from_list(objects, save_array[0])
                    
        
        if time.time() * 1000 - last_state_time > state_update_time:
            last_state_time = time.time() * 1000
            # Calculate the cells' next state
            i = 0
            for l in objects:
                j = 0
                for o in l:
                    if (playing):
                        future_state[i][j] = update_cells(objects, i, j)
                    j += 1
                i += 1
            #Copy new state over
            i =  0
            for l in objects:
                j = 0
                for o in l:
                    if playing:
                        o.alive = future_state[i][j]
                        cell_to_midi(o, i, j, midi_out)
                    j += 1
                i += 1
            
        if time.time() * 1000 - last_frame_time > frame_update_time:
            last_frame_time = time.time() * 1000
            # Clear current display stuff
            screen.blit(background, (300, 70), pygame.Rect(300, 70, 200, 50))
            for l in objects:
                for o in l:
                    o.check_mouse(pygame.mouse.get_pos())
                    screen.blit(background, o.pos, o.pos)
            # Redraw tiles
            for l in objects:
                screen.blit(play_pause, (300, 10))
                screen.blit(rule_text, (300, 70))
                for o in l:
                    screen.blit(o.image, o.pos)
            pygame.display.update()
    
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