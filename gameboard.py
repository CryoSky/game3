from constants import *
from engine_class import data
    
class Board(object):
    """ map board object """
    def __init__(self):
        self.load_map_file("testmap.map")
        self.blocked_squares = []
        self.update_blocked_square_list()
            
    def get_square(self, (x,y)):
        if 0 <= x < self.board_size[0] and 0 <= y < self.board_size[1]:
            square = self.grid[y][x]
            return square            
    
    def get_rect(self):
        width = self.board_size[0] * data.square_size
        height = self.board_size[1] * data.square_size
        return pygame.rect.Rect(0, 0, width, height)
    
    def update_blocked_square_list(self):
        self.blocked = []
        for row in self.grid:
            for square in row:
                if square.blocked:
                    self.blocked_squares.append(square)
                    
    def get_blocked_squares(self):
        blocklist = []
        for row in self.grid:
            for square in row:
                if square.blocked:
                    blocklist.append(square)
        return blocklist
    
    def get_unblocked_squares(self):
        unblocked = []
        for row in self.grid:
            for square in row:
                if square.blocked == False:
                    unblocked.append(square)
        return unblocked
    
    def block_square(self, (x, y)):
        square = self.get_square((x, y))
        square.blocked = True
        
    def get_occupied_squares(self):
        occupied = []
        for row in self.grid:
            for square in row:
                if square.unit:
                    occupied.append(square)
        return occupied
    
    def load_map_file(self, mapfile):
        self.grid = []
        self.blocked_squares = []
        f = open(mapfile)
        y = 0
        for line in f:
            line = line.strip()
            row = []
            x = 0
            for square in line:
                row.append(Square((x,y)))
                x += 1
            self.grid.append(row)
            y += 1
        self.board_size = (x, y)

        y = 0
        f.seek(0)
        for row in f:
            x = 0
            for square in row:
                if square == '#':
                    sq = self.get_square((x,y))
                    sq.blocked = True
                    sq.image = '#'
                elif square == 't':
                    sq = self.get_square((x,y))
                    sq.blocked = True
                    sq.image = 't'
                elif square == '.':
                    sq = self.get_square((x,y))
                    sq.image = '.'
                elif square == 'o':
                    sq = self.get_square((x,y))
                    sq.blocked = True
                    sq.image = 'o'
                x += 1
            y += 1
        f.close()
    
class Square(object):
    """ map square object """
    def __init__(self, xy):
        self.xy = xy
        self.unit = None
        self.blocked = False
        self.path_parent = None
        self.path_g = None
        self.path_h = None
        self.path_f = None
        self.ap_cost = 1
        
    def __str__(self):
        return str(self.xy)
    
    def __getitem__(self, index):
        return self.xy[index]
    
    def get_rect(self):
        left = self.xy[0] * data.square_size + data.camera_offset[0]
        top = self.xy[1] * data.square_size + data.camera_offset[1]
        width = data.square_size
        height = data.square_size
        return pygame.rect.Rect(left, top, width, height)
    
    def get_distance_to_square(self, square):
        x1, y1 = self.xy
        x2, y2 = square.xy
        dist = abs(x1 - x2) + abs(y1 - y2)
        return dist
    
board = Board()