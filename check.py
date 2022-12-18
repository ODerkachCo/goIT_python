import pygame, random
from pygame.constants import QUIT, K_DOWN, K_UP, K_LEFT, K_RIGHT

pygame.init()
FPS = pygame.time.Clock()

screen = width, height = 1280, 720

BLACK = 0, 0, 0
WHITE = 255, 255, 255
GREEN = 0, 255, 255
RED = 136, 8, 8

colors = (BLACK, WHITE, GREEN, RED)

main_surface = pygame.display.set_mode(screen)
b = pygame.Surface((20, 20))
b.fill((0, 0, 0))
b_rect = b.get_rect()
b_speed = 1

enemy = pygame.Surface((20, 20))
enemy.fill(GREEN)
enemy_rect = pygame.Rect(width, 100, *enemy.get_size())
enemy_speed = 1


is_working = True

while is_working:
    FPS.tick(240)
    for event in pygame.event.get():
        if event.type == QUIT:
             is_working = False  
             
    press_keys = pygame.key.get_pressed()
    
    if press_keys[K_DOWN]:
        b_rect = b_rect.move(0, b_speed)
        
    if press_keys[K_UP]:
        b_rect = b_rect.move(0, -b_speed)
        
    if press_keys[K_LEFT]:
        b_rect = b_rect.move(-b_speed, 0)
    
    if press_keys[K_RIGHT]:
        b_rect = b_rect.move(b_speed, 0)
    
    
    main_surface.fill((205, 25, 145))
    main_surface.blit(b, b_rect)

    enemy_rect = enemy_rect.move(-enemy_speed, 0)
    main_surface.blit(enemy, enemy_rect)

    pygame.display.flip()