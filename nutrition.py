import random
from abc import abstractmethod, ABC

import pygame

import food
import settings


class NutritionType(ABC):
    @abstractmethod
    def can_eat(self, f: food.Food) -> bool:
        pass

    @abstractmethod
    def nutrition_system_penalty(self):
        pass

    @abstractmethod
    def mutate(self) -> "NutritionType":
        pass

    @abstractmethod
    def color(self) -> pygame.Color:
        pass


class Herb(NutritionType):
    def can_eat(self, f: food.Food) -> bool:
        return isinstance(food, food.Plant)

    def nutrition_system_penalty(self):
        return settings.HERB_PENALTY

    def mutate(self) -> NutritionType:
        r = random.random()
        if r < settings.NUTRITION_MUTATE_PROBABILITY:
            return Predator()
        if r < 2 * settings.NUTRITION_MUTATE_PROBABILITY:
            return Omnivorous()
        return Herb()

    def color(self) -> pygame.Color:
        return pygame.color.THECOLORS["darkgreen"]


class Predator(NutritionType):
    def can_eat(self, f: food.Food) -> bool:
        return isinstance(food, food.Animal)

    def nutrition_system_penalty(self):
        return settings.PREDATOR_PENALTY

    def mutate(self) -> NutritionType:
        r = random.random()
        if r < settings.NUTRITION_MUTATE_PROBABILITY:
            return Herb()
        if r < 2 * settings.NUTRITION_MUTATE_PROBABILITY:
            return Omnivorous()
        if r < 3 * settings.NUTRITION_MUTATE_PROBABILITY:
            return Scavenger()
        return Predator()

    def color(self) -> pygame.Color:
        return pygame.color.THECOLORS["red"]


class Omnivorous(NutritionType):
    def can_eat(self, f: food.Food) -> bool:
        return True

    def nutrition_system_penalty(self):
        return settings.OMNI_PENALTY

    def mutate(self) -> NutritionType:
        r = random.random()
        if r < settings.NUTRITION_MUTATE_PROBABILITY:
            return Herb()
        if r < 2 * settings.NUTRITION_MUTATE_PROBABILITY:
            return Scavenger()
        if r < 3 * settings.NUTRITION_MUTATE_PROBABILITY:
            return Predator()
        return Omnivorous()

    def color(self) -> pygame.Color:
        return pygame.color.THECOLORS["grey"]


class Scavenger(NutritionType):
    def can_eat(self, f: food.Food) -> bool:
        return isinstance(food, food.Carrion)

    def nutrition_system_penalty(self):
        return settings.SCAV_PENALTY

    def mutate(self) -> NutritionType:
        r = random.random()
        if r < settings.NUTRITION_MUTATE_PROBABILITY:
            return Herb()
        if r < 2 * settings.NUTRITION_MUTATE_PROBABILITY:
            return Omnivorous()
        if r < 3 * settings.NUTRITION_MUTATE_PROBABILITY:
            return Predator()
        return Scavenger()

    def color(self) -> pygame.Color:
        return pygame.color.THECOLORS["brown"]

