from item import Item
from zombie import Zombie
from status import PLANT_AREA, ZOMBIE_AREA, GRID_SIZE
from plant import QIAO_MU
from utils import resource_path, zombie_grid_to_plant_grid
import pygame

class Rope(Item):
    def __init__(self, pos, json_path, name):
        super().__init__(pos, json_path, name)
    
    def move(self, deltay):
        self.pos[1] += deltay
        self.rect.move_ip(0, deltay)

    def update(self, event, status):
        return True

class static_plant(Item):
    def __init__(self, pos, json_path, name):
        super().__init__(pos, json_path, name)
        
    def move(self, deltay):
        self.pos[1] += deltay
        self.rect.move_ip(0, deltay)

    def update(self, event, status):
        return True

G = 0.2
class WaCaiJiangShi(Zombie):
    def __init__(self, pos, json_path, name, tick, life, item_name, aim):
        super().__init__(pos, json_path, name, tick, life, item_name)
        self.speed = 1
        self.float_pos = [self.pos[0], self.pos[1]]
        self.aimy = PLANT_AREA.top + (aim[1] * 2 + 1) * GRID_SIZE[1] / 2
        print(aim)
        self.aim_top = PLANT_AREA.top + aim[1] * GRID_SIZE[1]
        print(self.aim_top)
        self.k = 2 * G / (self.aimy - 60)
        self.is_attack = False
        self.rope_name = "rope_" + str(pos)
        self.has_rope = False
        self.bottom_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                                (self.rect.bottom - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.aim_plant_name = "aim_plant_" + str(pos)
        self.has_aim_plant = False

    def move(self, status):
        acc = G - self.k * self.pos[1]
        self.speed += acc
        self.remove(status)
        self.pos[1] += self.speed
        self.rect.move_ip(0, self.speed)
        self.left_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                           (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.right_index = [(self.rect.right - ZOMBIE_AREA.left) // GRID_SIZE[0],
                            (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        status.items[5][self.rope_name].move(self.speed)
        
    def add_zombie(self, status):
        status.zombies[self.left_index[0]][self.left_index[1]][self.item_name] = True
        status.zombies[self.right_index[0]][self.right_index[1]][self.item_name] = True

    def remove(self, status):
        if self.bottom_index[1] < 5 and\
              self.item_name in status.zombies[self.bottom_index[0]][self.bottom_index[1]]:
            del status.zombies[self.bottom_index[0]][self.bottom_index[1]][self.item_name]

    def update(self, event, status):
        if not self.is_attack and self.life <= 0:
            self.remove(status)
            del status.items[5][self.rope_name]
            return False
        
        if self.rect.bottom > self.aim_top and not self.is_attack:
            self.is_attack = True
            self.bottom_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                                (self.rect.bottom - ZOMBIE_AREA.top) // GRID_SIZE[1]]
            plant_index = zombie_grid_to_plant_grid(self.bottom_index)
            print(f"real aim: {self.bottom_index}, bottom: {self.rect.bottom}")

            if self.bottom_index[1] < 5:
                status.zombies[self.bottom_index[0]][self.bottom_index[1]][self.item_name] = True
            
            aim_plant = status.planted_plant[plant_index[0]][plant_index[1]]
            if aim_plant is None or\
                "dihuang" in aim_plant or\
                    any(s in aim_plant for s in QIAO_MU):
                return True

            pos = status.items[3][aim_plant].rect.center
            json_path = status.items[3][aim_plant].json_path
            status.items[3][aim_plant].harm()
            status.items[5][self.aim_plant_name] = static_plant(
                pos=pos,
                json_path=json_path,
                name="static_plant"
            )
            self.has_aim_plant = True

            self.move(status)
            return True

        if self.rect.bottom < self.aim_top and self.is_attack:
            self.remove(status)

        if self.rect.bottom <= 5 and self.is_attack:
            self.remove(status)
            if self.has_aim_plant:
                del status.items[5][self.aim_plant_name]
            del status.items[5][self.rope_name]
            return False

        if self.is_attack and self.speed <= 0 and self.has_aim_plant:
            status.items[5][self.aim_plant_name].move(self.speed)

        if self.rect.top <= 0 and not self.has_rope:
            self.has_rope = True
            status.items[5][self.rope_name] = Rope(
                pos=[self.rect.centerx, -470],
                json_path=resource_path("./configs/statics/rope.json"),
                name="rope"
            )
        
        self.move(status)
        return True
