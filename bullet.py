from item import Item
from status import PLANT_AREA, GRID_SIZE

class Bullet(Item):
    def __init__(self, pos, json_path, name, speed, harm, tick, item_name, attack_time):
        super().__init__(pos, json_path, name)
        self.speed = speed
        self.harm = harm
        self.start_tick = tick
        self.index = [(self.rect.centerx - PLANT_AREA.left) // GRID_SIZE[0],
                      (self.rect.centery - PLANT_AREA.top) // GRID_SIZE[1]]
        self.item_name = item_name
        self.attack_time = attack_time
        self.last_attack_time = tick
        self.in_grid = True
    
    def remove(self, status):
        if self.in_grid and self.item_name in status.bullets[self.index[0]][self.index[1]]:
            del status.bullets[self.index[0]][self.index[1]][self.item_name]

    def move(self, status):
        '''
        leave for child to implement
        '''
        pass

    def attack(self, status):
        if not self.in_grid:
            return
        status.planted_aoe_harm[self.index[0]][self.index[1]] += self.harm

    def check_exist(self, status):
        if self.pos[0] >= PLANT_AREA.right + 300:
            self.remove(status)
            return False
        return True

    def update(self, event, status):
        if status.global_ticks - self.last_attack_time >= self.attack_time:
            self.last_attack_time = status.global_ticks
            self.attack(status)
        if status.global_ticks % 3 != 0:
            return True
        if not self.check_exist(status):
            return False
        self.move(status)
        return True

        