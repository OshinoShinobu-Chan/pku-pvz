from item import Item
from status import ZOMBIE_AREA, GRID_SIZE
from utils import zombie_grid_to_plant_grid

class Zombie(Item):
    def __init__(self, pos, json_path, name, tick, life, item_name):
        super().__init__(pos, json_path, name)
        self.start_tick = tick
        self.life = life
        self.speed = -1
        self.left_index = [(self.rect.left - ZOMBIE_AREA.left) // GRID_SIZE[0],
                           (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.right_index = [(self.rect.right - ZOMBIE_AREA.left) // GRID_SIZE[0],
                            (self.rect.centery - ZOMBIE_AREA.top) // GRID_SIZE[1]]
        self.can_move = True
        self.item_name = item_name
        
    def remove(self, status):
        # move left
        if self.item_name in status.zombies[self.left_index[0]][self.left_index[1]]:
            del status.zombies[self.left_index[0]][self.left_index[1]][self.item_name]
        # move right
        if self.item_name in status.zombies[self.right_index[0]][self.right_index[1]]:
            del status.zombies[self.right_index[0]][self.right_index[1]][self.item_name]
    
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
        if self.left_index[0] >= 0:
            status.zombies[self.left_index[0]][self.left_index[1]][self.item_name] = True
            status.zombies[self.right_index[0]][self.right_index[1]][self.item_name] = True

    def check_move(self, status):
        if self.left_index[0] >= 0:
            return status.zombie_can_move[self.left_index[0]][self.left_index[1]]
        return True
    
    def harm(self, status, harm_num=None):
        if harm_num is None:
            self.life = 0
            status.zombies_total_life -= self.life
        else:
            self.life -= harm_num if harm_num <= self.life else self.life
            status.zombies_total_life -= harm_num if harm_num <= self.life else self.life

    def update(self, event, status):
        if self.life <= 0:
            self.remove(status)
            return False
        
        # normal move, check tick first
        if status.global_ticks % 3 != 0:
            return True
        self.can_move = self.check_move(status)
        self.move(status)
        return True
    
    def attack(self, status):
        '''
        leave for child to implement
        '''
        pass
        