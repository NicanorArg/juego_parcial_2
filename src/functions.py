import pygame
import USEREVENTS
from random import randint
from settings import *


bullet_sound = pygame.mixer.Sound("src/sounds/player_fire.ogg")
bullet_sound.set_volume(0.5)
homing_bullet_sound = pygame.mixer.Sound("src/sounds/homing_bullet.ogg")
homing_bullet_sound.set_volume(0.5)
death_sound = pygame.mixer.Sound("src/sounds/player_death.ogg")
death_sound.set_volume(0.5)


PJ_HEIGHT = 5
PJ_WIDTH = 5
player_image = pygame.image.load("src/graphics/ship.png")

BULLET_HEIGHT = 21
BULLET_WIDTH = 10
BULLET_SPEED = 10
bullet_img = pygame.image.load("src/graphics/bullet.png")
bullet_img = pygame.transform.scale(bullet_img, (BULLET_WIDTH , BULLET_HEIGHT))
homing_bullet_img = pygame.image.load("src/graphics/homing_bullet.png")
homing_bullet_img = pygame.transform.scale(homing_bullet_img, (BULLET_WIDTH * 3, BULLET_WIDTH * 3))

PICKUP_Y = -40
PICKUP_WIDTH = 20
PICKUP_HEIGHT = 20
PICKUP_SPEED = 1
PICKUP_DELAY_LOWER_RANGE = 40000
PICKUP_DELAY_UPPER_RANGE = 60000

pickup_img = pygame.image.load("src/graphics/power_up.png")
pickup_img = pygame.transform.scale(pickup_img, (PICKUP_WIDTH, PICKUP_HEIGHT))

def set_movement_flags(keys: list[bool]) -> tuple[bool, bool, bool, bool]:
    """devuelve una tupla de banderas asociadas a las direcciones apretadas por el jugador

    Args:
        keys (list[bool]): lista de 

    Returns:
        tuple[bool, bool, bool, bool]: direcciones: (arriba, abajo, izquierda, derecha)
    """
    move_up, move_down, move_left, move_right = keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]

    return (move_up, move_down, move_left, move_right)

def move_player_rect(player_rect: pygame.rect.Rect) -> None:
    """mueve al jugador en la direccion que el jugador apriete

    Args:
        player_rect (pygame.rect.Rect): rectangulo del jugador
    """
    keys = pygame.key.get_pressed()
    NORMAL_SPEED = 5
    SLOW_SPEED = 2
    if keys[pygame.K_LSHIFT]:
        speed = SLOW_SPEED
    else:
        speed = NORMAL_SPEED

    
    movement_flags = set_movement_flags(keys)
    
    if movement_flags[0]:   player_rect.y -= speed
    if movement_flags[1]:   player_rect.y += speed
    if movement_flags[2]:   player_rect.x -= speed
    if movement_flags[3]:   player_rect.x += speed

def control_player_movement_bounds(player_rect: pygame.rect.Rect) -> None:
    """reposiciona el rectangulo del jugador si este se sale de los bordes de la pantalla

    Args:
        player_rect (pygame.rect.Rect): rectangulo del jugador
    """

    if player_rect.left < 10:
        player_rect.left = 10
    elif player_rect.right > WIDTH -10:
        player_rect.right = WIDTH - 10

    if player_rect.top < 10:
        player_rect.top = 10
    elif player_rect.bottom > HEIGHT - 10:
        player_rect.bottom = HEIGHT - 10

