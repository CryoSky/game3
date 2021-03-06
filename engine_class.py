import pygame, time
import constants
from constants import *

ZOOM_FACTOR = 8

class DamageResult():
    def __init__(self, attacker, defender, num):
        self.attacker = attacker
        self.defender = defender
        self.num = num
        self.float = 0
        self.start_time = time.time()
        self.timer = 2
        
    def __str__(self):
        return str(self.attacker) + ", " + str(self.defender) + ", " + str(self.num)

class Data(object):
    def __init__(self):
        self.draw_square_lines = False
        self.draw_square_numbers = False
        self.focus = "normal"
        self.display_size = (1024, 768)
        self.base_square_size = 64
        self.square_size = 64
        self.base_unit_size = 32
        self.unit_size = 32
        self.zoom = 100
        self.zoom_step = 4
        self.pathfinding_route = []
        self.debug = True
        self.damage = []
        self.factions = []
        self.turn_num = 1
        self.turn = []
        
    def create_damage_result(self, attacker, defender, num):
        self.damage.append(DamageResult(attacker, defender, num))
        
    def get_display_rect(self):
        return pygame.rect.Rect((0, 0), self.display_size)
        
    def new_turn(self):
        data.turn_num += 1
        for unit in unitlist:
            unit.new_turn()       
            
    def end_turn(self):
        print self.factions
        cur_ind = self.factions.index(data.turn)
        if cur_ind >= len(self.factions) - 1:
            ind = 0
            self.new_turn()
        else:
            ind = cur_ind + 1
        self.turn = self.factions[ind]
                    
    def adjust_for_zoom(self, number):
        return (number * self.zoom) / 100
        

data = Data()
from graphics_class import Graphics
from interface_class import Interface
from gameboard import board
from pathfinding import astar
from unit_class import unitlist
from items import itemlist

data.itemlist = itemlist
data.turn = data.factions[0]

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
            unit.update()


