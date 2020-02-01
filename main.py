import pygame
import numpy as np
from settings import *
from environment import Environment


pygame.init()

map_image: pygame.Surface = pygame.image.load('images/map.bmp')
screen_size = np.array(map_image.get_size()) * TILE_SIZE
screen = pygame.display.set_mode(screen_size)

environment = Environment(map_image)
environment.add_creature((120, 70, 210))

clock = pygame.time.Clock()
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.blit(map_image, (0, 0))
    environment.update()
    environment.draw(screen)
    pygame.display.flip()
    clock.tick(60)
