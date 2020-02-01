import pygame
import numpy as np
from random import choice, randint
from settings import *


class Creature(pygame.sprite.Sprite):
    def __init__(self, position, color, speed_ms, reproduction_rate_steps, environment):
        super().__init__()

        self.position = np.array(position)
        self.color = color
        self.speed = speed_ms
        self.reproduction_rate = reproduction_rate_steps
        self.environment = environment
        self.last_update = 0
        self.steps_since_reproduction = 0
        self.age = 0

    def _move_by(self, x, y):
        new_position = self.position + (x, y)
        if tuple(new_position) in self.environment.available_tiles:
            self.position = new_position

    def _move_randomly(self):
        '''Переместиться на рандомный прилегающий тайл'''
        self.position = choice([i for i in self.environment.available_tiles
                                if max(self.position - i) <= 1 and min(self.position - i) >= -1
                                and (self.position - i).any()])

    @staticmethod
    def _mutate_trait(value, rate, min_value, max_value):
        return value + randint(-rate if value >= min_value + rate else min_value - value,
                               rate if value <= max_value - rate else max_value - value)

    def _mutate(self):
        new_color = [self._mutate_trait(self.color[i], 30, 0, 255) for i in range(3)]
        new_speed = self._mutate_trait(self.speed, 5, MIN_SPEED, MAX_SPEED)
        new_reproduction_rate = self._mutate_trait(self.reproduction_rate, 2, MIN_REPRODUCTION_RATE, MAX_REPRODUCTION_RATE)
        new_creature = Creature(self.position, new_color, new_speed, new_reproduction_rate, self.environment)
        return new_creature

    def _reproduce(self):
        self.environment.add_creature(self._mutate())

    def update(self, current_time=0, *args, **kwargs):
        if current_time < self.last_update + self.speed:
            return
        if self.age > MAX_AGE:
            self.kill()
        self.last_update = current_time
        if self.age >= MATURE_AGE:
            if self.steps_since_reproduction >= self.reproduction_rate:
                self._reproduce()
                self.steps_since_reproduction = 0
            else:
                self.steps_since_reproduction += 1
        self._move_randomly()
        self.age += 1
