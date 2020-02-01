import pygame
from creature import Creature
from settings import *
import numpy as np
from random import choice, randint


class Environment(pygame.sprite.Group):
    def __init__(self, map_image: pygame.SurfaceType):
        super().__init__()

        self.map_image = map_image
        self.size = self.map_image.get_size()
        self.border_size = self.map_image.get_size()
        self.available_tiles = np.array([(x, y) for x in range(self.size[0]) for y in range(self.size[1])
                                         if self.map_image.get_at((x, y)) == (0, 255, 0)])
        self._scaled_map_image = None

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
        if not self._scaled_map_image:
            self._scaled_map_image = pygame.transform.scale(self.map_image, surface.get_size())
        surface.blit(self._scaled_map_image, (0, 0))
        for creature in self.spritedict:
            if creature.age >= MATURE_AGE:
                pygame.draw.circle(surface, creature.color, creature.position * TILE_SIZE + TILE_SIZE // 2,
                                   TILE_SIZE // 2)
            else:
                radius = int(creature.age / MATURE_AGE * TILE_SIZE / 2)
                pygame.draw.circle(surface, creature.color, creature.position * TILE_SIZE + TILE_SIZE // 2,
                                   radius if radius >= 2 else 2)

    def update(self, *args):
        super().update(pygame.time.get_ticks(), *args)
