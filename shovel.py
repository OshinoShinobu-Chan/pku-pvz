from plant import Plant
from status import PLANT_AREA
from utils import resource_path, plant_grid_to_zombie_grid

def click_shovel(status):
    status.items[5]["shovel"] = Shovel(pos=status.mouse_pos,
                                    json_path=resource_path("./configs/statics/shovel.json"),
                                    name="shovel",
                                    tick=None,
                                    life=None,
                                    sun=None,
                                    to_cold_time=None,
                                    item_name="shovel")

class Shovel(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)

    def plant(self, status):
        status.mouse = None
        index = [(self.rect.left - PLANT_AREA.left) // 100,
                 (self.rect.bottom - PLANT_AREA.top) // 120]
        if status.planted_plant[index[0]][index[1]] is not None:
            # del status.items[status.planted_plant[index[0]][index[1]]]
            # status.planted_plant[index[0]][index[1]] = None
            zombie_index = plant_grid_to_zombie_grid(index)
            status.zombies_harm[zombie_index[0]][zombie_index[1]] += 114514
            return False
        else:
            return False