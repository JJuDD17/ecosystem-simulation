import numpy
import pygame

from food import Food
from settings import PLANT_ENERGY


class Plant(Food, pygame.sprite.Sprite):
    def __init__(self, position: numpy.array, size: float):
        super().__init__()

        self.position = numpy.array(position)
        self.size = size
        half_size = self.size / 2
        self.rect = pygame.Rect([self.position[0] - half_size, self.position[1] - half_size, half_size, half_size])

    def energy(self):
        return self.size * PLANT_ENERGY
