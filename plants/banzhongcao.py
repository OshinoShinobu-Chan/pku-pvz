from plant import Plant
from status import PLANT_AREA, GRID_SIZE
from random import seed, randint
from plants.ant import Ant
from utils import resource_path
import json
import pygame

class BanZhongCao(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.blossom_animation =  [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["blossom_animation"]]
        self.is_blossom = False
        seed()

    def attack(self, status):
        for i in range(self.index[0] - 1, self.index[0] + 2):
            for j in range(self.index[1] - 1, self.index[1] + 2):
                if i < 9 and i >= 0 and j < 5 and j >= 0:
                    center = [PLANT_AREA.left + (i * 2 + 1) * GRID_SIZE[0] // 2,
                              PLANT_AREA.top + (j * 2 + 1) * GRID_SIZE[1] // 2]
                    random = [randint(-GRID_SIZE[0] // 3, GRID_SIZE[0] // 3),
                              randint(-GRID_SIZE[1] // 3, GRID_SIZE[1] // 3)]
                    pos = [center[0] + random[0], center[1] + random[1]]
                    item_name = "ant" + str(status.global_ticks) + str(center)
                    status.items[5][item_name] = Ant(
                        pos=pos,
                        json_path=resource_path("./configs/statics/ant.json"),
                        name=item_name,
                        tick=status.global_ticks
                    )
    
    def update(self, event, status):
        if self.is_planted and status.global_ticks - self.start_tick < 300:
            return super().check_life(event, status)
        elif self.is_planted and not self.is_blossom:
            self.is_blossom = True
            self.animation = self.blossom_animation
            return True
        elif self.is_planted and self.animation_index >= len(self.blossom_animation) - 1:
            self.attack(status)
            self.remove(status)
            return False
        elif self.is_planted:
            return True
        return super().not_planted(event, status)
