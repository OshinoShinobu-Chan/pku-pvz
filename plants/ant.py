from item import Item
from utils import resource_path
from status import PLANT_AREA, GRID_SIZE
import json
import pygame

class Ant(Item):
    def __init__(self, pos, json_path, name, tick):
        super().__init__(pos, json_path, name)
        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.walk_animation =  [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["animation"]]
        self.is_walking = False
        self.start_tick = tick
        self.speed = 3

    def attack(self, status):
        index = [(self.rect.centerx - PLANT_AREA.left) // GRID_SIZE[0],
                 (self.rect.centery - PLANT_AREA.top) // GRID_SIZE[1]]
        if index[0] < 9:
            status.planted_aoe_harm[index[0]][index[1]] += 1800

    def move(self):
        self.pos[0] += self.speed
        self.rect.move_ip(self.speed, 0)

    def update(self, event, status):
        if status.global_ticks - self.start_tick < 60:
            return True
        if not self.is_walking:
            self.is_walking = True
            self.animation = self.walk_animation
        if self.is_walking:
            if self.pos[0] > 1280:
                return False
            self.move()
            self.attack(status)
        return True