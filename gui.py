import sys, pygame, random
import asset
from pygame import Surface
from pygame import time
from tile import Tile
pygame.init()

TILE_SIZE = 45

SURFACE_WIDTH = 990 # 22*45
SURFACE_HEIGHT = 675 # 15*45

NUM_TILES_HOR = SURFACE_WIDTH/TILE_SIZE
NUM_TILES_VER = SURFACE_HEIGHT/TILE_SIZE
# 330 tiles (including blank tiles)
# 16*10 available tiles/ 80 pairs

TIMER_WIDTH = 720
SCORE_WIDTH = 200
TIMER_HEIGHT = 60

PUP_HEIGHT = 50
PUP_HINT_WIDTH = 150
PUP_TIME_WIDTH = 150

RECT_SCORE_BOARD = pygame.Rect(SURFACE_WIDTH-SCORE_WIDTH, 30,
                               SCORE_WIDTH, TIMER_HEIGHT)

RECT_TIME_TOTAL = pygame.Rect(20, 30,
                             TIMER_WIDTH, TIMER_HEIGHT-25)

RECT_SURFACE_TILES = pygame.Rect(0, TIMER_HEIGHT,
                                 SURFACE_WIDTH, SURFACE_HEIGHT)

RECT_PUP_HINT = pygame.Rect(50, SURFACE_HEIGHT+TIMER_HEIGHT,
                        PUP_HINT_WIDTH, PUP_HEIGHT)
RECT_PUP_TIME = pygame.Rect(250, SURFACE_HEIGHT+TIMER_HEIGHT,
                            PUP_TIME_WIDTH, PUP_HEIGHT)
RECT_PUP_SHUF = pygame.Rect(450, SURFACE_HEIGHT+TIMER_HEIGHT,
                            PUP_TIME_WIDTH, PUP_HEIGHT)
RECT_NOTICE = pygame.Rect(150, 100, 800, 35)

pygame.font.init()
FONT_SIZE = 30
FONT = pygame.font.SysFont("Mono", FONT_SIZE, True)
PUP_FONT_SIZE = 20
PUP_FONT = pygame.font.SysFont("Arial", PUP_FONT_SIZE, True)

def rnd_pairs(total_num, num_pairs):
    '''
    Return a randomized list of non-negative integer numbers
    which are less than or equal to total_num. For each different
    number, number of the numbers should be even.

    Args:
    total_num(int): number of kinds of pictures
    num_pairs(int): number of picture pairs to be displayed in the game
 
    Return
    (list): list of numbers, # of each number should be even
    '''

    list_nums = list()
    # for each kind of pictures
    for i in range(0, num_pairs):
        rnd_num = random.randint(0, total_num)
        list_nums.append(rnd_num)
        list_nums.append(rnd_num)

    random.shuffle(list_nums)
    return list_nums


