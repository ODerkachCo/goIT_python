import pygame as pg
from pygame.constants import QUIT, K_DOWN, K_UP, K_RIGHT, K_LEFT, K_w, K_s, K_d, K_a
import math, os
from random import random

def check_file():
    isFile = os.path.exists('score.txt')
    if not isFile:
        try:
            with open('score.txt', 'w+') as file:
                file.write('0')
                file.close()
        except Exception as ex:
            print(f'Error: {ex}')
            return False
    return True
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
GREEN = (0, 100, 0)

pg.init()

screen = width, height = 800, 600
surface = pg.display.set_mode(screen)
pg.display.set_caption("Strange game!")

score = 0
isFile = check_file()
if isFile:
    best_score = read()

font = pg.font.Font('freesansbold.ttf', 18)
GOOSE_PATH = "./imgs/goose"
player_imgs = [pg.image.load(f'{GOOSE_PATH}/{file}').convert_alpha() for file in os.listdir(GOOSE_PATH)]
player = player_imgs[0]
p_rect = player.get_rect()
p_speed = 5

bg = pg.transform.scale(pg.image.load("./imgs/background.png").convert(), screen)
bg_start = 0
bg_finish = bg.get_width()
bg_speed = 3

isWorking = True
CREATE_ENEMY = pg.USEREVENT + 1
CREATE_BONUS = pg.USEREVENT + 2
CHANGE_IMG = pg.USEREVENT + 3
pg.time.set_timer(CREATE_ENEMY, 1500)
pg.time.set_timer(CREATE_BONUS, 2000)
pg.time.set_timer(CHANGE_IMG, 125)

def create_enemy():
    enemy = pg.image.load("./imgs/enemy.png").convert_alpha()
    e_rect = pg.Rect(width, get_random(enemy.get_size()[1], height - enemy.get_size()[1]), *enemy.get_size())
    e_speed = get_random(2, 5)
    return [enemy, e_rect, e_speed]
def create_bonus():
    bonus = pg.image.load("./imgs/bonus.png").convert_alpha()
    bonus_rect = pg.Rect(get_random(bonus.get_size()[0], width - bonus.get_size()[0]), -bonus.get_size()[1], *bonus.get_size())
    bonus_speed = get_random(5, 8)
    return [bonus, bonus_rect, bonus_speed]

enemies = []
bonuses = []
count = 0
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
        if i.type == CHANGE_IMG:
            count += 1
            if count == len(player_imgs):
                count = 0
            player = player_imgs[count]

    keys = pg.key.get_pressed()
    
    if (keys[K_DOWN] or keys[K_s]) and not p_rect.bottom >= height:
       p_rect = p_rect.move(0, p_speed)
    if (keys[K_UP] or keys[K_w]) and not p_rect.top <= 0:
        p_rect = p_rect.move(0, -p_speed)
    if (keys[K_RIGHT] or keys[K_d]) and not p_rect.right >= width:
        p_rect = p_rect.move(p_speed, 0)
    if (keys[K_LEFT] or keys[K_a]) and not p_rect.left <= 0:
        p_rect = p_rect.move(-p_speed, 0)

    # surface.blit(bg, (0, 0))
    bg_start -= bg_speed
    bg_finish -= bg_speed

    if bg_start < -bg.get_width():
        bg_start = bg.get_width()
    
    if bg_finish < -bg.get_width():
        bg_finish = bg.get_width()

    surface.blit(bg, (bg_start, 0))
    surface.blit(bg, (bg_finish, 0))


    surface.blit(player, p_rect)
    

    for enemy in enemies:
        enemy[1] = enemy[1].move(-enemy[2], 0)
        surface.blit(enemy[0], enemy[1])

        if enemy[1].left < -enemy[0].get_size()[0]:
            enemies.pop(enemies.index(enemy))

        if p_rect.colliderect(enemy[1]):
            enemies.pop(enemies.index(enemy))
            isWorking = False
    
    for bonus in bonuses:
        bonus[1] = bonus[1].move(0, bonus[2])
        surface.blit(bonus[0], bonus[1])
        
        if bonus[1].bottom > height + bonus[0].get_size()[1]:
            bonuses.pop(bonuses.index(bonus))

        if p_rect.colliderect(bonus[1]):
            bonuses.pop(bonuses.index(bonus))
            score += 1

    score_text = font.render('Score: ' + str(score), True, GREEN)
    text_rect = score_text.get_rect()
    text_rect.x = width - 150
    text_rect.y = 10
    if best_score < score:
        best_score = score
    
    best_text = font.render('Best score: ' + str(best_score), True, GREEN)
    best_rect = best_text.get_rect()
    best_rect.x = width - 150
    best_rect.y = 40

    surface.blit(best_text, best_rect)
    surface.blit(score_text, text_rect)
    pg.display.flip()