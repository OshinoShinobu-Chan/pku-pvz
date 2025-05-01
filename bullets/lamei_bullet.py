from bullet import Bullet
from status import PLANT_AREA, GRID_SIZE
import json
from utils import resource_path, plant_grid_to_zombie_grid
import pygame

class LaMeiBullet(Bullet):
    def __init__(self, pos, json_path, name, speed, harm, tick, item_name, attack_time):
        super().__init__(pos, json_path, name, speed, harm, tick, item_name, attack_time)
        self.speed = speed
        self.float_pos = pos
        self.is_attack = False
        
        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.attack_animation =  [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["attack_animation"]]

    def move(self, status):
        self.remove(status)
        self.float_pos[0] += self.speed[0]
        self.float_pos[1] += self.speed[1]
        delta = [int(self.float_pos[0]) - self.pos[0], int(self.float_pos[1]) - self.pos[1]]
        self.pos = [int(self.float_pos[0]), int(self.float_pos[1])]
        self.rect.move_ip(delta[0], delta[1])
        self.index = [(self.rect.centerx - PLANT_AREA.left) // GRID_SIZE[0],
                      (self.rect.centery - PLANT_AREA.top) // GRID_SIZE[1]]
        if self.index[0] < 9 and self.index[0] >= 0 \
              and self.index[1] >= 0 and self.index[1] < 5:
            status.bullets[self.index[0]][self.index[1]][self.item_name] = True
        else:
            self.in_grid = False

    def attack(self, status):
        status.planted_single_harm[self.index[0]][self.index[1]] += self.harm

    def check_exist(self, status):
        if self.rect.colliderect(PLANT_AREA):
            return True
        self.remove(status)
        return False

    def check_attack(self, status):
        if not self.in_grid:
            return False
        zombie_index = plant_grid_to_zombie_grid(self.index)
        for zombie in status.zombies[zombie_index[0]][zombie_index[1]].keys():
            if self.rect.colliderect(status.items[4][zombie].rect):
                return True
        return False
        
    
    def update(self, event, status):
        if self.is_attack and self.animation_index >= len(self.attack_animation) - 1:
            return False
        if self.is_attack:
            return True
        if self.check_attack(status):
            self.is_attack = True
            self.animation = self.attack_animation
            self.animation_index = 0
            self.attack(status)
            return True
        self.move(status)
        return self.check_exist(status)

