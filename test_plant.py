from plant import Plant
from utils import plant_grid_to_zombie_grid

class TestPlant(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.harm_ = 200

    def attack(self, status):
        if status.global_ticks % 30 == 0:
            status.planted_aoe_harm[self.index[0]][self.index[1]] += self.harm_

    def update(self, event, status):
        if self.is_planted:
            self.attack(status)
        return super().update(event, status)