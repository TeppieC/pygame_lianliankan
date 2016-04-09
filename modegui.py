import sys, pygame, random, time
import asset
from pygame import Surface
from pygame import time
from pygame.locals import *

pygame.init()

BACK_COLOR = pygame.Color("BLACK")

pygame.font.init()
FONT_SIZE_BIG = 30
FONT_BIG = pygame.font.SysFont("Mono", FONT_SIZE_BIG, True)
FONT_SIZE_SMALL = 20
FONT_SMALL = pygame.font.SysFont("Mono", FONT_SIZE_SMALL, True)
FONT_COLOR = pygame.Color("WHITE")

class ModeWindow(pygame.Surface):
    def __init__(self, screen_size_tuple):

        pygame.Surface.__init__(self, size = screen_size_tuple)
        self.screen = pygame.display.set_mode(screen_size_tuple, 0, 0)
        pygame.display.set_caption("Mode Select")
        
        self.rect_question = (20, 20)
        self.str_num_turn = str()
        self.question = "Enter the max number of turns allowed: "
        self.instruction = "Press [Enter] to forward..."

    def get_key(self):
        '''
        Get key when player is typing on the keyboard
        and return the key out
        '''

        # check for pygame events
        event = pygame.event.poll()

        # if pressed on the keyboard
        while event.type != KEYUP:
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            event = pygame.event.poll()

        # return the key out
        return event.key

    def ask_question(self):
        '''
        Get all keys that the player has typed. And combine
        them as a number larger than 1
        '''
        key = K_SPACE
        while key != K_RETURN or not int(self.str_num_turn)>1:

            # check if pressed [Esc]
            if key == K_ESCAPE:
                pygame.display.quit()
                sys.exit()

            self.display_question()
            key = self.get_key()
            if K_0 <= key <= K_9:
                self.str_num_turn = self.str_num_turn + pygame.key.name(key)

    def return_time_elapsed(self):
        '''
        return time elapsed when stilling in mode select window
        '''
        return pygame.time.get_ticks()

    def return_num_turn(self):
        return int(self.str_num_turn)

    def display_question(self):
        '''
        Displaying question to the player in the mode select
        window
        '''

        # print question
        question = self.question + self.str_num_turn
        text_surface = FONT_BIG.render(
            question, True, FONT_COLOR, BACK_COLOR)
        self.screen.blit(text_surface, self.rect_question)

        # print instruction
        instr_surface = FONT_SMALL.render(
            self.instruction, True, FONT_COLOR, BACK_COLOR)
        self.screen.blit(instr_surface, (20, 100))

        pygame.display.update()
