from plant import Plant
from utils import plant_grid_to_zombie_grid, resource_path
import json
import pygame

class DiHuang(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.attack_animation = [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["attack_animation"]]
        self.is_attack_animation = False
        
    def attack(self, status):
        status.planted_aoe_harm[self.index[0]][self.index[1]] += 1800
        if self.index[0] + 1 < 9:
            status.planted_aoe_harm[self.index[0] + 1][self.index[1]] += 1800

    def update(self, event, status):
        if self.is_attack_animation:
            if self.animation_index >= len(self.animation) - 1:
                super().remove(status)
                return False
            return True
        if self.is_planted:
            zombie_grid = plant_grid_to_zombie_grid(self.index)
            if len(status.zombies[zombie_grid[0]][zombie_grid[1]]) > 0:
                self.attack(status)
                self.is_attack_animation = True
                self.animation = self.attack_animation
            return super().check_life(event, status)
        return super().not_planted(event, status)