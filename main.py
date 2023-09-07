import random
import pygame
import os
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE = (0, 0, 255)
COLOR_YELLOW = (255, 255, 0)
COLOR_RED = (255, 0, 0)

pygame.init()

FPS = pygame.time.Clock()
FPS.tick(60)

HEIGHT = 800
WIDTH = 1200

FONT = pygame. font.SysFont ('Verdana', 50)

main_display = pygame.display.set_mode((WIDTH, HEIGHT))

bg = pygame.transform.scale(pygame.image.load('background.png'), (WIDTH, HEIGHT))
bg_X1 = 0
bg_X2 = bg.get_width()
bg_move = 3

IMAGE_PATH = "Goose"
PLAYER_IMAGES = os.listdir(IMAGE_PATH)

player_size = (20, 20)
player = pygame.image.load('player.png').convert_alpha()
player_rect = player.get_rect()
player_move_down = [0, 4]
player_speed_right = [4, 0]
player_move_left = [-4, 0]
player_move_up = [0, -4]

bonus_size = (20, 20)
bonus_speed = [0, 3]
bonuses = []

def create_enemy():
    enemy_image = pygame.image.load('enemy.png').convert_alpha()
    enemy_rect = enemy_image.get_rect()
    enemy_rect.x = WIDTH
    enemy_rect.y = random.randint(0, HEIGHT)
    enemy_move = [random.randint(-8, -4), 0]
    return [enemy_image, enemy_rect, enemy_move]

def create_bonus():
    bonus_image = pygame.image.load('bonus.png').convert_alpha()
    bonus_rect = bonus_image.get_rect()
    bonus_rect.x = random.randint(0, WIDTH - bonus_rect.width)
    bonus_rect.y = -bonus_rect.height
    bonus_move = [0, random.randint(4, 8)]
    return [bonus_image, bonus_rect, bonus_move]

CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)
CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 3000)
CHANGE_IMAGE = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_IMAGE, 200)

enemies = []
bonuses = []

score = 0

image_index = 0

playing = True
game_over = False

while playing:
    FPS.tick(120)

    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
           enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
               bonuses.append(create_bonus())
        if event.type == CHANGE_IMAGE:
            player = pygame.image.load(os.path.join(IMAGE_PATH, PLAYER_IMAGES[image_index]))
            image_index += 1
            if image_index >= len(PLAYER_IMAGES):
                image_index = 0

    bg_X1 -= bg_move
    bg_X2 -= bg_move

    if bg_X1 < -bg.get_width():
        bg_X1 = bg.get_width()

    if bg_X2 < -bg.get_width():
        bg_X2 = bg.get_width()

    main_display.blit(bg, (bg_X1, 0))
    main_display.blit(bg, (bg_X2, 0))

    keys = pygame.key.get_pressed()

    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
       player_rect = player_rect.move(player_move_down)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_speed_right)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False
            game_over = True

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus_speed)
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    if game_over:
        game_over_text = FONT.render("Game Over", True, COLOR_RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        main_display.blit(game_over_text, game_over_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))
