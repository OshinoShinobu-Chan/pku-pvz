from button import Button
from enum import Enum, auto
from copy import deepcopy
from plant import Plant

class PlantCardStatus(Enum):
    NORMAL = auto(),
    COLDTIME = auto(),

def on_click_wrapper(name, plant, json_path):
    def on_click(status):
        status.planted_plant_cnt += 1
        p = Plant(pos=plant.pos, 
                  json_path=json_path, 
                  name=plant.name,
                  tick=status.global_ticks,
                  life=plant.life,
                  sun=plant.sun,
                  to_cold_time=plant.to_cold_time)
        status.items[name + "_" + str(status.planted_plant_cnt)] = p
    return on_click

def to_cold_time_wrapper(card):
    def to_cold_time():
        card.status = PlantCardStatus.COLDTIME
        card.already_cold_time = 0
    return to_cold_time

class PlantCard(Button):
    def __init__(self, pos, json_path, name, cold_time, sun, start_tick, life, plant_name):
        self.plant = Plant(pos=pos, 
                           json_path=json_path, 
                           name="planted_" + plant_name, 
                           tick=start_tick, 
                           life=life,
                           sun=sun,
                           to_cold_time=to_cold_time_wrapper(self))
        super().__init__(pos, on_click_wrapper(name, self.plant, json_path), json_path, name)
        self.status = PlantCardStatus.NORMAL
        self.cold_time = cold_time * 60
        self.sun = sun
        self.already_cold_time = 0  # Time that already in cold status
        self.start_tick = start_tick
        self.life = life

    def check_enable_(self, sun):
        return self.status != PlantCardStatus.COLDTIME and sun >= self.sun

    
    
    def update(self, event, status):
        # if (status.global_ticks - self.start_tick) % 3 != 0:
        #     super().update(event, status)
        #     return True
        if self.status == PlantCardStatus.COLDTIME:
            self.already_cold_time += 1
        if self.already_cold_time >= self.cold_time:
            self.status = PlantCardStatus.NORMAL
            self.already_cold_time = 0
        self.enable = self.check_enable_(status.sun)
        super().update(event, status)
        return True
        