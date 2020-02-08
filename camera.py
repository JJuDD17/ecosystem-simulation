import pygame
from pygame import gfxdraw
import numpy as np

from environment import Environment
from settings import *


class Camera:
    def __init__(self, environment: Environment):
        self.environment = environment
        self.original_map_image = environment.map_image
        self.map_size = np.array(self.original_map_image.get_size())
        self.resolution = np.array(pygame.display.get_surface().get_size())
        self.normal_scale = min(self.resolution // self.map_size)
        self.scale = self.normal_scale
        self.position = self.resolution / 2
        self.update_scaled_image()
        self.dragging = False

    def update_scaled_image(self):
        new_size = min(self.resolution * self.scale // self.normal_scale)
        self.scaled_image = pygame.transform.scale(self.original_map_image, (new_size, new_size))
        self.rect = self.scaled_image.get_rect()

    def set_resolution(self, value):
        self.resolution = value
        self.normal_scale = min(self.resolution // self.map_size)
        self.update_scaled_image()

    def set_scale(self, value):
        if value > 1:
            self.scale = value
        self.update_scaled_image()

    def draw(self, surface: pygame.SurfaceType):
        surface.fill(BACKGROUND_COLOR)
        image = self.scaled_image.copy()

        for plant in self.environment.plants:
            radius = self.scale // 2 - 1
            params = (image, *(plant.position * self.scale + radius), radius, plant.get_color())
            gfxdraw.aacircle(*params)
            gfxdraw.filled_circle(*params)

        for corpse in self.environment.corpses:
            radius = self.scale // 2 - 1
            params = (image, *(corpse.position * self.scale + radius), radius, corpse.get_color())
            gfxdraw.aacircle(*params)
            gfxdraw.filled_circle(*params)

        for creature in self.environment.creatures:
            radius = int(self.scale / 2 * creature.get_size())
            radius = radius if creature.get_size() < 1 else radius - 1
            params = (image, *(creature.position * self.scale + radius), radius, creature.get_color())
            gfxdraw.aacircle(*params)
            gfxdraw.filled_circle(*params)

        surface.blit(image, -np.array(self.rect.center) + self.position)

    def process_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.dragging = True
                self._offset = self.position - event.pos
            elif event.button == 4:
                new_scale = int((self.scale * 1.2))
                self.set_scale(new_scale if self.scale * 1.2 == new_scale else self.scale + 1)
                self.position -= (np.array(event.pos) - self.resolution / 2) / 4
            elif event.button == 5 and self.scale > 1:
                self.set_scale(int((self.scale / 1.2)))
                self.position = (self.position + self.resolution / 2) / 2
        elif event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:
                self.dragging = False
        elif event.type == pygame.MOUSEMOTION:
            if self.dragging:
                self.position = self._offset + event.pos
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.set_scale(min(self.resolution // self.map_size))
                self.position = self.resolution / 2
        elif event.type == pygame.VIDEORESIZE:
            self.set_resolution(np.array(event.size))
