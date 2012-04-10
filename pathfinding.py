from engine_class import data
from gameboard import board
import time, pygame, copy

class AStar():
    def __init__(self):
        self.take_step = False
        self.open = []
    
    def start_pathfinding(self, start, goal=board.get_square((6,1))):
        data.draw_square_numbers = False
        self.reset_pathfinding()
        self.take_step = True
        data.pathfinding_route = []
        self.start = start
        self.goal = goal
        self.open = [start]
        self.closed = copy.copy(board.blocked_squares)
        self.step = 0
        self.square = self.start
        print "start -------- " + str(self.start)
        
    def run_pathfinding(self):
        if self.take_step and len(self.open) > 0:
            data.pathfinding_route.append(self.square)
            self.step += 1
            print "step: " + str(self.step) + "  square: " + str(self.square)
            self.square = self.process_node(self.square)
            if self.square == self.goal:
                print "GOAL REACHED"
            self.take_step = False
        if self.take_step and len(self.open) < 1:
            print "open list is empty."
        
        
    def process_node(self,current):
        self.open.remove(current)
        self.closed.append(current)
        for neighbor in self.get_adjacent_squares(current):
            if neighbor not in self.closed:
                if neighbor not in self.open:
                    self.open.append(neighbor)
                    neighbor.path_parent = current
                    neighbor.path_h = self.get_h_score(neighbor)
                    neighbor.path_g = self.get_g_score(neighbor)
                    neighbor.path_f = self.get_f_score(neighbor)
                elif neighbor in self.open:
                    new_g = self.get_g_score(current) + self.get_square_to_square_dist(current, neighbor)
                    if new_g < neighbor.path_g:
                        neighbor.path_parent = current
                        neighbor.path_g = self.get_g_score(neighbor)
                        neighbor.path_f = self.get_f_score(neighbor)
                print "candidate: " + str(neighbor) + " F-Score: " + str(neighbor.path_f)
        choice = self.get_lowest_f_score_square()
        print "Choice: " + str(choice)
        print "-----------"
        return choice
    
    def reset_pathfinding(self):
        self.open = []
        self.closed = []
        self.start = None
        self.goal = None
        self.step = 0
        for row in board.grid:
            for square in row:
                square.path_h = None
                square.path_f = None
                square.path_g = None
                square.path_parent = None
        
    def get_adjacent_squares(self, square):
        x,y = square.xy
        north = board.get_square((x,y-1))
        east = board.get_square((x+1, y))
        south = board.get_square((x, y+1))
        west = board.get_square((x-1, y))
        results = []
        for sq in [north, east, south, west]:
            if sq != None:
                results.append(sq)
        return results
    
    def get_square_to_square_dist(self, square1, square2):
        x1, y1 = square1.xy
        x2, y2 = square2.xy
        dist = abs(x1 - x2)
        dist += abs(y1 - y2)
        return dist
    
    def get_h_score(self, square):
        return self.get_square_to_square_dist(square, self.goal)
    
    def get_g_score(self, square):
        score = 0
        if square.path_parent != None:
            score += self.get_square_to_square_dist(square, square.path_parent)
        return score
    
    def get_f_score(self, square):
        return square.path_g + square.path_h
    
    def get_lowest_f_score_square(self):
        f_list = []
        for square in self.open:
            f_list.append([square.path_f, square])
        f_list.sort()
        return f_list[0][1]
    
    def get_route(self):
        route = []
        square = self.goal
        while square.path_parent != None:
            route.insert(0,square)
            square = square.path_parent
        return route
        
            
  
astar = AStar()
