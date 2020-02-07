import pygame
import numpy as np
from random import choice, randint

from food import AbstractFood, AbstractAnimal
from settings import *
from prototype import Prototype


class Creature(pygame.sprite.Sprite, AbstractAnimal):
    def __init__(self, position, environment, prototype: Prototype, energy: float):
        super().__init__()

        self.position = np.array(position)
        self.environment = environment
        self.prototype = prototype
        self.energy_level = energy
        self.last_update = 0
        self.steps_since_reproduction = 0
        self.age = 0

        self._update_rect()

    def _move_by(self, x, y):
        new_position = self.position + (x, y)
        if tuple(new_position) in self.environment.available_tiles:
            self.position = new_position
            self._update_rect()

    def _move_randomly(self):
        '''Переместиться на рандомный прилегающий тайл'''
        self.position = choice([i for i in self.environment.available_tiles
                                if max(self.position - i) <= 1 and min(self.position - i) >= -1
                                and (self.position - i).any()])
        self._update_rect()

    def _update_rect(self):
        half_size = self.get_size() / 2
        self.rect = pygame.Rect([self.position[0] - half_size, self.position[1] - half_size, half_size, half_size])

    @staticmethod
    def _mutate_trait(value, rate, min_value, max_value):
        return value + randint(-rate if value >= min_value + rate else min_value - value,
                               rate if value <= max_value - rate else max_value - value)

    def _mutate(self) -> "Creature":
        return Creature(self.position, self.environment, self.prototype.mutate(), DEFAULT_ENERGY)

    def _reproduce(self):
        self.environment.add(self._mutate())

    def update(self, current_time=0, *args, **kwargs):
        if current_time < self.last_update + self.prototype.speed:
            return

        self.energy_level -= self.prototype.get_energy_consumption()

        if self.energy_level < 0:
            self.kill()

        if self.age > MAX_AGE:
            self.kill()

        self.last_update = current_time
        if self.age >= MATURE_AGE:
            if self.steps_since_reproduction >= self.prototype.reproduction_rate:
                self._reproduce()
                self.steps_since_reproduction = 0
            else:
                self.steps_since_reproduction += 1
        self._move_randomly()
        self.age += 1

    def get_energy(self):
        return self.energy_level

    def eat(self, food: AbstractFood):
        self.energy_level += food.get_energy()

    def get_size(self):
        if self.age <= MATURE_AGE:
            return self.age / MATURE_AGE
        else:
            return 1.0
