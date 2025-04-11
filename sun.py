from button import Button
import pygame
from utils import resource_path

class Sun(Button):
    def __init__(self, pos, on_click, json_path, name, sun, move_delta = 0, on_focus=None, lose_fucus=None, check_enable=None):
        super().__init__(pos, on_click, json_path, name, on_focus, lose_fucus, check_enable)
        self.sun = sun
        self.move_delta = move_delta
    
    def move(self):
        if self.move_delta == 0:
            return
        self.pos[1] += self.move_delta
        self.rect.move_ip(0, self.move_delta)

    def update(self, event, status):
        self.move()
        if self.pos[1] > 730:
            return False
        if not self.rect.collidepoint(status.mouse_pos):
            return True
        for e in event:
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1 and status.mouse is None:
                status.sun += self.sun
                return False
        return True

class SunSpawner:
    def __init__(self, start_tick):
        self.start_tick = start_tick
    
    def excute(self, status, event):
        if (status.global_ticks - self.start_tick) % 600 == 0:
            status.items["moving_sun" + str(status.global_ticks)] = Sun(pos=[450, 160],
                                         on_click=None,
                                         json_path=resource_path("./configs/statics/sun.json"),
                                         name="moving_sun",
                                         sun=50,
                                         move_delta=1)
        return True