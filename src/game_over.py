import pygame
from persistant_data import *
from settings import *

def game_over(screen: pygame.Surface):
    screen.fill("BLACK")

    font = pygame.font.Font(None, 64)
    text_surface = font.render("Game Over", True, "WHITE")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 4))
    screen.blit(text_surface, text_rect)

    font = pygame.font.Font(None, 32)
    text_surface = font.render("Press backspace to return to main menu", True, "WHITE")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
    screen.blit(text_surface, text_rect)

    score_text = f"Your score: {scores[1]['score']}"
    text_surface = font.render(score_text, True, "WHITE")
    text_rect = text_surface.get_rect(center=(WIDTH // 2, (HEIGHT // 2) + 40))
    screen.blit(text_surface, text_rect)

    pygame.display.flip()

    game_state = STATE_GAME_OVER
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_state = GAME_EXIT
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                game_state = STATE_MAIN_MENU

    return game_state

