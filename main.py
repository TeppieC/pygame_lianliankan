import sys, pygame, os, gui, time, modegui
import asset
from gui import GUI
from tile import Tile
from modegui import ModeWindow
from pygame import time

# define the position for generating the windows
# from pygame wiki
X = 150
Y = 50
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (X, Y)

# add background music to the game
pygame.init()
pygame.mixer.init()
pygame.time.delay(1000)
pygame.mixer.music.load("classical_music.mp3")
pygame.mixer.music.play(-1, 0.0)

MODEGUI_SIZE = (990, 180)
mode_surface = ModeWindow(MODEGUI_SIZE)
mode_surface.ask_question()
start_time = mode_surface.return_time_elapsed()
num_turns = mode_surface.return_num_turn()

print("Game Mode: " + str(num_turns) + " turns")
# initialize the surface
SCREEN_SIZE = (990, 800)
NUM_PICTURES = (16, 10)
surface = GUI(SCREEN_SIZE, NUM_PICTURES, num_turns, start_time)

while not surface.is_game_over():

    # check if player has cleared all pictures
    if surface.all_clear():
        surface.display_ending("youwin")
        break

    # update the surface and all objects
    pygame.display.update()
    surface.display_time_line()
    surface.display_score_board()
    surface.display_pup_time_add()
    surface.display_pup_hint()
    surface.display_pup_shuf()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.display.quit()
            sys.exit()
        # End if q is pressed
        elif (event.type == pygame.KEYDOWN and
        (event.key == pygame.K_q or event.key == pygame.K_ESCAPE)):
            pygame.display.quit()
            sys.exit()
        # Respond to clicks
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = event.pos
            x_mouse = mouse_pos[0]
            y_mouse = mouse_pos[1]
            surface.on_click(x_mouse, y_mouse)
            pygame.display.update()

# display the ending pictures to the player
surface.display_ending("gameover")
print("game over")

sys.exit()
