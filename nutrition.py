import random
from abc import abstractmethod, ABC

import pygame

import food
import settings


class AbstractNutritionType(ABC):
    @abstractmethod
    def can_eat(self, f: food.AbstractFood) -> bool:
        pass

    @abstractmethod
    def get_nutrition_system_penalty(self):
        pass

    @abstractmethod
    def mutate(self) -> "AbstractNutritionType":
        pass

    @abstractmethod
    def get_color(self) -> pygame.Color:
        pass


class Herbivorous(AbstractNutritionType):
    def can_eat(self, f: food.AbstractFood) -> bool:
        return isinstance(food, food.AbstractPlant)

    def get_nutrition_system_penalty(self):
        return settings.HERBIVOROUS_PENALTY

    def mutate(self) -> AbstractNutritionType:
        if random.random() < settings.NUTRITION_MUTATE_PROBABILITY:
            return random.choice((Scavenger, Omnivorous, Predator))()
        return Herbivorous()

    def get_color(self) -> pygame.Color:
        return settings.HERBIVOROUS_COLOR


class Predator(AbstractNutritionType):
    def can_eat(self, f: food.AbstractFood) -> bool:
        return isinstance(food, food.AbstractAnimal)

    def get_nutrition_system_penalty(self):
        return settings.PREDATOR_PENALTY

    def mutate(self) -> AbstractNutritionType:
        if random.random() < settings.NUTRITION_MUTATE_PROBABILITY:
            return random.choice((Herbivorous, Omnivorous, Scavenger))()
        return Predator()

    def get_color(self) -> pygame.Color:
        return settings.PREDATOR_COLOR


class Omnivorous(AbstractNutritionType):
    def can_eat(self, f: food.AbstractFood) -> bool:
        return True

    def get_nutrition_system_penalty(self):
        return settings.OMNIVOROUS_PENALTY

    def mutate(self) -> AbstractNutritionType:
        if random.random() < settings.NUTRITION_MUTATE_PROBABILITY:
            return random.choice((Herbivorous, Scavenger, Predator))()
        return Omnivorous()

    def get_color(self) -> pygame.Color:
        return settings.OMNIVOROUS_COLOR


class Scavenger(AbstractNutritionType):
    def can_eat(self, f: food.AbstractFood) -> bool:
        return isinstance(food, food.AbstractCarrion)

    def get_nutrition_system_penalty(self):
        return settings.SCAVENGER_PENALTY

    def mutate(self) -> AbstractNutritionType:
        if random.random() < settings.NUTRITION_MUTATE_PROBABILITY:
            return random.choice((Herbivorous, Omnivorous, Predator))()
        return Scavenger()

    def get_color(self) -> pygame.Color:
        return settings.SCAVENGER_COLOR
