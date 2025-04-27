from zombie import Zombie
from utils import zombie_grid_to_plant_grid

class TestZombie(Zombie):
    def __init__(self, pos, json_path, name, tick, life, item_name):
        super().__init__(pos, json_path, name, tick, life, item_name)
        self.harm_ = 200

    def attack(self, status):
        if status.global_ticks % 30 == 0:
            status.zombies_harm[self.left_index[0]][self.left_index[1]] += self.harm_