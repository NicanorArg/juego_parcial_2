import pygame
import USEREVENTS
from persistant_data import *
from random import randint
from functions import *
from settings import *

death_sound = pygame.mixer.Sound("src/sounds/enemy_death.ogg")
death_sound.set_volume(0.5)
grunt_fire_sound = pygame.mixer.Sound("src/sounds/grunt_fire.ogg")
grunt_fire_sound.set_volume(0.5)
flooder_fire_sound = pygame.mixer.Sound("src/sounds/flooder_fire.ogg")
flooder_fire_sound.set_volume(0.5)

GRUNT_HEIGHT = 15
GRUNT_WIDTH = 15
GRUNT_SPEED = 5
GRUNT_BULLET_SPEED = 5
GRUNT_BULLET_DELAY = 150 

BULLET_WIDTH = 15

grunt_img = pygame.image.load("src/graphics/grunt.png")
grunt_img = pygame.transform.scale(grunt_img, (GRUNT_WIDTH, GRUNT_HEIGHT))
grunt_bullet_img = pygame.image.load("src/graphics/grunt_bullet.png")
grunt_bullet_img = pygame.transform.scale(grunt_bullet_img, (15, 15))

FLOODER_HEIGHT = 30
FLOODER_WIDTH = 30
FLOODER_SPEED = 5
FLOODER_BULLET_DELAY = 100
FLOODER_BULLET_SPEED = 2
FLOODER_INITIAL_OBJECTIVE = (WIDTH, HEIGHT)
FLOODER_AIM_CHANGE = 87

flooder_img = pygame.image.load("src/graphics/flooder.png")
flooder_img = pygame.transform.scale(flooder_img, (FLOODER_WIDTH, FLOODER_HEIGHT))
flooder_bullet_img = pygame.image.load("src/graphics/flooder_bullet.png")
flooder_bullet_img = pygame.transform.scale(flooder_bullet_img, (15, 15))


