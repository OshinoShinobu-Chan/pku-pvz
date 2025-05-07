from zombie import Zombie
from utils import resource_path
from status import ZOMBIE_AREA, GRID_SIZE
import pygame
import json

class FakeZombie(Zombie):
    def __init__(self, pos, json_path, name, tick, life, item_name):
        super().__init__(pos, json_path, name, tick, life, item_name)
        with open(resource_path(json_path), "r") as f:
            config = json.load(f)

        self.image = pygame.transform.flip((pygame.transform.smoothscale(
                        pygame.image.load(
                            resource_path(
                                config["image_paths"]["normal"]
                            )
                        ).convert_alpha(), self.size)), True, False)
        self.speed = 1
       
    def harm(self, status, harm_num=None):
        if harm_num is None:
            self.life = 0
        else:
            self.life -= harm_num if harm_num <= self.life else self.life

    def check_move(self, status):
        if self.right_index[0] >= 11:
            return None
        for zombie in status.zombies[self.right_index[0]][self.right_index[1]]:
            if self.rect.colliderect(status.items[4][zombie].rect):
                return zombie
        return None

    def attack(self, status, aim_name):
        status.items[4][aim_name].harm(status, 3)

    def update(self, event, status):
        if self.life <= 0 or self.rect.left >= 1280:
            self.remove(status)
            return False
        
    def check_harm(self, status):
        harm = 0
        if self.right_index[0] >= 11:
            return 0
        for zombie in status.zombies[self.right_index[0]][self.right_index[1]]:
            if self.rect.colliderect(status.items[4][zombie].rect):
                harm += 3
        return harm
    
    def move(self, status):
        if self.speed == 0 or not self.can_move:
            return
        self.remove(status)
        self.pos[0] += self.speed
        self.rect.move_ip(self.speed, 0)
        self.left_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                           (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.right_index = [(self.rect.right - ZOMBIE_AREA.left) // GRID_SIZE[0],
                            (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        if self.right_index[0] < 11:
            status.fake_zombies[self.right_index[0]][self.right_index[1]][self.item_name] = True
            status.fake_zombies[self.left_index[0]][self.left_index[1]][self.item_name] = True

    def remove(self, status):
        if self.right_index[1] < 11 and\
              self.item_name in status.fake_zombies[self.right_index[0]][self.right_index[1]]:
            del status.fake_zombies[self.right_index[0]][self.right_index[1]][self.item_name]
            del status.fake_zombies[self.left_index[0]][self.left_index[1]][self.item_name]

    def update(self, event, status):
        if self.life <= 0 or self.rect.left > 1280:
            self.remove(status)
            return False
        
        if status.global_ticks % self.interval != 0:
            return True
        zombie_name = self.check_move(status) 
        if zombie_name is not None:
            self.attack(status, zombie_name)
            self.harm(status, self.check_harm(status))
        else:
            self.move(status)
        
        return True