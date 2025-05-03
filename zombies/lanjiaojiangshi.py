from zombie import Zombie
from plant import QIAO_MU
from utils import zombie_grid_to_plant_grid

class LanJiaoJiangShi(Zombie):
    def __init__(self, pos, json_path, name, tick, life, item_name):
        super().__init__(pos, json_path, name, tick, life, item_name)
        self.real_life = 270
        self.interval = 4
        self.is_first_plant = False

    def attack(self, status):
        if self.is_first_plant or self.left_index[0] < 1 or self.left_index[0] >= 10:
            status.zombies_harm[self.left_index[0]][self.left_index[1]] += 3
            return
        plant_index = zombie_grid_to_plant_grid(self.left_index)
        plant = status.planted_plant[plant_index[0]][plant_index[1]]
        if plant is not None:
            for p in QIAO_MU:
                if p in plant:
                    self.is_first_plant = True
                    return
            status.items[3][plant].harm()
            self.is_first_plant = True

    def update(self, event, status):
        if self.life <= 0:
            status.winter_zombie_cnt -= 1
            super().remove(status)
            return False
        if self.check_lose(status):
            return True
        if self.life <= self.real_life:
            self.interval = 6

        if status.global_ticks % self.interval != 0:
            return True
        self.can_move = super().check_move(status)
        self.move(status)
        self.attack(status)
        return True
            