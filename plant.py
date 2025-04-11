import pygame
from item import Item
from enum import Enum, auto
from status import PLANT_AREA
import json

class Plant(Item):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time):
        super().__init__(pos, json_path, name)
        self.is_planted = False
        self.life = life
        self.start_tick = tick
        self.sun = sun
        self.to_cold_time = to_cold_time
    
    def on_mouse(self, status):
        delta = [status.mouse_pos[0] - self.rect.centerx, status.mouse_pos[1] - self.rect.centery]
        self.pos = status.mouse_pos
        self.rect.move_ip(delta)
    
    def plant(self, status):
        self.is_planted = True
        status.mouse = None
        index = [(self.rect.centerx - PLANT_AREA.left) // self.rect.width,
                 (self.rect.centery - PLANT_AREA.top) // self.rect.height]
        self.pos = [PLANT_AREA.left + (index[0] * 2 + 1) * self.rect.width // 2,
                    PLANT_AREA.top + (index[1] * 2 + 1) * self.rect.height // 2]
        delta = [self.pos[0] - status.mouse_pos[0], self.pos[1] - status.mouse_pos[1]]
        self.rect.move_ip(delta)
        status.sun -= self.sun
        self.to_cold_time()
    
    def update(self, event, status):
        if self.life == 0:
            return False
        if self.is_planted:
            return True
        self.on_mouse(status)
        # check click
        for e in event:
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                if not PLANT_AREA.collidepoint(status.mouse_pos):
                    return False
                self.plant(status)
                break
        return True


