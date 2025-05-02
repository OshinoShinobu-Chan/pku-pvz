from plant import Plant
import pygame
from status import PLANT_AREA

class Aim(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)

    def not_planted(self, event, status):
        self.on_mouse(status)
        for e in event:
            if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                print("mouse_pos: " + str(status.mouse_pos))
                if PLANT_AREA.collidepoint(status.mouse_pos):
                    status.suanzao_aim = [status.mouse_pos[0], status.mouse_pos[1]]
                    print("aim: " + str(status.suanzao_aim))
                return False
        return True
    
    def update(self, event, status):
        if status.global_ticks - self.start_tick <= 3:
            return True
        return self.not_planted(event, status)