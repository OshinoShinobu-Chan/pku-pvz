from plant import Plant
from bullets.suanzao_bullet import SuanZaoBullet
from utils import resource_path
from status import PLANT_AREA
from plants.aim import Aim
import pygame
import json

class SuanZao(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.last_attack_time = tick
        self.attack_interval = 900
        self.status = 0
        self.aim_pic = ""
        self.aim = None

        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.attack_animation = [pygame.transform.smoothscale(pygame.image.load(
                                    resource_path(img)
                                ).convert_alpha(), self.size)
                                    for img in config["attack_animation"]]
        self.dark_image = pygame.transform.smoothscale(
            pygame.image.load(resource_path(config["image_paths"]["focus"])).convert_alpha(), self.size)
        self.normal_image = pygame.transform.smoothscale(
            pygame.image.load(resource_path(config["image_paths"]["normal"])).convert_alpha(), self.size)

    def attack(self, status):
        item_name = "suanzao_bullet" + str(status.global_ticks)
        harm = 900
        status.items[5][item_name] = SuanZaoBullet(
            pos=self.pos,
            json_path=resource_path("./configs/statics/suanzaojianongpao_bullet.json"),
            name="suanzao_bullet",
            speed=114514,
            harm=harm,
            tick=status.global_ticks,
            item_name=item_name,
            attack_time=114514,
            aim=self.aim
        )
    
    def update(self, event, status):
        if not self.is_planted:
            return super().not_planted(event, status)
        if self.attack_interval == 900 and status.winter_zombie_cnt > 0:
            self.attack_interval = 1125
        elif self.attack_interval == 1125 and status.winter_zombie_cnt <= 0:
            self.attack_interval = 900
        if self.status == 3 and self.animation_index >= len(self.attack_animation) - 1:
            self.attack(status)
            self.status = 0
            self.animation = []
            self.animation_index = 0
            self.last_attack_time = status.global_ticks
        elif self.status == 2 and status.suanzao_aim is not None and\
              status.suanzao_aim[0] == -1:
            self.status = 1
            status.suanzao_aim = None
        elif self.status == 2 and status.suanzao_aim is not None:
            self.aim = status.suanzao_aim
            print("aim: " + str(self.aim))
            status.suanzao_aim = None
            self.status = 3
            self.animation = self.attack_animation
            self.animation_index = 0
        elif self.status == 1:
            for e in event:
                if e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                    if self.rect.collidepoint(status.mouse_pos):
                        self.status = 2
                        self.image = self.normal_image
                        status.items[5]["suanzao_aim"] = Aim(
                            pos=status.mouse_pos,
                            json_path=resource_path("./configs/statics/aim.json"),
                            name="suanzai_aim",
                            tick=status.global_ticks,
                            life=114514,
                            sun=114514,
                            to_cold_time=114514,
                            item_name="suanzai_aim"
                        )
                    break
        elif self.status == 0 and status.global_ticks - self.last_attack_time >= self.attack_interval:
            self.status = 1
            self.image = self.dark_image
        return super().check_life(event, status)
            


                    