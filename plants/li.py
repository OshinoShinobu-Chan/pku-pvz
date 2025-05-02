from plant import Plant
from bullets.libullet import LiBullet
from utils import resource_path
from random import seed, randint
import pygame
import json

class Li(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.last_attack_time = tick
        self.attack_interval = 180
        self.is_attack = False
        self._aim = None
        seed()

        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.attack_animation = [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["attack_animation"]]

    def aim(self, status):
        for i in range(self.index[1] + 1, 10):
            if len(status.zombies[i][self.index[1]]) == 0:
                continue
            for zombie in status.zombies[i][self.index[1]].keys():
                if zombie in status.items[4]:
                    return [status.items[4][zombie].rect.center, status.items[4][zombie].interval]
        return None

    def attack(self, status):
        aim = self._aim
        if aim is None:
            return
        aim = [aim[0][0] - 120 // aim[1], aim[0][1]]
        speed = (aim[0] - self.pos[0]) / 120
        item_name = "li_bullet" + str(status.global_ticks) + str(self.index)
        harm = 100 if randint(0, 9) != 0 else 114514
        status.items[5][item_name] = LiBullet(
            pos=[self.pos[0], self.pos[1]],
            json_path=resource_path("./configs/statics/li_bullet.json"),
            name="li_bullet",
            speed=speed,
            harm=harm,
            tick=status.global_ticks,
            item_name=item_name,
            attack_time=114514,
            index=self.index
        )
    
    def update(self, event, status):
        if not self.is_planted:
            return super().not_planted(event, status)
        if self.attack_interval == 180 and status.winter_zombie_cnt > 0:
            self.attack_interval = 225
        elif self.attack_interval == 225 and status.winter_zombie_cnt <= 0:
            self.attack_interval = 180
        if self.is_attack and self.animation_index < len(self.attack_animation) - 1:
            return super().check_life(event, status)
        elif self.is_attack:
            self.animation = []
            self.animation_index = 0
            self.attack(status)
            self.is_attack = False
            return super().check_life(event, status)
        if status.global_ticks - self.last_attack_time >= self.attack_interval:
            self._aim = self.aim(status)
            if self._aim is None:
                return super().check_life(event, status)
            self.animation = self.attack_animation
            self.is_attack = True
            self.last_attack_time = status.global_ticks
        return super().check_life(event, status)
            

        

