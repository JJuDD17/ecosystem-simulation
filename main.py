import pygame
import numpy as np
from settings import *
from environment import Environment
from camera import Camera


pygame.init()

map_image = pygame.Surface = pygame.image.load('images/map.bmp')
screen_size = DEFAULT_RESOLUTION
screen = pygame.display.set_mode(screen_size, flags=pygame.RESIZABLE)

environment = Environment(map_image)
environment.add_random_creature()

camera = Camera(environment)

clock = pygame.time.Clock()
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            screen = pygame.display.set_mode(event.size, flags=pygame.RESIZABLE)
        else:
            camera.process_event(event)

    screen.blit(map_image, (0, 0))
    environment.update()
    camera.draw(screen)
    pygame.display.flip()
    clock.tick(60)
