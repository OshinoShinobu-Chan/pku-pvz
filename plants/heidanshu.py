from plant import Plant
from utils import resource_path
import pygame
import json
from bullets.zhiyingxiang import ZhiYingXiang

class HeiDanShu(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.is_dead = False

        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.dead_animation = [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["dead_animation"]]
        
    def update(self, event, status):
        if not self.is_planted:
            return super().not_planted(event, status)
        if self.is_dead and self.animation_index >= len(self.dead_animation) - 1:
            self.remove(status)
            pos = [self.pos[0] - 100, self.pos[1]]
            item_name = "zhiyingxiang" + str(status.global_ticks) + str(self.index)
            status.items[5][item_name] = ZhiYingXiang(
                pos=pos,
                json_path=resource_path("./configs/statics/zhiyingxiang.json"),
                name="zhiyingxiang",
                speed=2,
                harm=114514,
                tick=status.global_ticks,
                item_name=item_name,
                attack_time=114514
            )
            return False
        if self.life <= 0:
            self.is_dead = True
            self.animation = self.dead_animation
            self.animation_index = 0
        return True