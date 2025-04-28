from plant import Plant
from sun import Sun
from utils import resource_path

class ZhongHuaXiaoKuMai(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.make_sun = [30, 15, 30]
        self.sun_cold_time = 1200
        self.status = 0
        self.last_sun_time = tick

    def update(self, event, status):
        if self.is_planted:
            if self.sun_cold_time == 1200 and status.winter_zombie_cnt > 0:
                self.sun_cold_time = 1500
            elif self.sun_cold_time == 1500 and status.winter_zombie_cnt <= 0:
                self.sun_cold_time = 1200
            if status.global_ticks - self.last_sun_time >= self.sun_cold_time:
                self.last_sun_time = status.global_ticks
                sun_value = self.make_sun[self.status]
                pos = [self.rect.centerx + self.rect.width // 2, 
                       self.rect.centery + self.rect.height // 2]
                json_path = "sun_middle" if self.status != 1 else "sun_small"
                self.status = (self.status + 1) % 3
                status.items[5]["static_sun" + str(self.index) + str(status.global_ticks)] = \
                    Sun(
                        pos=pos,
                        on_click=None,
                        json_path=resource_path("./configs/statics/" + json_path + ".json"),
                        name="static_sun",
                        sun=sun_value,
                        move_delta=0,
                        tick=status.global_ticks
                    )
            return super().check_life(event, status)
        return super().not_planted(event, status)