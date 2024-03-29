import random
import os
import pygame
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()

# Game const
FONT = pygame.font.SysFont("Helvetica", 30)
FPS = pygame.time.Clock()
HEIGHT = 800
WIDTH = 1200
COLOR_BLACK = (0, 0, 0)

# DISPLAY SIZE
main_display = pygame.display.set_mode((WIDTH, HEIGHT))


# Load images
enemy_size = (80, 40)
bonus_size = (120, 200)
player_size = (150, 70)
bg = pygame.transform.scale(pygame.image.load("img/background.png"), (WIDTH, HEIGHT))
enemy_img = pygame.transform.scale(
    pygame.image.load("img/enemy.png").convert_alpha(), (enemy_size[0], enemy_size[1])
)
bonus_img = pygame.transform.scale(
    pygame.image.load("img/bonus.png").convert_alpha(), (bonus_size[0], bonus_size[1])
)
player_img = pygame.transform.scale(
    pygame.image.load("img/player.png").convert_alpha(),
    (player_size[0], player_size[1]),
)


# Background move settings
bg_x1 = 0
bg_x2 = bg.get_width()
bg_move = 3

# Player animation flay settings
ANIM_PATH = "anim/GUSAK"
ANIM_PLAYER = os.listdir(ANIM_PATH)


# Player desc
player_sped = 5
player = player_img
player_rect = player.get_rect()
player_rect.x = WIDTH * 0.15
player_rect.y = HEIGHT / 2
player_move_down = [0, player_sped]
player_move_up = [0, -player_sped]
player_move_left = [-player_sped, 0]
player_move_right = [player_sped, 0]


# Enemy desc
def create_enemy():
    enemy_size = (80, 40)
    enemy = enemy_img
    enemy_rect = pygame.Rect(
        WIDTH, random.randint(int(HEIGHT * 0.2), int(HEIGHT * 0.8)), *enemy_size
    )
    enemy_move = [random.randint(-6, -4), 0]
    return [enemy, enemy_rect, enemy_move]


# Bonus desc
def create_bonus():
    bonus = bonus_img
    bonus_rect = pygame.Rect(
        random.randint(int(WIDTH * 0.4), int(WIDTH * 0.8)), 0, *bonus_size
    )
    bonus_move = [0, 1]
    return [bonus, bonus_rect, bonus_move]


CREATE_ENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(CREATE_ENEMY, 1500)

CREATE_BONUS = pygame.USEREVENT + 2
pygame.time.set_timer(CREATE_BONUS, 2000)

CHANGE_USER = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGE_USER, 100)

enemies = []
bonuses = []
score = 0
index_img = 0

# Game main mechanics
playing = True
while playing:
    FPS.tick(200)
    for event in pygame.event.get():
        if event.type == QUIT:
            playing = False
        if event.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if event.type == CREATE_BONUS:
            bonuses.append(create_bonus())
        if event.type == CHANGE_USER:
            player = pygame.image.load(os.path.join(ANIM_PATH, ANIM_PLAYER[index_img]))
            index_img += 1
            if index_img >= len(ANIM_PLAYER):
                index_img = 0

    bg_x1 -= bg_move
    bg_x2 -= bg_move

    if bg_x1 < -bg.get_width():
        bg_x1 = bg.get_width()

    if bg_x2 < -bg.get_width():
        bg_x2 = bg.get_width()

    main_display.blit(bg, (bg_x1, 0))
    main_display.blit(bg, (bg_x2, 0))

    # Move player on screen
    keys = pygame.key.get_pressed()
    if keys[K_DOWN] and player_rect.bottom < HEIGHT:
        player_rect = player_rect.move(player_move_down)

    if keys[K_UP] and player_rect.top > 0:
        player_rect = player_rect.move(player_move_up)

    if keys[K_LEFT] and player_rect.left > 0:
        player_rect = player_rect.move(player_move_left)

    if keys[K_RIGHT] and player_rect.right < WIDTH:
        player_rect = player_rect.move(player_move_right)

    for enemy in enemies:
        enemy[1] = enemy[1].move(enemy[2])
        main_display.blit(enemy[0], enemy[1])

        if player_rect.colliderect(enemy[1]):
            playing = False

    for bonus in bonuses:
        bonus[1] = bonus[1].move(bonus[2])
        main_display.blit(bonus[0], bonus[1])

        if player_rect.colliderect(bonus[1]):
            score += 1
            bonuses.pop(bonuses.index(bonus))

    main_display.blit(FONT.render(str(score), True, COLOR_BLACK), (WIDTH - 50, 20))
    main_display.blit(player, player_rect)

    pygame.display.flip()

    for enemy in enemies:
        if enemy[1].left < 0:
            enemies.pop(enemies.index(enemy))

    for bonus in bonuses:
        if bonus[1].top > HEIGHT:
            bonuses.pop(bonuses.index(bonus))