class GUI(pygame.Surface):

    def __init__(self, screen_size_tuple, num_picture_tuple, num_turns, start_time):

        pygame.Surface.__init__(self, size = screen_size_tuple)
        self.screen = pygame.display.set_mode(screen_size_tuple, 0, 0)
        pygame.display.set_caption("Picture Matching")

        self._num_turns = num_turns
        self._width = screen_size_tuple[0]
        self._height = screen_size_tuple[1]
        self._num_pictures_tuple = num_picture_tuple
        self._num_pictures = num_picture_tuple[0] * num_picture_tuple[1]

        self._rect_screen = screen_size_tuple # size of the window
        self._rect_surface_tiles = RECT_SURFACE_TILES # size of 990*675
        self._rect_surface_pictures = pygame.Rect(
            ((NUM_TILES_HOR-self._num_pictures_tuple[0])/2)*TILE_SIZE,
            ((NUM_TILES_VER-self._num_pictures_tuple[1])//2+1)*TILE_SIZE+TIMER_HEIGHT,
            self._num_pictures_tuple[0]*TILE_SIZE,
            self._num_pictures_tuple[1]*TILE_SIZE)# size of 720*450
        self._rect_score_board = RECT_SCORE_BOARD
        self._rect_time_total = RECT_TIME_TOTAL
        self._tiles = self.initial_tiles(TILE_SIZE)

        self.score = 0
        self.score_min = 0

        self.start_time = start_time
        self.time_total = 180000
        self.elapsed_time = 0
        self.time_bonus = 0

        self.time_add_times = 3
        self.hint_times = 5
        self.shuffle_times = 3

        self.hint_search_tile = list()
        self.hint_found = list()
        self.highlighted_items = list()
        self.hint_item = list()

        self.blank_tiles = list()

        self.connected_tiles = set()

        self.passing_tiles = list()
    
    def is_in_rect(self, x, y, rect):
        '''
        Check and return whether given position(x, y)
        is located inside of the specified rect

        Args:
        x, y(int): the postion to be checked if located in rect
        
        rect(pygame.Rect): the rectangle to be checked if 
        contains (x,y)

        Return:
        (bool): True if (x,y) is inside of rect, False otherwise.
        '''
        
        if x>=rect[0] and x<rect[0]+rect[2]\
                and y>=rect[1] and y<rect[1]+rect[3]:
            return True

    def load_image(self, x, y, image_num):
        '''
        Display a selected picture in a certain position(x, y)
        The picture should be stored in asset folder

        Args:
        x, y(int): the coordinates where the picture should be displayed

        image_num(int): the name of the picture to be displayed
        '''

        # blit images to the subsurfaces
        image_load = pygame.image.load("asset/%s.gif" % str(image_num))

        # in case no file is found
        if image_load == None:
            raise ValueError("No such file")

        self.screen.blit(image_load, (x, y, TILE_SIZE, TILE_SIZE)) 


    def initial_tiles(self, TILE_SIZE):
        '''
        Initialize the pictures and blank tiles
        Return them out as a list

        Return:
        (list): a list containing all tiles which is initialized 
        at the begining of the game
        '''

        Tiles = dict()
        
        lst_nums = rnd_pairs(25, self._num_pictures//2)

        i = 0
        for x in range(0, self._width, TILE_SIZE):
            for y in range(TIMER_HEIGHT, self._height-PUP_HEIGHT, TILE_SIZE):
                # if the tile is in the tiles panel
                if self.is_in_rect(x, y, self._rect_surface_pictures):
                    # initialize images for the tiles(pictures)
                    self.load_image(x, y, lst_nums[i])
                    # create Tile instances for each picture
                    Tiles[(x//TILE_SIZE, (y-TIMER_HEIGHT)//TILE_SIZE)] \
                        = Tile(x, y, lst_nums[i])
                    i +=1
                else:
                    # create Tile instances for each black tile
                    Tiles[(x//TILE_SIZE, (y-TIMER_HEIGHT)//TILE_SIZE)] \
                        = Tile(x, y, 26)

        pygame.display.update()
        return Tiles


    def display_score_board(self):
        '''
        Displaying the score board while running the game
        '''
        text_surface = FONT.render(
            "SCORE: "+ str(self.score),
            True,
            pygame.Color("white"),
            pygame.Color("black"))
        self.screen.fill(pygame.Color("black"), self._rect_score_board)
        self.screen.blit(text_surface, self._rect_score_board)

    def display_notice(self, notice):
        '''
        Diplaying notices in the screen while running the game.

        Args:
        notice(str): the text string of notice which is to be displayed
        '''
        
        # create text surface for the notice
        text_surface = FONT.render(
                            notice,
                            True,
                            pygame.Color("yellow"))
        # display to the screen
        self.screen.blit(text_surface, RECT_NOTICE)
                        
    def denotice(self):
        '''
        Erase the notice from the screen
        '''

        # fill the rect for notice with black
        self.screen.fill(pygame.Color("black"), RECT_NOTICE)

    def display_pup_time_add(self):
        '''
        Displaying power-up button of adding time
        '''

        text_surface = PUP_FONT.render(
            "ADD TIME: "+ str(self.time_add_times),
            True,
            pygame.Color("white"))
        pygame.draw.rect(self.screen, 
                         pygame.Color("black"),
                         RECT_PUP_TIME)
        pygame.draw.rect(self.screen, 
                       pygame.Color("white"),
                       RECT_PUP_TIME,
                       2)
        self.screen.blit(text_surface, (265, 750))

                
    def press_pup_time(self, x, y):
        '''
        Handles functionality when pressing the add-time button
        '''

        if self.is_in_rect(x, y, RECT_PUP_TIME):
            if self.time_add_times:
                self.time_add_times -=1 # deduce the remaining times
                self.time_bonus +=5000 # add time
            else:
                # if there is no more times for adding time
                pygame.draw.rect(self.screen, 
                                 pygame.Color("red"),
                                 RECT_PUP_TIME,
                                 10)
                self.display_notice("TIME POWER-UP IS USED UP")
     
    def time_rect_deduce(self):
        '''
        Handles the deducement of time bar with converting
        the elapsed time to the length of time bar
        '''

        # when pictures are displayed, initialize the elapsed_time to 0
        # when used power-up or got time bonus, deduce the elapsed_time
        self.elapsed_time = \
            pygame.time.get_ticks() - self.time_bonus - self.start_time
        
        # set the minimum elapsed time to 0
        if self.elapsed_time < 0:
            self.elapsed_time = 0

        elapsed_block = self.elapsed_time * 0.004

        # renew the rect of time regard of elapsed time
        self._rect_time_total = pygame.Rect(
            20+1, 30+1,
            TIMER_WIDTH-elapsed_block,
            TIMER_HEIGHT-27)

    def display_time_line(self):
        '''
        Diplaying time bar when game is running
        '''

        if not self.elapsed_time>=self.time_total:
            # deduce the time
            self.time_rect_deduce()
            
            # draw time bar
            pygame.draw.rect(self.screen,
                             pygame.Color("black"),
                             RECT_TIME_TOTAL)
            pygame.draw.rect(self.screen,
                             pygame.Color("white"),
                             RECT_TIME_TOTAL,
                             1)
            pygame.draw.rect(self.screen,
                             pygame.Color("red"),
                             self._rect_time_total)
            text_surface = FONT.render(
                "TIME REMAIN",
                True,
                pygame.Color("white"))
            # display to the screen
            self.screen.blit(text_surface, (300, 30, 30, 30))

    def is_game_over(self):
        '''
        Determine if the game has ran out of time

        Return:
        (bool) True if game is over, otherwise False
        '''

        if self.elapsed_time >= self.time_total:
            return True
        else:
            return False

    def all_clear(self):
        '''
        Check if all pictures are cleared by the player

        Return:
        (bool): True if no pictures available on the screen
        Otherwise False
        '''

        for key in self._tiles.keys():
            if self._tiles[key].num != 26:
                return False
        return True

    def display_ending(self, pic):
        '''
        Displaying the selected ending pictures when the game is over

        Args:
        pic(str): name of the picture file to be displayed when game over
        '''

        self.screen.fill(pygame.Color("black"))
        image_load = pygame.image.load("asset/%s.gif" % str(pic))
        self.screen.blit(image_load, (150, 350, 700, 200))
        pygame.display.update()
        pygame.time.delay(2000)

    def get_tile(self, x, y):
        '''
        Return the tile at the given postion (x, y)
        '''
        return self._tiles[(x//45, (y-TIMER_HEIGHT)//45)]

    def add_to_highlight(self, pic):
        '''
        Add the selected picture to the highlighted list
        '''
        self.highlighted_items.append(pic)
        self.highlight(pic)

    def highlight(self, pic):
        '''
        Highlighted the given picture
        '''

        self.load_image(pic.x, pic.y, "mask")
        print((pic.index_x, pic.index_y))

    def dehighlight(self, pic):
        '''
        Erase the highlight of the given picture
        '''
        self.load_image(pic.x, pic.y, 26)
        self.load_image(pic.x, pic.y, pic.num)
        
    def flush_highlight(self, state):
        '''
        Clear the highlighted list in selected mode

        Args:
        state(int):
        0 - clear the list and erase the pirtures
        1 - only clear the list
        '''

        # state 0: eliminate the pictures and flush the list
        if state == 0:
            for tile in self.highlighted_items:
                self.load_image(tile.x, tile.y, 26)
                self.highlighted_items.remove(tile)
                tile.eliminate_for_tile()
                self.score +=50
                self.time_bonus +=2000
            self.hint_dehighlight()

        else:
            # state 1: just flush the list
            for tile in self.highlighted_items:
                self.highlighted_items.remove(tile)
                self.dehighlight(tile)
            self.hint_dehighlight()

    def is_same_to(self, pic1, pic2):
        '''
        Check if pic1 is the same picture as pic2
        
        Args:
        pic1, pic2(Tile): the pictures to be checked
        '''

        if pic1.index_x == pic2.index_x \
                and pic1.index_y == pic2.index_y:
            return True
        else:
            return False

    def display_pup_hint(self):
        '''
        Displaying power-up button for giving hint
        '''
        # render textsurface
        text_surface = PUP_FONT.render(
            "HINT: "+ str(self.hint_times),
            True,
            pygame.Color("white"))
        # draw frames
        pygame.draw.rect(self.screen, 
                       pygame.Color("black"),
                       RECT_PUP_HINT)
        pygame.draw.rect(self.screen, 
                       pygame.Color("white"),
                       RECT_PUP_HINT,
                       2)
        self.screen.blit(text_surface, (90, 750))

    def hint_highlight(self, pic):
        '''
        Add the selected picture to the hint highlighted list
        '''
        if not self.hint_item:
            print("hint is asked for " + str(self.highlighted_items[0]))
            self.load_image(pic.x, pic.y, "hintmask")
            self.hint_item.append(pic)
            print("hint is given at " + str(pic))

    def hint_dehighlight(self):
        for pic in self.hint_item:
            self.load_image(pic.x, pic.y, 26)
            self.load_image(pic.x, pic.y, pic.num)
        if self.hint_item:
            self.hint_item = []

    def press_pup_hint(self, x, y):
        '''
        Handles functionality when pressing the Hint button
        '''
        if self.is_in_rect(x, y, RECT_PUP_HINT):
            print("ASK FOR HINT: ")
            
            if self.hint_times:
                print(str(self.hint_times-1) + " times left")
                if len(self.highlighted_items)==1:
                    if not self.search_paired_hints(self.highlighted_items[0], 0):
                        print("No hint found")
                        self.display_notice("SORRY, NO HINT FOUND")
                        return False
                    else:
                        self.hint_times -=1 # deduce the remaining times
                        return True
                    
            else:
                # if there is no more times for adding time
                pygame.draw.rect(self.screen, 
                                 pygame.Color("red"),
                                 RECT_PUP_HINT,
                                 10)  
                self.display_notice("HINT POWER-UP IS USED UP")
        
    def left_side_tiles(self, pic):
        '''
        Check for the pic, and put all consecutive blank tiles
        which is to the left of pic into a list, then return
        it out

        Args:
        pic(Tile): the picture to be checked for left side

        Return:
        (list): A list containing all consecutive blank tiles to the
        left of pic
        '''

        lst = list()

        for i in range(1, pic.index_x-1):
            
            if not self._tiles[(pic.index_x - i), pic.index_y].is_active():
                lst.append(self._tiles[(pic.index_x - i), pic.index_y])
            else:
                break
        return lst

    def right_side_tiles(self, pic):
        '''
        Check for the pic, and put all consecutive blank tiles
        which is to the right of pic into a list, then return
        it out

        Args:
        pic(Tile): the picture to be checked for right side

        Return:
        (list): A list containing all consecutive blank tiles to the
        right of pic
        '''

        lst = list()

        for i in range(1, 20-pic.index_x):
            
            if not self._tiles[(pic.index_x + i), pic.index_y].is_active():
                lst.append(self._tiles[(pic.index_x + i), pic.index_y])
            else:
                break
        return lst

    def top_side_tiles(self, pic):
        '''
        Check for the pic, and put all consecutive blank tiles
        which is to the top of pic into a list, then return
        it out

        Args:
        pic(Tile): the picture to be checked for top side

        Return:
        (list): A list containing all consecutive blank tiles to the
        top of pic
        '''

        lst = list()

        for i in range(1, pic.index_y-1):
            
            if not self._tiles[pic.index_x, (pic.index_y-i)].is_active():
                lst.append(self._tiles[pic.index_x, (pic.index_y-i)])
            else:
                break
        return lst

    def bottom_side_tiles(self, pic):
        '''
        Check for the pic, and put all consecutive blank tiles
        which is to the bottom of pic into a list, then return
        it out

        Args:
        pic(Tile): the picture to be checked for bottom side

        Return:
        (list): A list containing all consecutive blank tiles to the
        bottom of pic
        '''

        lst = list()

        for i in range(1, 14 - pic.index_y):
            
            if not self._tiles[pic.index_x, (pic.index_y+i)].is_active():
                lst.append(self._tiles[pic.index_x, (pic.index_y+i)])
            else:
                break
        return lst


    def hint_left_side_tiles(self, pic, num):
        '''
        Check for the tile which is to the left of pic, return if or not
        they have their num-attribute equal to num.

        Args:
        pic(Tile): the picture which is to be check for left side
        num(int): the value to be checked

        Return:
        (bool): True if one of the blank tiles has their num-attribute
        is equal to num. Otherwise False
        '''
        
        for i in range(1, pic.index_x-1):
            if self._tiles[(pic.index_x - i), pic.index_y].is_active():
                if (self._tiles[(pic.index_x - i), pic.index_y].num == num
                    and not self.is_same_to(
                        self._tiles[(pic.index_x-i), pic.index_y], 
                        self.hint_search_tile[0])):
                    self.hint_found.append(self._tiles[(pic.index_x-i), pic.index_y])
                    return True
                else:
                    return False

    def hint_right_side_tiles(self, pic, num):
        '''
        Check for the tile which is to the right of pic, return if or not
        they have their num-attribute equal to num.

        Args:
        pic(Tile): the picture which is to be check for right side
        num(int): the value to be checked

        Return:
        (bool): True if one of the blank tiles has their num-attribute
        is equal to num. Otherwise False
        '''

        for i in range(1, 20-pic.index_x):
            if self._tiles[(pic.index_x + i), pic.index_y].is_active():
                if (self._tiles[(pic.index_x+i), pic.index_y].num == num
                    and not self.is_same_to(
                        self._tiles[(pic.index_x+i), pic.index_y], 
                        self.hint_search_tile[0])):      
                    
                    self.hint_found.append(self._tiles[(pic.index_x+i), pic.index_y])
                    return True
                else:
                    return False

    def hint_top_side_tiles(self, pic, num):
        '''
        Check for the tile which is to the top of pic, return if or not
        they have their num-attribute equal to num.

        Args:
        pic(Tile): the picture which is to be check for top side
        num(int): the value to be checked

        Return:
        (bool): True if one of the blank tiles has their num-attribute
        is equal to num. Otherwise False
        '''
      
        for i in range(1, pic.index_y-1):
            if self._tiles[pic.index_x, (pic.index_y-i)].is_active():
                if (self._tiles[pic.index_x, (pic.index_y-i)].num == num
                    and not self.is_same_to(
                        self._tiles[pic.index_x, (pic.index_y-i)], 
                        self.hint_search_tile[0])):
               
                    self.hint_found.append(self._tiles[pic.index_x, (pic.index_y-i)])
                    return True
                else:
                    return False

    def hint_bottom_side_tiles(self, pic, num):
        '''
        Check for the tile which is to the bottom of pic, return if or not
        they have their num-attribute equal to num.

        Args:
        pic(Tile): the picture which is to be check for bottom side
        num(int): the value to be checked

        Return:
        (bool): True if one of the blank tiles has their num-attribute
        is equal to num. Otherwise False
        '''

        for i in range(1, 14 - pic.index_y):
            if self._tiles[pic.index_x, (pic.index_y+i)].is_active():
                if (self._tiles[pic.index_x, (pic.index_y+i)].num == num
                    and not self.is_same_to(
                        self._tiles[pic.index_x, (pic.index_y+i)], 
                        self.hint_search_tile[0])):
                    
                    self.hint_found.append(self._tiles[pic.index_x, (pic.index_y+i)])
                    return True
                else:
                    return False

    def search_zero_turn(self, pic, num):
        '''
        Check if the picture with its num-attribute equal to num
        is reachable without making turns from the given pic.

        Args:
        pic(Tile): the picture tile which is to be checked for all consecutive
        tiles in the same row or column

        num(int): the value of picture which is to be checked if existed 
        '''
        
        if self.hint_left_side_tiles(pic, num):
            return True
        if self.hint_right_side_tiles(pic, num):
            return True
        if self.hint_top_side_tiles(pic, num):
            return True
        if self.hint_bottom_side_tiles(pic, num):
            return True

    def search_one_turn(self, pic, num):
        '''
        Check if the picture with its num-attribute equal to num
        is reachable within one turn from the given pic.
        '''
     
        for tile in self.left_side_tiles(pic):
            if self.search_zero_turn(tile, num):
                return True
        
        for tile in self.right_side_tiles(pic):
            if self.search_zero_turn(tile, num):
                return True

        for tile in self.top_side_tiles(pic):
            if self.search_zero_turn(tile, num):
                return True

        for tile in self.bottom_side_tiles(pic):
            if self.search_zero_turn(tile, num):
                return True

    def search_two_turns(self, pic, num):
        '''
        Check if the picture with its num-attribute equal to num
        is reachable within two turns from the given pic.
        '''
        
        for tile in self.left_side_tiles(pic):
            if self.search_one_turn(tile, num):
                return True
    
        for tile in self.right_side_tiles(pic):
            if self.search_one_turn(tile, num):
                return True
        
        for tile in self.top_side_tiles(pic):
            if self.search_one_turn(tile, num):
                return True
        
        for tile in self.bottom_side_tiles(pic):
            if self.search_one_turn(tile, num):
                return True

    def search_paired_hints(self, pic, mode):
        '''
        Return the available pairing picture with least
        turns to reach.
        return None if no available picture was found.
        Using BFS with minimum turns

        Args
        pic(Tile): the picture which is to be checked for hint

        mode(int): 1 - just find the counterpart
        0 - find paired counterpart for pic and highlight it
        '''

        self.hint_search_tile.append(pic)

        # First search pictures with zero turns for validity
        num = pic.num
        if self.search_zero_turn(pic, num):
            if mode == 0:
                self.hint_highlight(self.hint_found[0])
            self.hint_found = list()
            self.hint_search_tile = list()
            return True

        # If not find available pairing picture,
        # search for the pairing picture with one turn
        if self.search_one_turn(pic, num):
            if mode == 0:
                self.hint_highlight(self.hint_found[0])
            self.hint_found = list()
            self.hint_search_tile = list()
            return True

        # search for the pairing picture with two turns
        if self.search_two_turns(pic, num):
            if mode == 0:
                self.hint_highlight(self.hint_found[0])
            self.hint_found = list()
            self.hint_search_tile = list()
            return True

        return False

    def display_pup_shuf(self):
        '''
        Display the shuffle power-up button in the game
        '''

        text_surface = PUP_FONT.render(
            "SHUFFLE: "+ str(self.shuffle_times),
            True,
            pygame.Color("white"))

        pygame.draw.rect(self.screen, 
                         pygame.Color("black"),
                         RECT_PUP_SHUF)

        pygame.draw.rect(self.screen,
                       pygame.Color("white"),
                       RECT_PUP_SHUF,
                       2)

        self.screen.blit(text_surface, (470, 750))

    def press_pup_shuf(self, x, y):
        '''
        Handles functionality when pressing the shuffle button
        '''

        if self.is_in_rect(x, y, RECT_PUP_SHUF):
            if self.shuffle_times:
                self.shuffle_times -=1 # deduce the remaining times
                self.shuffle_pics()
            else:
                # if there is no more times for adding time
                pygame.draw.rect(self.screen, 
                                 pygame.Color("red"),
                                 RECT_PUP_SHUF,
                                 10)
                self.display_notice("SHUFFLE POWER-UP IS USED UP")

    def shuffle_pics(self):
        '''
        Shuffle all pictures in the game interface.
        Rearrange the order of all available pictures.
        '''

        lst_position = list()
        lst_pic_nums = list()
        lst_position_index = list()

        num_available_pic = 0
        # check for the available pictures on the surface
        for tile_tuple in self._tiles.items():
            tile = tile_tuple[1]
            if tile.is_active():
                lst_position_index.append((tile.index_x, tile.index_y))
                lst_position.append((tile.x, tile.y))
                lst_pic_nums.append(tile.num)
                num_available_pic += 1

        print("# available pictures now: " + str(num_available_pic))

        self.screen.fill(pygame.Color("black"), RECT_SURFACE_TILES)

        # randomize the list of existing picture numbers
        random.shuffle(lst_pic_nums)
        
        # Re-display the pictures in the new order
        for i in range(0, num_available_pic):
            self.load_image(lst_position[i][0], lst_position[i][1], lst_pic_nums[i])
            self._tiles[(lst_position_index[i][0], lst_position_index[i][1])]\
                = Tile(lst_position[i][0], lst_position[i][1], lst_pic_nums[i])

        pygame.display.update()

    def check_whether_shuffle(self):
        '''
        Automatically checks for if there is 
        available pair existed in the game or not
        '''
        for tile_tuple in self._tiles.items():
            tile = tile_tuple[1]

            if tile.is_active():
                # if found one pair available 
                if self.search_paired_hints(tile, 1):
                    return True

        # if not, shuffle the pictures automatically
        self.shuffle_pics()


    def search_left_side_tiles(self, pic, pic2):
        '''
        Check for the tiles which are to the left of pic, return if or not
        one of the tiles is pic2

        Args:
        pic(Tile): the picture tile which is to be check for left side
        pic2(Tile): the picture which is to be checked if is among the tiles
        which are to the left of pic

        Return:
        (list): 
        a list containing all consecutive blank tiles which are to the left of pic.
        Or pic2 as a list, if pic2 is found this time.
        '''

        lst = list()

        for i in range(1, pic.index_x-1):
            if self._tiles[(pic.index_x - i), pic.index_y].num==26:
                lst.append(self._tiles[(pic.index_x - i), pic.index_y])
            else:
                if self.is_same_to(self._tiles[(pic.index_x - i), pic.index_y], pic2):
                    return [self._tiles[(pic.index_x - i), pic.index_y]]
                break
        return lst

    def search_right_side_tiles(self, pic, pic2):
        '''
        Check for the tiles which are to the right of pic, return if or not
        one of the tiles is pic2

        Args:
        pic(Tile): the picture tile which is to be check for right side
        pic2(Tile): the picture which is to be checked if is among the tiles
        which are to the right of pic

        Return:
        (list): 
        a list containing all consecutive blank tiles which are to 
        the right of pic. 
        Or pic2 as a list, if pic2 is found this time.
        '''

        lst = list()

        for i in range(1, 20-pic.index_x):
            if self._tiles[(pic.index_x + i), pic.index_y].num==26:
                lst.append(self._tiles[(pic.index_x + i), pic.index_y])
            else:
                if self.is_same_to(self._tiles[(pic.index_x + i), pic.index_y], pic2):
                    return [self._tiles[(pic.index_x + i), pic.index_y]]
                break
        return lst

    def search_top_side_tiles(self, pic, pic2):
        '''
        Check for the tiles which are to the top of pic, return if or not
        one of the tiles is pic2

        Args:
        pic(Tile): the picture tile which is to be check for top side
        pic2(Tile): the picture which is to be checked if is among the tiles
        which are to the top of pic

        Return:
        (list): 
        a list containing all consecutive blank tiles which are to 
        the top of pic. 
        Or pic2 as a list, if pic2 is found this time.
        '''

        lst = list()
        for i in range(1, pic.index_y-1):
            if self._tiles[pic.index_x, (pic.index_y-i)].num==26:
                lst.append(self._tiles[pic.index_x, (pic.index_y-i)])
            else:
                if self.is_same_to(self._tiles[pic.index_x, (pic.index_y-i)], pic2):
                    return [self._tiles[pic.index_x, (pic.index_y-i)]]
                break
        return lst

    def search_bottom_side_tiles(self, pic, pic2):
        '''
        Check for the tiles which are to the bottom of pic, return if or not
        one of the tiles is pic2

        Args:
        pic(Tile): the picture tile which is to be check for bottom side
        pic2(Tile): the picture which is to be checked if is among the tiles
        which are to the bottom of pic

        Return:
        (list): 
        a list containing all consecutive blank tiles which are to 
        the bottom of pic. 
        Or pic2 as a list, if pic2 is found this time.
        '''

        lst = list()
        for i in range(1, 14 - pic.index_y):
            if self._tiles[pic.index_x, (pic.index_y+i)].num==26:
                lst.append(self._tiles[pic.index_x, (pic.index_y+i)])
            else:
                if self.is_same_to(self._tiles[pic.index_x, (pic.index_y+i)], pic2):
                    return [self._tiles[pic.index_x, (pic.index_y+i)]]
                break
        return lst

    def reachable(self, pic1, pic2):
        '''
        Check if pic1 is connectable to pic2 without making turns
        If yes, return True
        If not, return all consecutive blank tiles which are connectable
        to pic1 without making turns in a set.

        NOTE: pic1 here is not the same pic1 in connectable() function
        while pic2 here is always the same pic2 given as the parameter in 
        connectable() function

        Return:
        either Ture if pic2 is found without making turns from pic1 
        or a set of blank tiles which pic1 could reach without making turns

        Efficiency:
        O(r) while r is the # of rows or columns of all pictures
        (worst case)
        '''

        reached = set()

        for tile in self.search_left_side_tiles(pic1, pic2): #O(r)
            if self.is_same_to(tile, pic2): #O(1)
                return True
            else:
                reached.add(tile) #O(1)

        for tile in self.search_right_side_tiles(pic1, pic2):
            if self.is_same_to(tile, pic2):
                return True
            else:
                reached.add(tile)

        for tile in self.search_top_side_tiles(pic1, pic2):
            if self.is_same_to(tile, pic2):
                return True
            else:
                reached.add(tile)

        for tile in self.search_bottom_side_tiles(pic1, pic2):
            if self.is_same_to(tile, pic2):
                return True
            else:
                reached.add(tile)
        
        return reached

    def connectable(self, pic1, pic2):
        '''
        Main function to determine if pic1 can
        reach pic2 within certain turns

        Return:
        (int): number of turns it takes for pic1 to reach pic2
        -1 if pic1 cannot reach pic2 within the maximum number
        of turns.

        Efficiency: 
        O(#row * #col)
        '''
        
        reached_temp = set()
        reached_curr = set()

        reached_curr.add(pic1)
        
        # then iteriate from 0 turn to n turns
        for n in range(0, self._num_turns+1): # O(n)
                      
            # for each blank tile found last time
            for tile in reached_curr:
                # check if it can reach pic2 without making turns
                reached = self.reachable(tile, pic2)

                # if yes, reached should be a boolean value True
                if reached == True:
                    pic2.prev = tile
                    print(" %s-turn" % str(n))
                    # return the num of turns out
                    return n

                # if not, reached will be a set of blank tiles
                else:
                    for blank_tile in reached:
                        # record their previous tiles
                        if blank_tile.prev is None:
                            blank_tile.prev = tile

                    # add the blank tiles into the temp set
                    reached_temp = reached_temp.union(reached)

            reached_curr = reached_temp

            # clear the temp set
            reached_temp = set()

        # if cannot found the route eventually
        # return -1 indicating not connectable
        return -1

    def is_pair_to(self, pic1, pic2):
        '''
        Check if pic1 is connectable by rules
        to pic2. And handles the score penalty
        for making more than two turns.

        Return True if pic1 and pic2 are 
        connectable. Otherwise False
        '''

        if pic1.num == pic2.num \
                and not self.is_same_to(pic1, pic2):

            connect_turns = self.connectable(pic1, pic2)
            # if pic1 is not connectable to pic2
            if  connect_turns == -1:
                return False

            # if #turns larger than 2, deduct scores
            elif connect_turns > 2:
                self.score -= 200
                if self.score < self.score_min:
                    self.score = self.score_min-100
                return True
            # if #turns smaller or equal to 2
            else:
                return True

    def trace_back_items(self, start, end):
        '''
        Check and record every tile where the route making turns
        from the start picture to the end picture.
        Return them in a ordered list
        '''

        path = [end]

        curr = end

        while curr!=start:
            prev = curr.prev
            path.append(prev)
            
            curr = prev

        return path

    def draw_lines(self, pic1, pic2, color):
        '''
        Draw connecting lines with a selected color
        between two pictures
        '''
      
        self.passing_tiles = \
            self.trace_back_items(pic1, pic2)

        self.passing_tiles = self.passing_tiles[1:-1]

        if not self.passing_tiles:
            pygame.draw.line(self.screen, 
                         pygame.Color("%s" % str(color)),
                         (pic2.x_center, pic2.y_center),
                         (pic1.x_center, pic1.y_center),
                         3)

        else:
            pygame.draw.line(self.screen, 
                             pygame.Color("%s" % str(color)),
                             (pic2.x_center, pic2.y_center),
                             (self.passing_tiles[0].x_center, self.passing_tiles[0].y_center),
                             3)

            if len(self.passing_tiles):
                for i in range(len(self.passing_tiles)-1):
                    pygame.draw.line(self.screen, 
                                     pygame.Color("%s" % str(color)), 
                                     (self.passing_tiles[i].x_center, 
                                      self.passing_tiles[i].y_center),
                                     (self.passing_tiles[i+1].x_center, 
                                      self.passing_tiles[i+1].y_center),
                                     3)

            pygame.draw.line(self.screen, 
                             pygame.Color("%s" % str(color)),
                             (self.passing_tiles[-1].x_center, self.passing_tiles[-1].y_center),
                             (pic1.x_center, pic1.y_center),
                             3)

    def draw_connect_lines(self, pic1, pic2):
        '''
        Drawing connecting lines between two pictures

        Args:
        pic1, pic2(Tile): Pictures to be connected
        '''

        self.draw_lines(pic1, pic2, "red")

        # update the lines and delay for 400ms
        pygame.display.update()
        pygame.time.delay(400)

        # clear the lines
        self.draw_lines(pic1, pic2, "black")
        
        # empty the list
        self.passing_tiles = []
      
        for tile_tuple in self._tiles.items():
            tile = tile_tuple[1]
            tile.prev = None
                
    def selected_two_pics(self):
        '''
        Check if player has selected two pictures
        '''
        if len(self.highlighted_items)==2:
            return True

    def on_click(self, x, y):
        '''
        Handles the functionality when the mouse is pressed on the
        game surface.
        '''

        # erase the highlight for hints
        self.hint_dehighlight()
        # clear the notice from screen
        self.denotice()

        # if mouse pressed on the surface for tiles
        if self.is_in_rect(x, y, self._rect_surface_tiles):


            # get the selected tile
            pic = self.get_tile(x, y)

            # if there is picture on this tile
            if pic.is_active():

                # if this picture has been selected before
                # cancel this time's selecting
                if pic in self.highlighted_items:
                    self.flush_highlight(1)
                    
                # if this picture has not been selected before
                # put the picture into the highlight list
                else:
                    self.add_to_highlight(pic)

                    # if has selected two pictures, go checking if they are
                    # erasable pair
                    if self.selected_two_pics():
                        
                        # if the two pictures can be connected by the rule
                        if self.is_pair_to(self.highlighted_items[0]
                                           , self.highlighted_items[1]):
                            
                            # highlight the second picture for a while
                            self.add_to_highlight(pic)
                            
                            # displaying the connecting lines 
                            # between them for a while
                            self.draw_connect_lines(self.highlighted_items[0]\
                                                        , self.highlighted_items[1])
                            
                            # erase the pictures and clear 
                            # the highlight list as well
                            self.flush_highlight(0)
                              
                        # if they cannot be connected
                        # just flush the highlighted list
                        else:
                            self.flush_highlight(1)

            # if there is no pictures on this tile
            # just flush the highlighted list
            else:
                self.flush_highlight(1)
        else:
            # if not pressing into the subsurface for tiles

            # if not asking for hint
            if not self.is_in_rect(x, y, RECT_PUP_HINT):
                self.flush_highlight(1)
            else:
                self.press_pup_hint(x, y)
            
            # check if pressed on other power-ups
            self.press_pup_time(x ,y)
            self.press_pup_shuf(x, y)
        
        # check if there is available pairs left in the game
        self.check_whether_shuffle()
