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
        else:
            if (self.alive):
                self.image = self.on_up
            else:
                self.image = self.off_up
            self.down = False
    def randomize(self):
        if (random.getrandbits(1) == 1):
            self.image = self.off_up
        else:
            self.image = self.on_up
        
    
def main_gen(device_id):
    pygame.init()
    pygame.midi.init()
    random.seed()
    
    print("Outputting to device #%s" % device_id)
    
    midi_out = pygame.midi.Output(device_id, 0)
    midi_out.set_instrument(2)
    
    screen = pygame.display.set_mode((600, 600))
    background = pygame.Surface(screen.get_size())
    background.fill(Color('slategray'))
    button_off_up   = pygame.image.load(os.path.join('data', 'blue_button06.png')).convert_alpha()
    button_off_down = pygame.image.load(os.path.join('data', 'blue_button07.png')).convert_alpha()
    button_on_up    = pygame.image.load(os.path.join('data', 'blue_button09.png')).convert_alpha()
    button_on_down  = pygame.image.load(os.path.join('data', 'blue_button10.png')).convert_alpha()
    screen.blit(background, (0, 0))
    
    # Initialize CA cells
    objects = []
    for x in range(10):
        objects.append([])
        for y in range(10):
            o = Button(button_off_up, button_off_down, button_on_up, button_on_down, 10+x*27, 10+y*27)
            objects[x].append(o)

    # Main loop
    while 1:
        for event in pygame.event.get():
            if event.type in (QUIT, KEYDOWN):
                sys.exit()
                
        # Update each tile, clearing its current display
        for l in objects:
            for o in l:
                o.check_mouse(pygame.mouse.get_pos())
                screen.blit(background, o.pos, o.pos)
        # Redraw tiles
        for l in objects:
            for o in l:
                screen.blit(o.image, o.pos)
        pygame.display.update()
        pygame.time.delay(100)
    
    midi_out.note_on(55, 127)
    time.sleep(.167)
    midi_out.note_off(55)
    
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
    print("-o [device_id] - main usage, define MIDI output device")
    print("-l             - list current MIDI devices")

if __name__ == "__main__":
    if "-o" in sys.argv:
        try:
            dev_id = int(sys.argv[-1])
        except: #default to device 3 (default MIDI loopback on my system)
            dev_id = 1
        main_gen(dev_id)
    elif "-l" in sys.argv:
        print_device_info()
    else:
        print_usage()