from random import randrange, seed, randint
from test_zombie import TestZombie
from status import ZOMBIE_AREA, Season
from zombies.shigongjiangshi import ShiGongJiangShi
from victory import VictoryChecker

class ZombieSpawner:
    def __init__(self, start_tick, round):
        self.start_tick = start_tick
        self.round = round
        self.plan = 50 if round % 4 != 2 else 100
        self.wait = 240 if self.plan == 50 else 120
        self.finish = False
        seed()

    def random_pos(self):
        return randrange(0, 5)

    def random_zombie(self, status):
        if self.plan == 0:
            return None
        if self.plan == 1:
            self.plan = 0
            return "shigongjiangshi"
        r = randint(0, 7)
        if r % 7 <= 3:
            self.plan -= 1
            return "shigongjiangshi"
        else:
            self.plan -= 2
            match status.season:
                case Season.SPRING:
                    return "shachenbaojiangshi"
                case Season.SUMMER:
                    return "xionghaizijiangshi"
                case Season.AUTUMN:
                    return "toucaijiangshi"
                case Season.WINTER:
                    return "lanjiaojiangshi"

    def excute(self, status, event):
        if (status.global_ticks - self.start_tick) % self.wait == 0:
            zombie_name = self.random_zombie(status) if self.plan < 100 else "zhihuijiangshi"
            if zombie_name is None:
                status.executors.append(ZombieChecker(status.global_ticks))
                return False
            index = [10, self.random_pos()]
            
            zombie_name = "shigongjiangshi"
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
            if status.zombie_round >= 16:
                status.executors.append(VictoryChecker())
                return False
            status.executors.append(ZombieSpawner(status.global_ticks, status.zombie_round))
            status.zombie_round += 1
            if status.zombie_round == 4:
                status.season = Season.SUMMER
            elif status.zombie_round == 8:
                status.season = Season.AUTUMN
            elif status.zombie_round == 12:
                status.season = Season.WINTER
            return False
        return True