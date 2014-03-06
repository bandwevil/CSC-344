import sys
import os
import time

import pygame
import pygame.midi
from pygame.locals import *

try:  # Ensure set available
    set
except NameError:
    from sets import Set as set

scale = [74, 72, 69, 67, 64, 62, 60, 57, 55, 52, 50]

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
        if self.alive:
            self.image = self.on_up
        else:
            self.image = self.off_up
        if (pygame.mouse.get_pressed()[0] == 1 and self.pos.collidepoint(mouse_pos)):
            if (self.down == False):
                self.down = True
                if (self.alive):
                    self.alive = False
                    self.image = self.off_down
                else:
                    self.alive = True
                    self.image = self.on_down
        else:
            self.down = False
    def randomize(self):
        if (random.getrandbits(1) == 1):
            self.image = self.off_up
        else:
            self.image = self.on_up
        

def count_neighbors(grid, x, y):
    sum = 0
    #Super-hackish way to add wrap-around -- Must change if altering size of CA --
    left = (x-1 if x-1 >= 0 else 10)
    down = (y-1 if y-1 >= 0 else 10)
    right = (x+1 if x+1 <= 10 else 0)
    up =    (y+1 if y+1 <= 10 else 0)
    
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
    if button.alive and not button.playing:
        midi.note_on(scale[y], 110, (x % 5))
        button.playing = True
    elif not button.alive and button.playing:
        midi.note_off(scale[y], None, (x % 5))
        button.playing = False

def main_gen(device_id):
    pygame.init()
    pygame.midi.init()
    
    print("Outputting to device #%s" % device_id)
    
    midi_out = pygame.midi.Output(device_id, 0)
    midi_out.set_instrument(2)
    
    screen = pygame.display.set_mode((600, 600))
    background = pygame.Surface(screen.get_size())
    background.fill(Color('slategray'))
    font = pygame.font.Font(os.path.join('data', 'kenvector_future_thin.ttf'), 20)
    background.blit(font.render("test", True, (255, 255, 255)), (400, 10))
    screen.blit(background, (0, 0))
    
    button_off_up   = pygame.image.load(os.path.join('data', 'blue_button06.png')).convert_alpha()
    button_off_down = pygame.image.load(os.path.join('data', 'blue_button07.png')).convert_alpha()
    button_on_up    = pygame.image.load(os.path.join('data', 'blue_button09.png')).convert_alpha()
    button_on_down  = pygame.image.load(os.path.join('data', 'blue_button10.png')).convert_alpha()
    
    playing = False
    
    # Initialize CA cells as well as a future state for updating the CA
    objects = []
    future_state = []
    for x in range(11):
        objects.append([])
        future_state.append([])
        for y in range(11):
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
                        for i in scale:
                            for j in range(5):
                                midi_out.note_off(i, None, j)
                elif event.key == K_c:
                    for l in objects:
                        for o in l:
                            o.alive = False
            
        # Clear the current buttons, calculate the cells' next state
        i = 0
        for l in objects:
            j = 0
            for o in l:
                o.check_mouse(pygame.mouse.get_pos())
                if (playing):
                    future_state[i][j] = update_cells(objects, i, j)
                screen.blit(background, o.pos, o.pos)
                j += 1
            i += 1
        # Redraw tiles, copy new state data over
        i =  0
        for l in objects:
            j = 0
            for o in l:
                if playing:
                    o.alive = future_state[i][j]
                    cell_to_midi(o, i, j, midi_out)
                screen.blit(o.image, o.pos)
                j += 1
            i += 1
        pygame.display.update()
        pygame.time.delay(100)
    
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