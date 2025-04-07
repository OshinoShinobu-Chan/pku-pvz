import pygame
from item import Item
from enum import Enum, auto

class Plant(Item):
    def __init__(self, pos, json_path, name, tick, life):
        super().__init__(pos, json_path, name)
        self.is_planted = False
        self.life = life
        self.start_tick = tick
    
    def on_mouse(self, status):
        self.pos = status.mouse_pos
        self.rect.move_ip(self.pos)
    
    def plant(self, status):
        self.is_planted = True
        status.mouse = None
    
    def update(self, event, status):
        if self.life == 0:
            return False
        if self.is_planted:
            return True
        self.on_mouse(status)
        # check click
        for e in event:
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.plant(status)
                break
        return True


