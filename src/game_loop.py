import pygame
from random import randint

import pygame.image
from enemies import *
from functions import *
from settings import *
import USEREVENTS

background = pygame.image.load("src/graphics/background.png")
background = pygame.transform.scale(background, SCREEN_SIZE)

FONT = pygame.font.Font(None, 30)

INFO_SURFACE_WIDTH = 75
INFO_SURFACE_HEIGHT = 30
score_surface = pygame.rect.Rect(0, HEIGHT - INFO_SURFACE_HEIGHT, INFO_SURFACE_WIDTH, INFO_SURFACE_HEIGHT)
lives_surface = pygame.rect.Rect(WIDTH - INFO_SURFACE_WIDTH, HEIGHT - INFO_SURFACE_HEIGHT, INFO_SURFACE_WIDTH, INFO_SURFACE_HEIGHT)


PLAYER_BULLET_DELAY = 70
SPAWN_FLOODER_DELAY_LOWER = 10000
SPAWN_FLOODER_DELAY_UPPER = 20000
SPAWN_GRUNTS_DELAY_LOWER = 5000
SPAWN_GRUNTS_DELAY_UPPER = 15000


def clear_screen(grunt_wave_left, grunt_wave_right, grunt_bullets, flooders, flooder_bullets):
    grunt_wave_left.clear()
    grunt_wave_right.clear()
    grunt_bullets.clear()
    flooders.clear()
    flooder_bullets.clear()

    pygame.time.set_timer(USEREVENTS.SPAWN_CENTER_FLOODER, randint(SPAWN_FLOODER_DELAY_LOWER, SPAWN_FLOODER_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_LEFT_FLOODER, randint(SPAWN_FLOODER_DELAY_LOWER, SPAWN_FLOODER_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_RIGHT_FLOODER, randint(SPAWN_FLOODER_DELAY_LOWER, SPAWN_FLOODER_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_GRUNT_LEFT, randint(SPAWN_GRUNTS_DELAY_LOWER, SPAWN_GRUNTS_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_GRUNT_RIGHT, randint(SPAWN_GRUNTS_DELAY_LOWER, SPAWN_GRUNTS_DELAY_UPPER))

def game_loop(screen: pygame.Surface) -> int:
    """bucle principal del gameplay

    Args:
        screen (pygame.Surface): pantalla sobre la que se dibujaran los elementos

    Returns:
        int: corresponde a un valor de game_state
    """
    clock = pygame.time.Clock()
    playing = True

    player_lives = difficulty_settings["starting_lives"]
    player_rect = pygame.rect.Rect(0, 0, PJ_WIDTH, PJ_HEIGHT)
    player_rect.midbottom = screen.get_rect().midbottom
    player_image_rect = player_image.get_rect()
    scores[1]["score"] = 0

    pickups = []
    player_bullets = []
    player_homing_bullets = []
    grunt_wave_right = []
    grunt_wave_left = []
    grunt_bullets = []
    flooders = []
    flooder_bullets = []

    power_up = False
    aim_left = True

    pygame.time.set_timer(USEREVENTS.BULLET_EVENT, PLAYER_BULLET_DELAY)
    pygame.time.set_timer(USEREVENTS.SPAWN_PICKUP, 30)
    pygame.time.set_timer(USEREVENTS.FIRE_HOMING_BULLET, 210)
    pygame.time.set_timer(USEREVENTS.GRUNT_FIRE, GRUNT_BULLET_DELAY * difficulty_settings["enemy_difficulty"])
    pygame.time.set_timer(USEREVENTS.FLOODER_FIRE, FLOODER_BULLET_DELAY * difficulty_settings["enemy_difficulty"])
    pygame.time.set_timer(USEREVENTS.SPAWN_GRUNT_LEFT, randint(SPAWN_GRUNTS_DELAY_LOWER, SPAWN_GRUNTS_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_GRUNT_RIGHT, randint(SPAWN_GRUNTS_DELAY_LOWER, SPAWN_GRUNTS_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_CENTER_FLOODER, randint(SPAWN_FLOODER_DELAY_LOWER, SPAWN_FLOODER_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_LEFT_FLOODER, randint(SPAWN_FLOODER_DELAY_LOWER, SPAWN_FLOODER_DELAY_UPPER))
    pygame.time.set_timer(USEREVENTS.SPAWN_RIGHT_FLOODER, randint(SPAWN_FLOODER_DELAY_LOWER, SPAWN_FLOODER_DELAY_UPPER))

    while playing:
        screen.blit(background, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return GAME_EXIT

            else:

                if event.type == USEREVENTS.BULLET_EVENT:
                    create_player_bullets(player_rect, player_bullets)

                if event.type == USEREVENTS.SPAWN_PICKUP:
                    pickups.append(spawn_pickup())

                if event.type == USEREVENTS.FIRE_HOMING_BULLET:
                    if power_up:
                        create_homing_bullets(player_rect, grunt_wave_left + grunt_wave_right + flooders, player_homing_bullets)
                
                if event.type == USEREVENTS.END_OF_POWERUP:
                    power_up = False

                if event.type == USEREVENTS.SPAWN_GRUNT_RIGHT:
                    grunt_wave_right = spawn_grunt_wave(10, WIDTH + 30, 100, -25)
                    pygame.time.set_timer(USEREVENTS.SPAWN_GRUNT_RIGHT, randint(SPAWN_GRUNTS_DELAY_LOWER, SPAWN_GRUNTS_DELAY_UPPER))

                if event.type == USEREVENTS.SPAWN_GRUNT_LEFT:
                    grunt_wave_left = spawn_grunt_wave(10, -20, 30, 25)
                    pygame.time.set_timer(USEREVENTS.SPAWN_GRUNT_LEFT, randint(SPAWN_GRUNTS_DELAY_LOWER, SPAWN_GRUNTS_DELAY_UPPER))

                if event.type == USEREVENTS.SPAWN_CENTER_FLOODER:
                    flooders.append(spawn_center_flooder())

                if event.type == USEREVENTS.SPAWN_LEFT_FLOODER:
                    flooders.append(spawn_left_flooder())

                if event.type == USEREVENTS.SPAWN_RIGHT_FLOODER:
                    flooders.append(spawn_right_flooder())

                if event.type == USEREVENTS.FLOODER_FIRE:
                    spawn_flooder_bullet(flooders, flooder_bullets)
                    aim_left = control_flooder_aim(flooders, aim_left)

                if event.type == USEREVENTS.GRUNT_FIRE:
                    spawn_grunt_bullets(grunt_wave_right, grunt_bullets, player_rect)
                    spawn_grunt_bullets(grunt_wave_left, grunt_bullets, player_rect)

        score_text = FONT.render(f"Score: {scores[1]["score"]}", True, "cyan")
        lives_text = FONT.render(f"Lives: {player_lives}", True, "green")
        screen.blit(score_text, score_surface)
        screen.blit(lives_text, lives_surface)


        power_up = pickup_behaviour(pickups, player_rect, screen, power_up)

        move_player_rect(player_rect)
        control_player_movement_bounds(player_rect)
        player_image_rect.center = player_rect.center
        screen.blit(player_image, player_image_rect)
        player_fire(player_bullets, screen)
        homing_bullets_behaviour(screen, player_homing_bullets, grunt_wave_left + grunt_wave_right + flooders)

        grunt_behaviour(screen, grunt_wave_right, grunt_bullets, player_bullets, player_homing_bullets, False)
        grunt_behaviour(screen, grunt_wave_left, grunt_bullets, player_bullets, player_homing_bullets)
        flooder_behaviour(flooders, flooder_bullets, screen, player_bullets, player_homing_bullets)

        if player_gets_hit(player_rect, grunt_bullets + flooder_bullets):
            player_lives -= 1
            power_up = False
            clear_screen(grunt_wave_left, grunt_wave_right, grunt_bullets, flooders, flooder_bullets)
            screen.fill("red")
            pygame.display.flip()
            pygame.time.wait(100)

        if player_lives <= 0:
            return STATE_GAME_OVER

        pygame.display.flip()
        clock.tick(FPS)



