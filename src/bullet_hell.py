import pygame
import json
from settings import *

pygame.init()

from game_loop import *
from main_menu import *
from game_over import *


SCREEN = pygame.display.set_mode(SCREEN_SIZE)
pygame.display.set_caption("Bullet Hell")
clock = pygame.time.Clock()


game_state = STATE_MAIN_MENU
running = True
menu = True
playing = False
game_over_screen = False

music = pygame.mixer.Sound("src/music/music.wav")

while running:

    if menu:
        game_state = main_menu(SCREEN)

    elif playing:
        music.play()
        game_state = game_loop(SCREEN)
        if scores[0]["score"] < scores[1]["score"]:
            scores[0]["score"] = scores[1]["score"]

    elif game_over_screen:
        music.stop()
        game_state = game_over(SCREEN)
    
    if game_state == STATE_MAIN_MENU:
        menu = True
        playing = False
        game_over_screen = False

    elif game_state == STATE_PLAYING:
        playing = True
        menu = False
        game_over_screen = False
    
    elif game_state == STATE_GAME_OVER:
        game_over_screen = True
        playing = False
        menu = False

    elif game_state == GAME_EXIT:
        running = False

    pygame.display.flip()
    clock.tick(FPS)

overwrite_scoreboard(scores)
overwrite_difficulty_settings(difficulty_settings)

pygame.quit()