def create_player_bullets(player_rect: pygame.rect.Rect, bullets: list[pygame.rect.Rect]) -> None:
    """crea dos balas disparadas por el jugador si este oprime la barra de espacio; son apendeadas a la lista proporcionada

    Args:
        player_rect (pygame.rect.Rect): rectangulo del jugador
        bullets (list[pygame.rect.Rect]): lista en la que las balas son guardadas
    """
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        bullet_sound.play()
        bullet1 = pygame.rect.Rect(player_rect.x - BULLET_WIDTH, player_rect.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
        bullet2 = pygame.rect.Rect(player_rect.right, player_rect.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)

        bullets.append(bullet1)
        bullets.append(bullet2)

def move_bullet(bullet: pygame.rect.Rect) -> None:
    """reposiciona la bala una cantidad de pixeles en el eje y segun la constante BULLET_SPEED

    Args:
        bullet (pygame.rect.Rect): bala a reposicionar
    """
    bullet.y -= BULLET_SPEED

def draw_bullet(bullet: pygame.rect.Rect, Surface: pygame.Surface) -> None:
    """dibuja la bala pasada como parametro en la superficie especificada

    Args:
        bullet (pygame.rect.Rect): rectangulo de la bala
        Surface (pygame.Surface): superficie sobre la que dibujarla
    """
    pygame.draw.rect(Surface, "yellow", bullet)

def player_fire(bullets: list[pygame.rect.Rect], surface: pygame.Surface) -> None:
    """funcion que centraliza y controla el comportamiento de las balas dibujadas por el jugador: las mueve, dibuja, y las elimina cuando estas superan el limite superior de la pantalla

    Args:
        bullets (list[pygame.rect.Rect]): lista que contiene las balas que el jugador ha disparado
        surface (pygame.Surface): superficie sobre la que dibujar las balas
    """
    if len(bullets) > 0 and bullets[0].bottom < 0:
        bullets.remove(bullets[0])

    for bullet in bullets:
        move_bullet(bullet)
        img_rect = bullet_img.get_rect()
        img_rect.center = bullet.center
        surface.blit(bullet_img, img_rect)
    
def player_gets_hit(player_rect: pygame.rect.Rect, bullets: list[dict]) -> bool:
    """chequea si el jugador es impactado por alguna de las balas de la lista proporcionada

    Args:
        player_rect (pygame.rect.Rect): rectangulo del jugador
        bullets (list[dict]): lista que contiene balas disparadas por los enemigos

    Returns:
        bool: True si hay impacto, de otra manera False
    """
    if len(bullets) > 0:
        for bullet in bullets:
            if calculate_diagonal_distance(player_rect.center, bullet["rect"].center) < player_rect.width + bullet["rect"].width:
                death_sound.play()
                return True
    return False

def calculate_diagonal_distance(point_1: tuple[int, int], point_2: tuple[int, int]) -> float:
    """calcula la distancia entre dos coordenadas dadas

    Args:
        point_1 (tuple[int, int]): coordenada 1 (x, y)
        point_2 (tuple[int, int]): coordenada 2 (x, y)

    Returns:
        float: distancia entre las coordenadas
    """
    x_distance = point_1[0] - point_2[0]
    y_distance = point_1[1] - point_2[1]
    return (x_distance ** 2 + y_distance ** 2) ** (1/2)

def set_rect_trajectory(origin: tuple[int, int], objective: tuple[int, int], speed: int) -> tuple[float, float]:
    """calcula las velocidades x e y necesarias para que un rectangulo se mueva en una trayectoria a una aproximacion de la velocidad dada

    Args:
        origin (tuple[int, int]): punto de origen de la trayectoria
        objective (tuple[int, int]): punto 2 que el vector atraviesa (a no confundir con punto final)
        speed (int): velocidad diagonal esperada

    Returns:
        tuple[float, float]: valores de x e y por los que un rectangulo tendria que ser modificado cada tick para moverse en la direccion deseada a la velocidad dada
    """

    diagonal_distance = calculate_diagonal_distance(objective, origin)
    try:
        percentage_of_speed = 1 / diagonal_distance * speed
    except ZeroDivisionError:
        percentage_of_speed = 0
    x_speed = (objective[0] - origin[0]) * percentage_of_speed
    y_speed = (objective[1] - origin[1]) * percentage_of_speed

    return (x_speed, y_speed)

def move_rect_in_trajectory(rect_dict: dict) -> None:
    """mueve un rect en una trayectoria segun las velocidades indicadas

    Args:
        rect (pygame.rect.Rect): rectangulo a mover
        floating_X_coordinate (float): valor x exacto del rectangulo
        floating_y_coordinate (float): valor y exacto del rectangulo
        velocities (tuple[float, float]): velocidades x e y que forman la trayectoria del rectangulo

    """
    velocities = rect_dict["velocities"]
    rect_dict["floating_x_coordinate"] += velocities[0]
    rect_dict["floating_y_coordinate"] += velocities[1]
    rect_dict["rect"].x = round(rect_dict["floating_x_coordinate"])
    rect_dict["rect"].y = round(rect_dict["floating_y_coordinate"])

def out_of_bounds(rect: pygame.rect.Rect) -> bool:
    """chequea si el rectangulo proporcionado como parametro se salió de los limites de la pantalla

    Args:
        rect (pygame.rect.Rect): rectangulo a chequear

    Returns:
        bool: True si el rect esta fuera de la pantalla, en otro caso False
    """
    return rect.left > WIDTH or rect.right < 0 or rect.bottom > HEIGHT or rect.top < 0

def player_collision(player: pygame.rect.Rect, enemy_bullet: pygame.rect.Rect) -> bool:
    """chequea colisiones entre el jugador y la bala proporcionada como parametro. *PENSADO PARA ELEMENTOS DIBUJADOS COMO CIRCULOS*

    Args:
        player (pygame.rect.Rect): rectangulo del jugador
        enemy_bullet (pygame.rect.Rect): rectangulo de la bala

    Returns:
        bool: True si hay colision, de otra manera False
    """
    distance = calculate_diagonal_distance(player.center, enemy_bullet.center)
    return distance < player.width + enemy_bullet.width
    
def move_rect_to_point(rect_dict: dict) -> bool:
    """mueve un rectangulo dentro de un diccionario hacia un punto hasta que estos colisionan

    Args:
        rect_dict (dict): diccionario que contiene un rect dentro de la key ["rect"] y un destino guardado en ["destiny"]

    Returns:
        bool: True si llego a su destino, en otro caso False
    """
    if rect_dict["destiny"]:
        arrived = rect_dict["rect"].collidepoint(rect_dict["destiny"][0], rect_dict["destiny"][1])
        if not arrived:
            move_rect_in_trajectory(rect_dict)
    else:
        arrived = False
    return arrived

def find_closest_enemy(rect: pygame.rect.Rect, enemies: list[any]) -> pygame.rect.Rect:
    """encuentra al enemigo mas cercano al rect. en caso de no haber ninguno retorna None

    Args:
        player_rect (pygame.rect.Rect): rectangulo desde el cual medir
        enemies (list[any]): lista de todos los enemigos (grunts son rect, flooders son dicts)

    Returns:
        pygame.rect.Rect: rectangulo del enemigo mas cercano
    """
    first_loop = True
    if len(enemies) > 0:
        for enemy in enemies:
            if isinstance(enemy, dict):
                distance = calculate_diagonal_distance(rect.center, enemy["rect"].center)
                if first_loop or distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy["rect"]
                first_loop = False

            elif isinstance(enemy, pygame.rect.Rect):
                distance = calculate_diagonal_distance(rect.center, enemy.center)
                if first_loop or distance < min_distance:
                    min_distance = distance
                    closest_enemy = enemy
                first_loop = False
        return closest_enemy
    else:
        return None

def create_homing_bullets(player_rect: pygame.rect.Rect, enemies: list[any], homing_bullets: list[pygame.rect.Rect]) -> None:
    """crea dos balas guiadas desde los costados del jugador y las guarda en una lista dada

    Args:
        player_rect (pygame.rect.Rect): rect del jugador
        enemies (list[any]): lista de enemigos para encontrar el objetivo de la bala
        homing_bullets (list[pygame.rect.Rect]): lista para almacenar las balas
    """
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        homing_bullet_sound.play()
        bullet_1 = {}
        bullet_1["rect"] = pygame.rect.Rect(player_rect.x - round(BULLET_WIDTH * 2.5), player_rect.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
        bullet_1["floating_x_coordinate"] = bullet_1["rect"].x
        bullet_1["floating_y_coordinate"] = bullet_1["rect"].y
        closest_rect = find_closest_enemy(bullet_1["rect"], enemies)
        if closest_rect != None:
            bullet_1["destiny"] = closest_rect.center
            bullet_1["velocities"] = set_rect_trajectory(bullet_1["rect"].center, bullet_1["destiny"], BULLET_SPEED)
        else:
            bullet_1["destiny"] = closest_rect

        bullet_2 = {}
        bullet_2["rect"] = pygame.rect.Rect(player_rect.x + round(BULLET_WIDTH * 2), player_rect.y - BULLET_HEIGHT, BULLET_WIDTH, BULLET_HEIGHT)
        bullet_2["floating_x_coordinate"] = bullet_2["rect"].x
        bullet_2["floating_y_coordinate"] = bullet_2["rect"].y
        closest_rect = find_closest_enemy(bullet_2["rect"], enemies)
        if closest_rect != None:
            bullet_2["destiny"] = closest_rect.center
            bullet_2["velocities"] = set_rect_trajectory(bullet_2["rect"].center, bullet_2["destiny"], BULLET_SPEED)
        else:
            bullet_2["destiny"] = closest_rect

        homing_bullets.append(bullet_1)
        homing_bullets.append(bullet_2)

def homing_bullets_behaviour(screen: pygame.Surface, homing_bullets: list[dict], enemies: list[any]) -> None:
    """mueve las balas hacia el objetivo mas cercano, o arriba en caso de haber ninguno

    Args:
        screen (pygame.Surface): superficie sobre la que dibujar las balas
        homing_bullets (list[dict]): lista de balas guiadas
        enemies (list[any]): lista de enemigos, grunts son rects y flooders son dicts
    """
    bullets_to_remove = []
    for bullet in homing_bullets:
        if bullet["destiny"] != None:
            move_rect_in_trajectory(bullet)
        else:
            bullet["rect"].y -= BULLET_SPEED
            bullet["floating_x_coordinate"] = bullet["rect"].x
            bullet["floating_y_coordinate"] = bullet["rect"].y
        img_rect = homing_bullet_img.get_rect()
        img_rect.center = bullet["rect"].center
        screen.blit(homing_bullet_img, img_rect)
        closest_rect = find_closest_enemy(bullet["rect"], enemies)
        if closest_rect != None:
            bullet["destiny"] = closest_rect.center
            bullet["velocities"] = set_rect_trajectory(bullet["rect"].center, bullet["destiny"], BULLET_SPEED)
        else:
            bullet["destiny"] = closest_rect

        if out_of_bounds(bullet["rect"]):
            bullets_to_remove.append(bullet)
    
    for bullet in bullets_to_remove:
        homing_bullets.remove(bullet)

def spawn_pickup() -> pygame.rect.Rect:
    """retorna un rectangulo pickup, que sera usado para que el jugador lo agarre y obtenga un powerup

    Returns:
        pygame.rect.Rect: _description_
    """
    pickup = pygame.rect.Rect(randint(0, WIDTH - PICKUP_WIDTH), PICKUP_Y, PICKUP_WIDTH, PICKUP_HEIGHT)
    pygame.time.set_timer(USEREVENTS.SPAWN_PICKUP ,randint(PICKUP_DELAY_LOWER_RANGE, PICKUP_DELAY_UPPER_RANGE))
    return pickup

def pickup_movement(pickup: pygame.rect.Rect, screen: pygame.Surface, player_rect: pygame.rect.Rect) -> None:
    """mueve y muestra al pickup

    Args:
        pickup (pygame.rect.Rect): pickup
        screen (pygame.Surface): superficie sobre la que se muestra
        player_rect (pygame.rect.Rect): ¿rectangulo del jugador
    """
    pickup.y += PICKUP_SPEED
    img_rect = pickup_img.get_rect()
    img_rect.center = pickup.center
    screen.blit(pickup_img, img_rect)

def pickup_behaviour(pickups: list[pygame.rect.Rect], player_rect: pygame.rect.Rect, screen: pygame.Surface, power_up_flag: bool) -> bool:
    """controla el comportamiento del pickup: lo mueve hacia abajo y en caso de colisionar con el jugador lo elimina y lanza la una bandera para que el powerup sea activado

    Args:
        pickups (list[pygame.rect.Rect]): lista de pickups
        player_rect (pygame.rect.Rect): rectangulo del jugador
        screen (pygame.Surface): superficie de pantalla
        power_up_flag (bool): bandera del powerup

    Returns:
        bool: bandera del powerup procesada
    """
    for pickup in pickups.copy():
        pickup_movement(pickup, screen, player_rect)
        if pickup.top > HEIGHT + pickup.width or calculate_diagonal_distance(player_rect, pickup) < pickup.width + player_rect.width:
            pickups.remove(pickup)
            power_up_flag = True
            pygame.time.set_timer(USEREVENTS.END_OF_POWERUP, 60000)
    return power_up_flag


        
