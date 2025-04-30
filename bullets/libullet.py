from bullet import Bullet
from status import PLANT_AREA, GRID_SIZE
import json
from utils import resource_path
import pygame

class LiBullet(Bullet):
    def __init__(self, pos, json_path, name, speed, harm, tick, item_name, attack_time, index):
        super().__init__(pos, json_path, name, speed, harm, tick, item_name, attack_time)
        self.speed = [speed, -120]
        self.start_pos = pos
        self.float_pos = pos
        self.is_attack = False
        self.start_index = index
        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.attack_animation =  [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["attack_animation"]]

    def move(self, status):
        self.remove(status)
        self.float_pos[0] += self.speed[0]
        self.float_pos[1] += self.speed[1] / 20
        delta = [int(self.float_pos[0]) - self.pos[0], int(self.float_pos[1]) - self.pos[1]]
        self.pos = [int(self.float_pos[0]), int(self.float_pos[1])]
        self.rect.move_ip(delta[0], delta[1])
        self.speed[1] += 2
        self.index = [(self.rect.centerx - PLANT_AREA.left) // GRID_SIZE[0],
                      (self.rect.centery - PLANT_AREA.top) // GRID_SIZE[1]]
        if self.index[0] < 9 and self.index[1] >= 0:
            status.bullets[self.index[0]][self.index[1]][self.item_name] = True
        else:
            self.in_grid = False
    
    def attack(self, status):
        status.planted_single_harm[self.index[0]][self.index[1]] += self.harm
        status.planted_aoe_harm[self.index[0]][self.index[1]] += 50

    def check_exist(self, status):
        if status.global_ticks - self.start_tick >= 100 and self.index[1] >= self.start_index[1]:
            self.attack(status)
            self.remove(status)
            return False
        return True
    
    def update(self, event, status):
        if self.is_attack and self.animation_index >= len(self.attack_animation) - 1:
            return False
        if not self.check_exist(status):
            self.is_attack = True
            self.animation = self.attack_animation
            return True
        self.move(status)
        return True