import pygame
from item import Item
from enum import Enum, auto
from status import PLANT_AREA
import json
from utils import plant_grid_to_zombie_grid

class Plant(Item):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name)
        self.is_planted = False
        self.life = life
        self.start_tick = tick
        self.sun = sun
        self.to_cold_time = to_cold_time
        self.item_name = item_name
    
    def on_mouse(self, status):
        delta = [status.mouse_pos[0] - self.rect.centerx, status.mouse_pos[1] - self.rect.centery]
        self.pos = status.mouse_pos
        self.rect.move_ip(delta)
    
    def plant(self, status):
        index = [(self.rect.centerx - PLANT_AREA.left) // self.rect.width,
                 (self.rect.centery - PLANT_AREA.top) // self.rect.height]
        if status.planted_plant[index[0]][index[1]] is not None:
            return True
        self.is_planted = True
        status.mouse = None
        self.pos = [PLANT_AREA.left + (index[0] * 2 + 1) * self.rect.width // 2,
                    PLANT_AREA.top + (index[1] * 2 + 1) * self.rect.height // 2]
        delta = [self.pos[0] - status.mouse_pos[0], self.pos[1] - status.mouse_pos[1]]
        self.rect.move_ip(delta)
        status.sun -= self.sun
        self.to_cold_time()
        status.planted_plant[index[0]][index[1]] = self.item_name
        self.index = [index[0], index[1]]
        return True

    def harm(self, harm_num=None):
        if harm_num is None:
            self.life = 0
        else:
            self.life -= harm_num
    
    def update(self, event, status):
        if self.is_planted:
            if self.life <= 0:
                status.planted_plant[self.index[0]][self.index[1]] = None
                return False
            return True
        self.on_mouse(status)
        # check click
        for e in event:
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if not PLANT_AREA.collidepoint(status.mouse_pos):
                    return False
                return self.plant(status)
        return True

    def attack(self, status):
        '''leave for child to implement'''
        pass
