import pygame
from item import Item

class Merge(Item):
    def __init__(self, pos, json_path, name, start_tick, duration_ms, static_time = 0):
        super().__init__(pos, json_path, name)
        self.start_tick = start_tick
        self.duration_tick = duration_ms * 60 // 1000
        self.delta = 255 / self.duration_tick
        self.static_time = static_time
        self.alpha = 0
        self.image.set_alpha(0)
    
    def update(self, event, status):
        if status.global_ticks - self.start_tick < self.duration_tick:
            self.alpha += self.delta
            self.image.set_alpha(int(self.alpha))
        if status.global_ticks >= self.start_tick + self.duration_tick + self.static_time:
            return False
        return True