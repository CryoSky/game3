import pygame
import constants
from constants import *

ZOOM_FACTOR = 8

class Data(object):
    def __init__(self):
        self.draw_square_lines = False
        self.draw_square_numbers = False
        self.focus = "normal"
        self.display_size = (1280, 800)
        self.base_square_size = 64
        self.square_size = 64
        self.base_unit_size = 32
        self.unit_size = 32
        self.zoom = 100
        self.pathfinding_route = []
        self.debug = True
        
    def get_display_rect(self):
        return pygame.rect.Rect((0, 0), self.display_size)
    
    def zoom_out(self):
        if self.square_size >= 18:
            self.square_size -= 2
            self.unit_size -= 1
        self.zoom = (self.square_size * 100) / (self.base_square_size)
    
    def zoom_in(self):
        if self.square_size < 256:
            self.square_size += 2
            self.unit_size += 1
        self.zoom = (self.square_size * 100) / (self.base_square_size)
        
    def new_turn(self):
        for unit in unitlist:
            unit.new_turn()
        

data = Data()

from graphics_class import Graphics
from interface_class import Interface
from gameboard import board
from pathfinding import astar
from unit_class import unitlist

data.selected_square = board.get_square((0, 0))
data.astar = astar

graphics = Graphics()
interface = Interface()
data.interface = interface
data.graphics = graphics

# Quick access to some debug variables, cut this out later
interface.debug_window.visible = False
data.debug = False

class Engine(object):
    
    def __init__(self):
        self.clock = pygame.time.Clock()
    
    def run(self):
        self.clock.tick()
        data.fps = self.clock.get_fps()
        if data.astar.run:
            data.astar.run_pathfinding()
        graphics.draw()
        interface.run()
        for unit in unitlist:
            if unit.move_dest != None:
                unit.update()

