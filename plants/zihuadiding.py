from plant import Plant
from zombies.fake_zombie import FakeZombie
from utils import resource_path, plant_grid_to_zombie_grid

class ZiHuaDiDing(Plant):
    def __init__(self, pos, json_path, name, tick, life, sun, to_cold_time, item_name):
        super().__init__(pos, json_path, name, tick, life, sun, to_cold_time, item_name)
        self.aim = None
        
    def attack(self, status):
        aim = status.items[4][self.aim]
        pos = aim.rect.center
        json_path = aim.json_path
        life = aim.life
        item_name = "fake_zombie_" + str(self.pos) + str(status.global_ticks)
        aim.harm(status)

        status.items[4][item_name] = FakeZombie(
            pos=pos,
            json_path=json_path,
            name="fake_zombie",
            tick=status.global_ticks,
            life=life,
            item_name=item_name
        )

    def check_aim(self, status):
        zombie_index = plant_grid_to_zombie_grid(self.index)
        if len(status.zombies[zombie_index[0]][zombie_index[1]]) > 0:
            for zombie in status.zombies[zombie_index[0]][zombie_index[1]]:
                if self.rect.colliderect(status.items[4][zombie].rect):
                    self.aim = zombie
                    return True
        return False

    def update(self, event, status):
        if self.is_planted:
            if self.check_aim(status):
                self.attack(status)
                super().harm()
            return super().check_life(event, status)
        return super().not_planted(event, status)
    