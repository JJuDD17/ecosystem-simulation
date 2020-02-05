import pygame
from pygame.sprite import Group

from corpse import Corpse
from creature import Creature
from plant import Plant
from settings import *
import numpy as np
from random import choice, randint, random
from prototype import Prototype


class Environment(Group):
    def __init__(self, map_image: pygame.SurfaceType):
        super().__init__()

        self._offset_x = self._offset_y = 0

        self.map_image = map_image
        self.size = np.array(self.map_image.get_size())
        self.border_size = self.map_image.get_size()
        self.available_tiles = np.array([(x, y) for x in range(self.size[0]) for y in range(self.size[1])
                                         if self.map_image.get_at((x, y)) == pygame.color.THECOLORS["green"]])
        self.dragging = False
        self.scale = TILE_SIZE
        self.image: pygame.SurfaceType = pygame.transform.scale(self.map_image, self.size * self.scale)
        self.rect: pygame.Rect = self.image.get_rect()

        self.creatures = pygame.sprite.Group()
        self.plants = pygame.sprite.Group()
        self.corpses = pygame.sprite.Group()

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

    def add_creature(self, creature: Creature = None):
        if creature is None:
            position = choice(self.available_tiles)
            creature = Creature(position, self, Prototype.random_prototype(), DEFAULT_ENERGY)
        creature.environment = self
        self.creatures.add(creature)
        return self.add(creature)

    def draw(self, surface: pygame.SurfaceType):
        surface.fill(pygame.color.THECOLORS["dimgrey"])
        surface.blit(self.image, self.rect.topleft)

        for plant in self.plants:
            pygame.draw.circle(surface, pygame.color.THECOLORS["lawngreen"],
                               plant.position * self.scale + self.scale // 2 + self.rect.topleft,
                               self.scale // 2)
        for corpse in self.corpses:
            pygame.draw.circle(surface, pygame.color.THECOLORS["black"],
                               corpse.position * self.scale + self.scale // 2 + self.rect.topleft,
                               self.scale // 2)

        for creature in self.creatures:
            radius = int(creature.size() * self.scale / 2)
            pygame.draw.circle(surface, creature.prototype.nutrition_type.color(),
                               creature.position * self.scale + self.scale // 2 + self.rect.topleft,
                               radius if radius >= 2 else 2)

    def update(self, *args):
        self.try_grow_plant()

        for plant, creatures in pygame.sprite.groupcollide(self.plants, self.creatures, False, False).items():
            for creature in creatures:
                creature.eat(plant)
                plant.kill()

        for eater, creatures in pygame.sprite.groupcollide(self.creatures, self.creatures, False, False).items():
            for creature in creatures:
                if eater.prototype.nutrition_type.can_eat(creature):
                    eater.eat(creature)
                    if not isinstance(creature, Corpse):
                        self.corpses.add(Corpse(creature.position, creature.size()))
                    creature.kill()

        super().update(pygame.time.get_ticks(), *args)

    def try_grow_plant(self):
        if random() < PLANT_PROBABILITY:
            plant = Plant(choice(self.available_tiles), randint(MIN_PLANT_SIZE, MAX_PLANT_SIZE))
            self.add(plant)
            self.plants.add(plant)
