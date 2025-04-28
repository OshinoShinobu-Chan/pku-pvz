from plant import Plant
from sun import Sun
from utils import resource_path

class DongQingWeiMao(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.sun_cold_time = 1200
        self.make_sun = 50
        self.last_sun_time = tick

    def update(self, event, status):
        if self.is_planted:
            if status.global_ticks - self.last_sun_time >= self.sun_cold_time:
                self.last_sun_time = status.global_ticks
                pos = [self.rect.centerx + self.rect.width // 2, 
                       self.rect.centery + self.rect.height // 2]
                status.items[4]["static_sun" + str(self.index) + str(status.global_ticks)] = \
                    Sun(
                        pos=pos,
                        on_click=None,
                        json_path=resource_path("./configs/statics/sun.json"),
                        name="static_sun",
                        sun=self.make_sun,
                        move_delta=0,
                        tick=status.global_ticks
                    )
            return super().check_life(event, status)
        return super().not_planted(event, status)