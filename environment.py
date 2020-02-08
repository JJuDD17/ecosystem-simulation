import pygame
from pygame.sprite import Group

from creature import Creature
from food import Corpse, Plant
from settings import *
import numpy as np
from random import choice, randint, random
from prototype import Prototype


class Environment(Group):
    def __init__(self, map_image: pygame.SurfaceType):
        super().__init__()

        self.map_image = map_image
        map_size = self.map_image.get_size()
        self.available_tiles = np.array([(x, y) for x in range(map_size[0]) for y in range(map_size[1])
                                         if self.map_image.get_at((x, y)) == GROUND_COLOR])
        self.creatures = pygame.sprite.Group()
        self.plants = pygame.sprite.Group()
        self.corpses = pygame.sprite.Group()

    def add(self, *sprites):
        super().add(*sprites)
        for i in sprites:
            if isinstance(i, Plant):
                self.plants.add(i)
            elif isinstance(i, Corpse):
                self.corpses.add(i)
            elif isinstance(i, Creature):
                self.creatures.add(i)

    def add_random_creature(self):
        position = choice(self.available_tiles)
        creature = Creature(position, self, Prototype.random_prototype(), DEFAULT_ENERGY)
        creature.environment = self
        self.add(creature)

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
                        self.corpses.add(Corpse(creature.position, creature.get_size()))
                    creature.kill()

        super().update(pygame.time.get_ticks(), *args)

    def try_grow_plant(self):
        if random() < PLANT_PROBABILITY:
            plant = Plant(choice(self.available_tiles), randint(MIN_PLANT_SIZE, MAX_PLANT_SIZE))
            self.add(plant)
            self.plants.add(plant)
