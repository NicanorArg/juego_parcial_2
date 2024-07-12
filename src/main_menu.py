import pygame
from persistant_data import *
from settings import *


FONT = pygame.font.Font(None, 60)
SETTINGS_FONT = pygame.font.Font(None, 30)


BUTTON_WIDTH = 300
BUTTON_HEIGHT = 100
SETTINGS_RECT_WIDTH = 50
SETTINGS_RECT_HEIGHT = 50

button_start = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - 150), (BUTTON_WIDTH, BUTTON_HEIGHT))
button_quit = pygame.Rect((WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 + 50), (BUTTON_WIDTH, BUTTON_HEIGHT))
hi_score_rect = pygame.rect.Rect(0, 0, 300, 50)
last_score_rect = pygame.rect.Rect(0, 50, 300, 50)

starting_lives_rect = pygame.rect.Rect(0, HEIGHT - SETTINGS_RECT_HEIGHT, SETTINGS_RECT_WIDTH * 7, SETTINGS_RECT_HEIGHT)
starting_lives_button_1 = pygame.rect.Rect(180, starting_lives_rect.y, SETTINGS_RECT_WIDTH, SETTINGS_RECT_HEIGHT)
starting_lives_button_2 = pygame.rect.Rect(starting_lives_button_1.right + 10, starting_lives_rect.y, SETTINGS_RECT_WIDTH, SETTINGS_RECT_HEIGHT)
starting_lives_button_3 = pygame.rect.Rect(starting_lives_button_2.right + 10, starting_lives_rect.y, SETTINGS_RECT_WIDTH, SETTINGS_RECT_HEIGHT)

enemy_difficulty_rect = pygame.rect.Rect(0, HEIGHT - SETTINGS_RECT_HEIGHT * 2 - 5, SETTINGS_RECT_WIDTH * 7, SETTINGS_RECT_HEIGHT)
enemy_difficulty_button_1 = pygame.rect.Rect(180, enemy_difficulty_rect.y, SETTINGS_RECT_WIDTH, SETTINGS_RECT_HEIGHT)
enemy_difficulty_button_2 = pygame.rect.Rect(enemy_difficulty_button_1.right + 10, enemy_difficulty_rect.y, SETTINGS_RECT_WIDTH, SETTINGS_RECT_HEIGHT)
enemy_difficulty_button_3 = pygame.rect.Rect(enemy_difficulty_button_2.right + 10, enemy_difficulty_rect.y, SETTINGS_RECT_WIDTH, SETTINGS_RECT_HEIGHT)


def main_menu(screen: pygame.Surface) -> int:
    """muestra el menu principal del juego

    Args:
        screen (pygame.Surface): _description_

    Returns:
        int: corresponde a un game state
    """
    game_state = STATE_MAIN_MENU
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GAME_EXIT

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_pos = event.pos
                if button_start.collidepoint(mouse_pos):
                    game_state = STATE_PLAYING
                elif button_quit.collidepoint(mouse_pos):
                    game_state = GAME_EXIT

                elif enemy_difficulty_button_1.collidepoint(mouse_pos):
                     difficulty_settings["enemy_difficulty"] = 3
                elif enemy_difficulty_button_2.collidepoint(mouse_pos):
                     difficulty_settings["enemy_difficulty"] = 2
                elif enemy_difficulty_button_3.collidepoint(mouse_pos):
                     difficulty_settings["enemy_difficulty"] = 1

                elif starting_lives_button_1.collidepoint(mouse_pos):
                    difficulty_settings["starting_lives"] = 3
                elif starting_lives_button_2.collidepoint(mouse_pos):
                    difficulty_settings["starting_lives"] = 2
                elif starting_lives_button_3.collidepoint(mouse_pos):
                    difficulty_settings["starting_lives"] = 1

 
    screen.fill("BLACK")

    pygame.draw.rect(screen, "GRAY", button_start)
    pygame.draw.rect(screen, "GRAY", button_quit)

    pygame.draw.rect(screen, "GRAY", enemy_difficulty_rect)
    pygame.draw.rect(screen, "green" if difficulty_settings["enemy_difficulty"] == 3 else "white", enemy_difficulty_button_1)
    pygame.draw.rect(screen, "yellow" if difficulty_settings["enemy_difficulty"] == 2 else "white", enemy_difficulty_button_2)
    pygame.draw.rect(screen, "red" if difficulty_settings["enemy_difficulty"] == 1 else "white", enemy_difficulty_button_3)


    pygame.draw.rect(screen, "GRAY", starting_lives_rect)
    pygame.draw.rect(screen, "green" if difficulty_settings["starting_lives"] == 3 else "white", starting_lives_button_1)
    pygame.draw.rect(screen, "yellow" if difficulty_settings["starting_lives"] == 2 else "white", starting_lives_button_2)
    pygame.draw.rect(screen, "red" if difficulty_settings["starting_lives"] == 1 else "white", starting_lives_button_3)


    start_text = FONT.render("Start Game", True, "BLACK")
    quit_text = FONT.render("Quit", True, "BLACK")
    screen.blit(start_text, (button_start.x + 30, button_start.y + 20))
    screen.blit(quit_text, (button_quit.x + 100, button_quit.y + 20))

    hi_score_text = FONT.render(f"Hi-Score: {scores[0]["score"]}", True, "GREEN")
    last_score_text = FONT.render(f"Last score: {scores[1]["score"]}", True, "GREEN")
    screen.blit(hi_score_text, hi_score_rect)
    screen.blit(last_score_text, last_score_rect)
    
    starting_lives_text = SETTINGS_FONT.render("Player lives:", True, "black")
    enemy_difficulty_text = SETTINGS_FONT.render("Enemy difficulty:", True, "black")
    screen.blit(starting_lives_text, (starting_lives_rect.left + 10, starting_lives_rect.top + 15))
    screen.blit(enemy_difficulty_text, (enemy_difficulty_rect.left + 10, enemy_difficulty_rect.top + 15))

    return game_state

