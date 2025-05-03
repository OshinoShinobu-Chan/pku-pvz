from zombie import Zombie
from utils import zombie_grid_to_plant_grid

class ShaChenBaoJiangShi(Zombie):
    def __init__(self, pos, json_path, name, tick, life, item_name):
        super().__init__(pos, json_path, name, tick, life, item_name)
        self.interval = 3
        self.pass_grid = [False for _ in range(11)]
        self.pass_cnt = 0
    
    def check_move(self, status):
        if self.left_index[0] >= 0 and\
            self.pass_grid[self.left_index[0]]:
            return True
        if self.left_index[0] >= 0 and\
            status.zombie_can_move[self.left_index[0]][self.left_index[1]]:
            return True
        if self.left_index[0] >= 0 and self.left_index[0] <= 9:
            plant_index = zombie_grid_to_plant_grid(self.left_index)
            plant = status.planted_plant[plant_index[0]][plant_index[1]]
            if "huangcimei" not in plant and self.pass_cnt < 3:
                self.pass_grid[self.left_index[0]] = True
                self.pass_cnt += 1
                return True
            return False
        return True
    
    def attack(self, status):
        status.zombies_harm[self.left_index[0]][self.left_index[1]] += 1

    def update(self, event, status):
        if self.life <= 0:
            super().remove(status)
            return False
        if self.check_lose(status):
            return True
        
        self.can_move = self.check_move(status)
        self.move(status)
        self.attack(status)
        return True