LEFT_FLOODER_X = -40
LEFT_FLOODER_Y = -40
LEFT_FLOODER_DESTINATION = (60, HEIGHT // 4)

RIGHT_FLOODER_X = WIDTH + 10
RIGHT_FLOODER_Y = - 40
RIGHT_FLOODER_DESTINATION = (WIDTH - 60, HEIGHT // 4)

CENTER_FLOODER_X = WIDTH // 2
CENTER_FLOODER_Y = - 40
CENTER_FLOODER_DESTINATION = (CENTER_FLOODER_X, HEIGHT // 4)

def spawn_grunt_wave(grunt_ammoun: int, x_coordinate: int, y_coordinate: int, spacing: int) -> list[pygame.rect.Rect]:
    """crea un grupo de enemigos basicos(grunt) en una lista

    Args:
        grunt_ammoun (int): cantidad de grunts
        x_coordinate (int): coordenada x del spawn
        y_coordinate (int): coordenada y del spawn
        spacing (int): espacio entre grunts

    Returns:
        list[pygame.rect.Rect]: grunts
    """
    grunts = []
    starting_x = x_coordinate

    for _ in range(grunt_ammoun):
        grunt = pygame.rect.Rect(starting_x, y_coordinate, GRUNT_WIDTH, GRUNT_HEIGHT)
        grunts.append(grunt)
        starting_x -= spacing
    
    return grunts

def create_enemy_bullet(enemy: pygame.rect.Rect, bullet_list: list[pygame.rect.Rect], objective: tuple[int, int], speed: int) -> None:
    """crea un diccionario bullet con los datos necesarios para trazar una trayectoria hacia su objetivo, la bullet es agregada a una lista proporiconada

    Args:
        enemy (pygame.rect.Rect): dispara la bullet
        bullet_list (list[pygame.rect.Rect]): lista a guardar la bullet
        objective (tuple[int, int]): objetivo para calcular la trayectoria de la bullet
        speed (int): velocidad de movimiento de la bullet
    """
    bullet = {}
    bullet["rect"] = pygame.rect.Rect(0, 0, BULLET_WIDTH, BULLET_WIDTH)
    bullet["rect"].center = enemy.center
    bullet["velocities"] = set_rect_trajectory(enemy.center, objective, speed)
    bullet["floating_x_coordinate"] = bullet["rect"].x
    bullet["floating_y_coordinate"] = bullet["rect"].y
    bullet_list.append(bullet)

def spawn_grunt_bullets(grunts: list[pygame.rect.Rect], bullet_list: list[dict], player: pygame.rect.Rect) -> None:
    """por cada grunt en la lista proporcionada, crea una bala cuya trayectoria es una linea trazada desde el grunt hacia la posicion del jugador al momento de llamada de esta funcion y la apendea en una lista parametro

    Args:
        grunts (list[pygame.rect.Rect]): lista de grunts
        bullet_list (list[dict]): lista para apendear las balas
        player (pygame.rect.Rect): player, objetivo de la bala
    """
    for grunt in grunts:
        if not out_of_bounds(grunt):
            grunt_fire_sound.play()
            create_enemy_bullet(grunt, bullet_list, player.center, GRUNT_BULLET_SPEED)

def find_in_list(element: any, list: list[any]) -> bool:
    """verifica si un elemento se encuentra en la lista pasada com parametro

    Args:
        element (any): elemento a encontrar
        list (list[any]): lista a buscar

    Returns:
        bool: resultado de la busqueda
    """
    for list_element in list:
        if list_element == element:
            return True
    return False

def grunt_behaviour(screen_surfae: pygame.Surface, grunts: list[pygame.rect.Rect], grunt_bullets: list[dict], player_bullets: list[pygame.rect.Rect], player_homing_bullets: list[dict], move_right: bool = True) -> None:
    """acciona los comportamientos basicos de los enemigos grunts y de sus balas (movimiento, dibujado, muerte, desespawneo)

    Args:
        screen_surfae (pygame.Surface): superficie sobre la que se dibujan los elementos
        grunts (list[pygame.rect.Rect]): lista de grunts
        grunt_bullets (list[dict]): balas de los grunts
        player_bullets (list[pygame.rect.Rect]): balas disparadas por el jugador
        move_right (bool, optional): Define la direccion del grunt. Defaults to True.
    """
    grunts_to_remove = []
    player_bullets_to_remove = []
    player_homing_bullets_to_remove = []

    # movimiento y dibujado de grunts
    for grunt in grunts:
        if move_right:
            grunt.x += GRUNT_SPEED
            if grunt.left > WIDTH:
                grunts.remove(grunt)
        else:
            grunt.x -= GRUNT_SPEED
            if grunt.right < 0:
                grunts.remove(grunt)
        img_rect = grunt_img.get_rect()
        img_rect.center = grunt.center
        screen_surfae.blit(grunt_img, img_rect)
        
        # deteccion de colision y guardado para eliminacion
        for bullet in player_bullets:
            if bullet.colliderect(grunt) and not find_in_list(grunt, grunts_to_remove):
                grunts_to_remove.append(grunt)
                player_bullets_to_remove.append(bullet)
        for bullet in player_homing_bullets:
            if bullet["rect"].colliderect(grunt) and not find_in_list(grunt, grunts_to_remove):
                grunts_to_remove.append(grunt)
                player_homing_bullets_to_remove.append(bullet)

    # eliminacion de elementos que hicieron colision
    for grunt in grunts_to_remove:
        grunts.remove(grunt)
        death_sound.play()
        scores[1]["score"] += 1
    for bullet in player_bullets_to_remove:
        player_bullets.remove(bullet)
    for bullet in player_homing_bullets_to_remove:
        player_homing_bullets.remove(bullet)

    # movimiento y dibujado de bullets, eliminacion de las que se salen de la pantalla
    for bullet in grunt_bullets.copy():
        move_rect_in_trajectory(bullet)
        img_rect = grunt_bullet_img.get_rect()
        img_rect.center = bullet["rect"].center
        screen_surfae.blit(grunt_bullet_img, img_rect)

        if out_of_bounds(bullet["rect"]):
            grunt_bullets.remove(bullet)

def spawn_flooder(x_coordinate: int, y_coordinate: int, destiny: tuple[int, int]) -> dict:
    """crea un diccionario con los datos del enemigo de tipo flooder

    Args:
        x_coordinate (int): coordenada x de spawneo(left)
        y_coordinate (int): coordenada y de spawneo(top)
        destiny (tuple[int, int]): coordenadas del punto al que el flooder se movera(center)

    Returns:
        dict: enemigo flooder
    """
    flooder = {}
    flooder["rect"] = pygame.rect.Rect(x_coordinate, y_coordinate, FLOODER_WIDTH, FLOODER_HEIGHT)
    flooder["floating_x_coordinate"] = x_coordinate
    flooder["floating_y_coordinate"] = y_coordinate
    flooder["destiny"] = destiny
    flooder["velocities"] = set_rect_trajectory(flooder["rect"].center, destiny, FLOODER_SPEED)
    flooder["x_objective"] = randint(0, WIDTH)
    flooder["health"] = 100
    flooder["arrived"] = False
    return flooder

def spawn_left_flooder() -> dict:
    """crea un flooder que aparece del lado izquierdo de la pantalla

    Returns:
        dict: enemigo del tipo flooder
    """
    left_flooder = spawn_flooder(LEFT_FLOODER_X, LEFT_FLOODER_Y, LEFT_FLOODER_DESTINATION)
    left_flooder["type"] = "left"
    pygame.time.set_timer(USEREVENTS.SPAWN_LEFT_FLOODER, 0)
    return left_flooder 

def spawn_right_flooder() -> dict:
    """crea un flooder que aparece del lado derecho de la pantalla

    Returns:
        dict: enemigo del tipo flooder
    """
    right_flooder = spawn_flooder(RIGHT_FLOODER_X, RIGHT_FLOODER_Y, RIGHT_FLOODER_DESTINATION)
    right_flooder["type"] = "right"
    pygame.time.set_timer(USEREVENTS.SPAWN_RIGHT_FLOODER, 0)
    return right_flooder 

def spawn_center_flooder() -> dict:
    """crea un flooder que aparece del lado central de la pantalla

    Returns:
        dict: enemigo del tipo flooder
    """
    center_flooder = spawn_flooder(CENTER_FLOODER_X, CENTER_FLOODER_Y, CENTER_FLOODER_DESTINATION)
    center_flooder["type"] = "center"
    pygame.time.set_timer(USEREVENTS.SPAWN_CENTER_FLOODER, 0)
    return center_flooder 

def spawn_flooder_bullet(flooders: list[dict], flooder_bullet_list: list[dict]) -> None:
    """por cada flooder que exista, si este llego a su destino, una bala que se dirigira a un punto definido por el atributo ["x_objective"] del flooder; esta es guardada dentro de la lista de balas dada como parametro

    Args:
        flooders (list[dict]): diccionario que contiene la informacion del flooder
        flooder_bullet_list (list[dict]): lista de balas disparadas por los flooders
    """
    for flooder in flooders:
        if flooder["arrived"]:
            flooder_fire_sound.play()
            create_enemy_bullet(flooder["rect"], flooder_bullet_list, (flooder["x_objective"], HEIGHT), FLOODER_BULLET_SPEED)

def control_flooder_aim(flooders: list[dict], aim_left: bool) -> bool:
    """mueve la coordenada x del objetivo al que cada flooder dentro de la lista esta apuntando una cantidad de pixeles segun la constante FLOODER_AIM_CHANGE

    Args:
        flooders (list[dict]): lista de flooders
        aim_left (bool): determina la direccion hacia la que el objetivo es movido

    Returns:
        bool: para volver a pasar a esta funcion como parametro aim_left
    """
    for flooder in flooders:    
        flooder_x_aim = flooder["x_objective"]
        if flooder_x_aim >= WIDTH:
            aim_left = True
        elif flooder_x_aim <= 0:
            aim_left = False
            
        if aim_left:
            flooder["x_objective"] -= FLOODER_AIM_CHANGE
        else:
            flooder["x_objective"] += FLOODER_AIM_CHANGE

    return aim_left

def flooder_behaviour(flooders: list[dict], flooder_bullets: list[dict], screen_surface: pygame.surface, player_bullets: list[pygame.rect.Rect], player_homing_bullets: list[dict]) -> None:
    """funcion que centraliza y controla el comportamiento de los flooders y de sus balas; los mueve, dibuja, y elimina cuando es necesario.

    Args:
        flooders (list[dict]): lista de flooders
        flooder_bullets (list[dict]): lista de balas disparadas por los flooders
        screen_surface (pygame.surface): superficie sobre la cual se dibujan los flooders
        player_bullets (list[pygame.rect.Rect]): balas del player para chequear colisiones
    """

    flooders_to_remove = []
    bullets_to_remove = []
    homing_bullets_to_remove = []
    # movimiento de las balas, eliminacion si se pasan de los limites de la pantalla
    for bullet in flooder_bullets.copy():
        move_rect_in_trajectory(bullet)
        img_rect = flooder_bullet_img.get_rect()
        img_rect.center = bullet["rect"].center
        screen_surface.blit(flooder_bullet_img, img_rect)
        if out_of_bounds(bullet["rect"]):
            flooder_bullets.remove(bullet)

    # movimiento de los flooders hacia su punto destino (son frenados al alcanzarlo)
    for flooder in flooders:
        arrived = move_rect_to_point(flooder)
        img_rect = flooder_img.get_rect()
        img_rect.center = flooder["rect"].center
        screen_surface.blit(flooder_img, img_rect)
        if arrived:
            flooder["destiny"] = None
            flooder["arrived"] = True
        
        
        for bullet in player_bullets:
            if flooder["rect"].colliderect(bullet):
                flooder["health"] -= 2
                bullets_to_remove.append(bullet)
        
        for bullet in player_homing_bullets:
            if flooder["rect"].colliderect(bullet["rect"]):
                flooder["health"] -= 2
                homing_bullets_to_remove.append(bullet)

        # mata al flooder si su vida llega a 0, lanza un timer para respawnear al flooder correspondiente
        if flooder["health"] <= 0:
            flooders_to_remove.append(flooder)
            match flooder["type"]:
                case "left":
                    pygame.time.set_timer(USEREVENTS.SPAWN_LEFT_FLOODER, randint(10000, 30000))
                case "right":
                    pygame.time.set_timer(USEREVENTS.SPAWN_RIGHT_FLOODER, randint(10000, 30000))
                case "center":
                    pygame.time.set_timer(USEREVENTS.SPAWN_CENTER_FLOODER, randint(10000, 30000))

    # elimina balas y flooders que fueron guardados para ser removidos
    for flooder in flooders_to_remove:
        death_sound.play()
        flooders.remove(flooder)
        scores[1]["score"] += 40
    for bullet in bullets_to_remove:
        player_bullets.remove(bullet)
    for bullet in homing_bullets_to_remove:
        player_homing_bullets.remove(bullet)
