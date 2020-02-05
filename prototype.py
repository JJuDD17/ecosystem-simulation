from random import randint

import nutrition
from settings import *


class Prototype:
    def __init__(self, strength: float, mass: float, speed: float, nutrition_type: nutrition.NutritionType,
                 reproduction_rate: int):
        self.strength = strength
        self.mass = mass
        self.speed = speed
        self.nutrition_type = nutrition_type
        self.reproduction_rate = reproduction_rate

    @staticmethod
    def _mutate_trait(value, rate, min_value, max_value):
        return value + randint(-rate if value >= min_value + rate else min_value - value,
                               rate if value <= max_value - rate else max_value - value)

    def mutate(self) -> "Prototype":
        speed = self._mutate_trait(self.speed, 5, MIN_SPEED, MAX_SPEED)
        mass = self._mutate_trait(self.mass, 5, MIN_MASS, MAX_MASS)
        strength = self._mutate_trait(self.mass, 5, MIN_STRENGTH, MAX_STRENGTH)
        reproduction_rate = self._mutate_trait(self.reproduction_rate, 2, MIN_REPRODUCTION_RATE,
                                               MAX_REPRODUCTION_RATE)

        nutrition_type = self.nutrition_type.mutate()
        return Prototype(strength, mass, speed, nutrition_type, reproduction_rate)

    def energy_consumption(self) -> float:
        consumption = 0
        consumption += self.strength * STRENGTH_PENALTY
        consumption += self.speed * SPEED_PENALTY
        consumption += self.mass * MASS_PENALTY
        return consumption

    @staticmethod
    def random_prototype() -> "Prototype":
        return Prototype(randint(MIN_STRENGTH, MAX_STRENGTH),
                         randint(MIN_MASS, MAX_MASS),
                         randint(MIN_SPEED, MAX_SPEED),
                         nutrition.Herb(),
                         randint(MIN_REPRODUCTION_RATE, MAX_REPRODUCTION_RATE))
