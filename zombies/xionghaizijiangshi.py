from zombie import Zombie
from status import ZOMBIE_AREA, GRID_SIZE
import pygame

class XiongHaiZiJiangShi(Zombie):
    def __init__(self, pos, json_path, name, tick, life, item_name):
        super().__init__(pos, json_path, name, tick, life, item_name)
        self.real_life = 200
        self.interval = 4
        self.speed = -1
        self.status = 0
        self.visible_rect = pygame.Rect(self.rect)

    def check_move(self, status):
        if self.right_index[0] < 11:
            return status.zombie_can_move[self.right_index[0]][self.right_index[1]]
        return True
    
    def attack(self, status):
        if self.right_index[0] < 11:
            status.zombies_harm[self.right_index[0]][self.right_index[1]] += 10

    def move(self, status):
        if self.speed == 0 or not self.can_move:
            return
        self.remove(status)
        self.pos[0] += self.speed
        self.rect.move_ip(self.speed, 0)
        self.visible_rect.move_ip(self.speed, 0)
        self.left_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                           (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.right_index = [(self.rect.right - ZOMBIE_AREA.left) // GRID_SIZE[0],
                            (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        if self.right_index[0] < 11 and self.left_index[1] < 5:
            status.zombies[self.left_index[0]][self.left_index[1]][self.item_name] = True
            status.zombies[self.right_index[0]][self.right_index[1]][self.item_name] = True

    def go_left(self, status):
        self.remove(status)
        new_pos = ZOMBIE_AREA.left + GRID_SIZE[0]
        delta = new_pos - self.pos[0]
        self.pos[0] = new_pos
        self.rect.move_ip(delta, 0)
        self.visible_rect.move_ip(delta, 0)
        self.left_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                           (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.right_index = [(self.rect.right - ZOMBIE_AREA.left) // GRID_SIZE[0],
                            (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        if self.left_index[1] < 5:
            status.zombies[self.left_index[0]][self.left_index[1]][self.item_name] = True
            status.zombies[self.right_index[0]][self.right_index[1]][self.item_name] = True
    
    def go_down(self, status):
        self.remove(status)
        self.pos[1] += 1
        self.rect.move_ip(0, 1)
        self.left_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                           (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.right_index = [(self.rect.right - ZOMBIE_AREA.left) // GRID_SIZE[0],
                            (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
    
    def go_up(self, status):
        self.remove(status)
        self.pos[1] -= 1
        self.rect.move_ip(0, -1)
        self.left_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                           (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.right_index = [(self.rect.right - ZOMBIE_AREA.left) // GRID_SIZE[0],
                            (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]

    def check_move(self, status):
        if self.status == 0 and self.left_index[0] >= 0:
            return status.zombie_can_move[self.left_index[0]][self.left_index[1]]
        if self.status == 2 and self.right_index[0] < 11:
            return status.zombie_can_move[self.right_index[0]][self.right_index[1]]
        return True

    def update(self, event, status):
        if self.status == 0 and self.rect.left <= ZOMBIE_AREA.right - 2 * GRID_SIZE[0]:
            self.go_down(status)
            self.status = 1
            self.speed = 1
            return True
        if self.status == 1 and self.rect.top < self.visible_rect.bottom:
            self.go_down(status)
            return True
        if self.status == 1 and self.rect.top >= self.visible_rect.bottom:
            self.go_left(status)
            self.status = 2
            return True
        if self.status == 2 and self.rect.bottom > self.visible_rect.bottom:
            self.go_up(status)
            return True
            
        if self.life <= 0:
            self.remove(status)
            return False
        if self.right_index[0] >= 11:
            self.remove(status)
            return False
        
        if status.global_ticks % self.interval != 0:
            return True
        self.can_move = self.check_move(status)
        self.move(status)
        self.attack(status)
        return True

    def draw(self, surface, tick):
        cliped_rect = self.rect.clip(self.visible_rect)
        cliped_surface = surface.subsurface(cliped_rect)
        image_pos_in_clip = (self.rect.x - cliped_rect.x, self.rect.y - cliped_rect.y)
        cliped_surface.blit(self.image, image_pos_in_clip)
        