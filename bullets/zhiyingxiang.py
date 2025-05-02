from bullet import Bullet
import json
from utils import resource_path
import pygame
from status import PLANT_AREA, GRID_SIZE
from bullets.luomobullet import LuoMoBullet as XiaoFeng

class ZhiYingXiang(Bullet):
    def __init__(self, pos, json_path, name, speed, harm, tick, item_name, attack_time):
        super().__init__(pos, json_path, name, speed, harm, tick, item_name, attack_time)
        self.is_attack = False

        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.attack_animation =  [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["attack_animation"]]
        
    def move(self, status):
        if self.speed == 0:
            return
        self.remove(status)
        self.pos[0] += self.speed
        self.rect.move_ip(self.speed, 0)
        self.index = [(self.rect.centerx - PLANT_AREA.left) // GRID_SIZE[0],
                      (self.rect.centery - PLANT_AREA.top) // GRID_SIZE[1]]
        if self.index[0] < 9:
            status.bullets[self.index[0]][self.index[1]][self.item_name] = True
        else:
            self.in_grid = False

    def attack(self, status, aim_zombie):
        status.items[4][aim_zombie].harm(status)

    def check_exist(self, status):
        return self.pos[1] <= PLANT_AREA.right

    def check_aim(self, status):
        if not self.in_grid:
            return None
        for zombie in status.zombies[self.index[0]][self.index[1]].keys():
            if self.rect.colliderect(status.items[4][zombie].rect):
                return zombie
        return None
    
    def update(self, event, status):
        if self.is_attack and self.animation_index >= len(self.attack_animation) - 1:
            for y in range(int(self.pos[1]) - 40, int(self.pos[1]) + 80, 40):
                pos = [self.pos[0], y]
                item_name = "xiaofeng" + str(status.global_ticks) + str(self.index) + str(y)
                status.items[5][item_name] = XiaoFeng(
                    pos=pos,
                    json_path=resource_path("./configs/statics/xiaofeng.json"),
                    name="xiaofeng",
                    speed=5,
                    harm=10,
                    tick=status.global_ticks,
                    item_name=item_name,
                    attack_time=50
                )
            return False
        if not self.check_exist(status):
            return False
        aim = self.check_aim(status)
        if aim is not None:
            self.is_attack = True
            self.attack(status, aim)
            return True
        self.move(status)
        return True