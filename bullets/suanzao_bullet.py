from bullet import Bullet
from status import PLANT_AREA, GRID_SIZE
import json
from utils import resource_path
import pygame
from math import sqrt

ACC = 0.1

class SuanZaoBullet(Bullet):
    def __init__(self, pos, json_path, name, speed, harm, tick, item_name, attack_time, aim):
        super().__init__(pos, json_path, name, speed, harm, tick, item_name, attack_time)
        if self.pos[1] < aim[1]:
            m = self.pos[1] - 150 if self.pos[1] - 150 <= PLANT_AREA.top else PLANT_AREA.top
        else:
            m = aim[1] - 150 if aim[1] - 150 <= PLANT_AREA.top else PLANT_AREA.top
        
        k = 2*(-m + self.pos[1] + sqrt(m**2 - m*self.pos[1] - m*aim[1] + self.pos[1]*aim[1]))/(self.pos[0] - aim[0])
        speed = sqrt(2 * ACC * (self.pos[1] - m))
        self.para_speed = speed / k
        self.speed = [-self.para_speed, -speed]
        self.aim = aim
        self.float_pos = [pos[0], pos[1]]
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
        self.speed[1] += ACC
        self.index = [(self.rect.centerx - PLANT_AREA.left) // GRID_SIZE[0],
                      (self.rect.centery - PLANT_AREA.top) // GRID_SIZE[1]]
        if self.index[0] < 9 and self.index[1] >= 0:
            status.bullets[self.index[0]][self.index[1]][self.item_name] = True
        else:
            self.in_grid = False

    def attack(self, status):
        status.planted_aoe_harm[self.index[0]][self.index[1]] += self.harm
        for i in range(self.index[0] - 1, self.index[0] + 2):
            for j in range(self.index[1] - 1, self.index[1] + 2):
                if i >= 0 and i < 9 and j >= 0 and j < 5:
                    status.planted_aoe_harm[i][j] += self.harm // 3
    
    def check_exist(self, status):
        if status.global_ticks - self.start_tick >= 90 and self.pos[1] >= self.aim[1]:
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



