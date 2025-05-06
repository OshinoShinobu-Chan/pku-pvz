from plant import Plant
from bullets.luomobullet import LuoMoBullet
from utils import resource_path

class LuoMo(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.attack_time = 120
        self.short_attack_time = 20
        self.last_attack_time = tick
        self.status = 3

    def attack(self, status):
        if (self.status == 0 or self.status == 1 or self.status == 2) and \
            status.global_ticks - self.last_attack_time >= self.short_attack_time:
            self.last_attack_time = status.global_ticks
            status.bullets_cnt += 1
            self.status += 1
            bullet_name = "bullet_" + str(status.bullets_cnt)
            status.items[5][bullet_name] = LuoMoBullet(
                pos = [self.pos[0] + 40, self.pos[1]],
                json_path=resource_path("./configs/statics/luomo_bullet.json"),
                name=bullet_name,
                speed=5,
                harm=30,
                tick=status.global_ticks,
                item_name=bullet_name,
                attack_time=50
            )
        if self.status == 3 and status.global_ticks - self.last_attack_time >= self.attack_time\
            and self.check_aim(status):
            self.status = 0

    def check_aim(self, status):
        for i in range(self.index[0] + 1, 11):
            if len(status.zombies[i][self.index[1]]) > 0:
                return True
        return False
    
    def update(self, event, status):
        if self.is_planted and status.global_ticks % 3 == 0:
            if self.attack_time == 120 and status.winter_zombie_cnt > 0:
                self.attack_time = 150
                self.short_attack_time = 25
            elif self.attack_time == 150 and status.winter_zombie_cnt <= 0:
                self.attack_time = 120
                self.short_attack_time = 20
            self.attack(status)
        return super().update(event, status)