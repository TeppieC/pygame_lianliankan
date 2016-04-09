import pygame
#from pygame import Surface
#from gui import GUI

pygame.init()

TILE_SIZE = 45

class Tile():
    def __init__(self, input_x, input_y, input_num):
        self.x = input_x
        self.y = input_y
        self.index_x = (self.x)//TILE_SIZE
        self.index_y = (self.y-60)//TILE_SIZE
        self.x_center = self.x + 22
        self.y_center = self.y + 22

        self.prev = None

        # num-attribute
        # 1-25 for pictures, 26 for black tiles and not available tiles
        self.num = input_num
        
    def __repr__(self):
        return "Tile(%s, %s, %s)" %(str(self.index_x), str(self.index_y), str(self.num))

    def __eq__(self, pic2):
        return (self.index_x == pic2.index_x\
                    and self.index_y == pic2.index_y\
                    and self.num == pic2.num)
    
    def __hash__(self):
        return id(self)

    def is_active(self):
        '''
        Check if the tile is active.
        Return True if it is active
        '''

        if self.num != 26:
            return True
        else:
            return False

    def eliminate_for_tile(self):
        '''
        Change the tile status to unactive
        '''

        self.num = 26

   
        
