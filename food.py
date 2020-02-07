import pygame
import numpy
from settings import CORPSE_ENERGY, PLANT_ENERGY

from abc import ABC, abstractmethod


class AbstractFood(ABC):
    @abstractmethod
    def get_energy(self):
        pass


class AbstractPlant(AbstractFood):
    pass


class AbstractAnimal(AbstractFood):
    pass


class AbstractCarrion(AbstractFood):
    pass


class Plant(AbstractPlant, pygame.sprite.Sprite):
    def __init__(self, position: numpy.array, size: float):
        super().__init__()

        self.position = numpy.array(position)
        self.size = size
        half_size = self.size / 2
        self.rect = pygame.Rect([self.position[0] - half_size, self.position[1] - half_size, half_size, half_size])
        self.energy = PLANT_ENERGY

    def get_energy(self):
        return self.size * self.energy


class Corpse(AbstractCarrion, pygame.sprite.Sprite):
    def __init__(self, position: numpy.array, size: float):
        super().__init__()

        self.position = numpy.array(position)
        self.size = size
        half_size = self.size / 2
        self.rect = pygame.Rect([self.position[0] - half_size, self.position[1] - half_size, half_size, half_size])
        self.energy = CORPSE_ENERGY

    def get_energy(self):
        return self.size * self.energy
