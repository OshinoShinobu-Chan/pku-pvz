from plant import Plant
from bullets.lamei_bullet import LaMeiBullet
from utils import resource_path
import pygame
import json

class LaMei(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.attack_interval = 72
        self.last_attack_time = tick
        self.is_attack = False
        self.bullet_speeds = [[0, -2],
                              [1.902, -0.618],
                              [-1.902, -0.618],
                              [1.176, 1.618],
                              [-1.176, 1.618]]

        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.attack_animation =  [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["attack_animation"]]

    def attack(self, status):
        for i in range(5):
            item_name = "lamei_bullet" + str(status.global_ticks) + str(self.index) + str(i)
            status.items[5][item_name] = LaMeiBullet(
                pos=[self.rect.centerx, self.rect.centery],
                json_path=resource_path("./configs/statics/lamei_bullet.json"),
                name="lamei_bullet",
                speed=self.bullet_speeds[i],
                harm=20,
                tick=status.global_ticks,
                item_name=item_name,
                attack_time=0
            )

    def update(self, event, status):
        if self.is_planted:
            if self.is_attack and self.animation_index >= len(self.attack_animation) - 1:
                self.animation = []
                self.animation_index = 0
                self.is_attack = False
                self.attack(status)
            elif not self.is_attack and status.global_ticks - self.last_attack_time >= self.attack_interval:
                self.is_attack = True
                self.last_attack_time = status.global_ticks
                self.animation = self.attack_animation
                self.animation_index = 0
            return super().check_life(event, status)
        return super().not_planted(event, status)
