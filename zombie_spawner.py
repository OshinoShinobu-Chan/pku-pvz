from random import randrange, seed
from test_zombie import TestZombie
from status import ZOMBIE_AREA
from zombies.shigongjiangshi import ShiGongJiangShi

class ZombieSpawner:
    def __init__(self, start_tick, round):
        self.start_tick = start_tick
        self.round = round
        self.zombie_plan = 50 if round % 4 != 2 else 100
        self.difficulty_cnt = [0 for _ in range(3)]
        self.difficulty_plan = [20, 20, 10] if self.zombie_plan == 50 else [40, 40, 20]
        self.wait = 240 if self.zombie_plan == 50 else 120
        self.finish = False
        seed()

    def random_pos(self):
        return randrange(0, 5)

    def random_zombie(self, status):
        enable_difficulty = [i for i in range(3) 
                            if self.difficulty_cnt[i] < self.difficulty_plan[i] and
                            len(status.zombie_difficulties[i]) != 0]
        if len(enable_difficulty) == 0:
            return None
        difficulty = enable_difficulty[randrange(0, len(enable_difficulty))]
        self.difficulty_cnt[difficulty] += 1
        return status.zombie_difficulties[difficulty][randrange(0, len(status.zombie_difficulties[difficulty]))]

    def excute(self, status, event):
        if (status.global_ticks - self.start_tick) % self.wait == 0:
            zombie_name = self.random_zombie(status)
            if zombie_name is None:
                status.executors.append(ZombieChecker(status.global_ticks))
                return False
            index = [10, self.random_pos()]
            
            item_name = zombie_name + "_" + str(status.zombies_cnt)
            status.zombies_cnt += 1
            pos = [
                ZOMBIE_AREA.left + (index[0] * 2 + 1) * 100 // 2,
                ZOMBIE_AREA.top + (index[1] * 2 + 1) * 120 // 2,
            ]
            match zombie_name:
                case "shigongjiangshi":
                    z = ShiGongJiangShi(
                        pos=pos,
                        json_path=status.zombie_configs[zombie_name]["json_path"],
                        name=item_name,
                        tick=status.global_ticks,
                        life=status.zombie_configs[zombie_name]["life"],
                        item_name=item_name,
                    )
                case _:
                    z = TestZombie(
                        pos=pos,
                        json_path=status.zombie_configs[zombie_name]["json_path"],
                        name=item_name,
                        tick=status.global_ticks,
                        life=status.zombie_configs[zombie_name]["life"],
                        item_name=item_name,
                    )
            status.items[4][item_name] = z
            status.zombies_total_life += z.life
            status.zombies_origin_total_life += z.life
            return True
        return True
            
class ZombieChecker:
    def __init__(self, start_tick):
        self.start_tick = start_tick

    def excute(self, status, event):
        if (status.global_ticks - self.start_tick) % 3 != 0:
            return True
        if status.zombies_total_life < status.zombies_origin_total_life * 0.3 or\
            (status.global_ticks - self.start_tick) // 60 >= 15:
            status.executors.append(ZombieSpawner(status.global_ticks, status.zombie_round))
            status.season = status.zombie_round // 4
            status.zombie_round += 1
            return False
        return True