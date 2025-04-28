from bullet import Bullet
from status import PLANT_AREA, GRID_SIZE

class LuoMoBullet(Bullet):
    def __init__(self, pos, json_path, name, speed, harm, tick, item_name, attack_time):
        super().__init__(pos, json_path, name, speed, harm, tick, item_name, attack_time)

    def move(self, status):
        if self.speed == 0:
            return
        self.remove(status)
        self.pos[0] += self.speed
        self.rect.move_ip(self.speed, 0)
        self.index = [(self.rect.centerx - PLANT_AREA.left) // GRID_SIZE[0],
                      (self.rect.centery - PLANT_AREA.top) // GRID_SIZE[1]]
        if self.index[0] < 9:
            status.bullets[self.index[0]][self.index[1]][self.item_name] = True
        else:
            self.in_grid = False