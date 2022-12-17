import pygame as pg
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT
import math, os
from random import random

def read():
    try:
        with open('score.txt', 'r') as file:
            best_score = file.read()
            file.close()
    except Exception as ex:
        print(f'Error: {ex}')
    return int(best_score)

def write(score):
    try:
        with open('score.txt', 'w') as file:
            file.write(str(score))
            file.close()
        return True
    except Exception as ex:
        print(f'Error: {ex}')

def get_random(min, max):
    return math.floor(random() * (max - min)) + min

def setColor():
    c = []
    for i in range(0, 3):
        c.append(get_random(0, 255))

    return tuple(c)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 200)
YELLOW = (100, 100, 0)
GREEN = (0, 255, 0)

pg.init()

screen = width, height = 800, 600
surface = pg.display.set_mode(screen)
pg.display.set_caption("Strange game!")

score = 0
best_score = read()

font = pg.font.Font('freesansbold.ttf', 18)


ball = pg.Surface((20, 20))
ball.fill(WHITE)
b_rect = ball.get_rect()
b_speed = 5

isWorking = True
CREATE_ENEMY = pg.USEREVENT + 1
CREATE_BONUS = pg.USEREVENT + 2
pg.time.set_timer(CREATE_ENEMY, 1500)
pg.time.set_timer(CREATE_BONUS, 2000)


def create_enemy():
    enemy = pg.Surface((20, 20))
    enemy.fill(RED)
    e_rect = pg.Rect(width, get_random(0, height), *enemy.get_size())
    e_speed = get_random(2, 5)
    return [enemy, e_rect, e_speed]
def create_bonus():
    bonus = pg.Surface((20, 20))
    bonus.fill(GREEN)
    bonus_rect = pg.Rect(get_random(0, width), 0, *bonus.get_size())
    bonus_speed = get_random(2, 5)
    return [bonus, bonus_rect, bonus_speed]

enemies = []
bonuses = []

FPS = pg.time.Clock()
while isWorking:
    FPS.tick(120)
    for i in pg.event.get():
        if i.type == QUIT:
            write(best_score)
            isWorking = False
        if i.type == CREATE_ENEMY:
            enemies.append(create_enemy())
        if i.type == CREATE_BONUS:
            bonuses.append(create_bonus())

    keys = pg.key.get_pressed()
    
    if keys[K_DOWN] and not b_rect.bottom >= height:
       b_rect = b_rect.move(0, b_speed)
    if keys[K_UP] and not b_rect.top <= 0:
        b_rect = b_rect.move(0, -b_speed)
    if keys[K_RIGHT] and not b_rect.right >= width:
        b_rect = b_rect.move(b_speed, 0)
    if keys[K_LEFT] and not b_rect.left <= 0:
        b_rect = b_rect.move(-b_speed, 0)

    surface.fill(BLACK)
    surface.blit(ball, b_rect)
    
    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        surface.blit(enemy[0], enemy[1])

        if enemy[1].left < -30:
            enemies.pop(enemies.index(enemy))

        if b_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            score -= 1
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        surface.blit(bonus[0], bonus[1])
        
        if bonus[1].bottom > height + 30:
            bonuses.pop(bonuses.index(bonus))

        if b_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1
    score_text = font.render('Score: ' + str(score), True, WHITE, BLACK)
    text_rect = score_text.get_rect()
    text_rect.x = width - 150
    text_rect.y = 10
    if best_score < score:
        best_score = score
    
    best_text = font.render('Best score: ' + str(best_score), True, WHITE, BLACK)
    best_rect = best_text.get_rect()
    best_rect.x = width - 150
    best_rect.y = 40

    surface.blit(best_text, best_rect)
    surface.blit(score_text, text_rect)
    pg.display.flip()