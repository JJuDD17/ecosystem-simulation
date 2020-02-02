import pygame
from pygame.sprite import Group
from creature import Creature
from settings import *
import numpy as np
from random import choice, randint


class Environment(Group):
    def __init__(self, map_image: pygame.SurfaceType):
        super().__init__()

        self.map_image = map_image
        self.size = np.array(self.map_image.get_size())
        self.border_size = self.map_image.get_size()
        self.available_tiles = np.array([(x, y) for x in range(self.size[0]) for y in range(self.size[1])
                                         if self.map_image.get_at((x, y)) == (0, 255, 0)])
        self.dragging = False
        self.scale = TILE_SIZE
        self.image: pygame.SurfaceType = pygame.transform.scale(self.map_image, self.size * self.scale)
        self.rect: pygame.Rect = self.image.get_rect()

    def _rescale(self, factor):
        self.image = pygame.transform.scale(self.map_image, self.size * self.scale)
        self.rect.x -= self.scale * factor
        self.rect.y -= self.scale * factor

    def process_event(self, event: pygame.event.EventType):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                mouse_x, mouse_y = event.pos
                self._offset_x = self.rect.x - mouse_x
                self._offset_y = self.rect.y - mouse_y
            elif event.button == 4:
                self.scale += 1
                self._rescale(1)
            elif event.button == 5 and self.scale > 1:
                self.scale -= 1
                self._rescale(-1)
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                mouse_x, mouse_y = event.pos
                self.rect.x = mouse_x + self._offset_x
                self.rect.y = mouse_y + self._offset_y
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.scale = TILE_SIZE
                x, y = pygame.display.get_surface().get_size()
                self.rect.center = x / 2, y / 2
                self._rescale(0)

    def add_creature(self, color=None, speed_ms=None, reproduction_rate_steps=None, position=None):
        if isinstance(color, Creature):
            color.environment = self
            return self.add(color)
        if not color:
            color = (randint(0, 255) for i in range(3))
        if not speed_ms:
            speed_ms = randint(MIN_SPEED, MAX_SPEED)
        if not reproduction_rate_steps:
            reproduction_rate_steps = randint(MIN_REPRODUCTION_RATE, MAX_REPRODUCTION_RATE)
        if not position:
            position = choice(self.available_tiles)
        return self.add(Creature(position, color, speed_ms, reproduction_rate_steps, self))

    def draw(self, surface: pygame.SurfaceType):
        surface.fill((127, 127, 127))
        surface.blit(self.image, self.rect.topleft)
        for creature in self.spritedict:
            if creature.age >= MATURE_AGE:
                pygame.draw.circle(surface, creature.color, creature.position * self.scale + self.scale // 2 + self.rect.topleft,
                                   self.scale // 2)
            else:
                radius = int(creature.age / MATURE_AGE * self.scale / 2)
                pygame.draw.circle(surface, creature.color, creature.position * self.scale + self.scale // 2 + self.rect.topleft,
                                   radius if radius >= 2 else 2)

    def update(self, *args):
        super().update(pygame.time.get_ticks(), *args)
