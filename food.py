from abc import ABC, abstractmethod


class Food(ABC):
    @abstractmethod
    def energy(self):
        pass


class Plant(Food):
    pass


class Animal(Food):
    pass


class Carrion(Food):
    pass
