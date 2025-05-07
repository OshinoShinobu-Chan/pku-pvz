from random import randrange, seed, randint
from test_zombie import TestZombie
from status import ZOMBIE_AREA, Season, PLANT_AREA, GRID_SIZE
from zombies.shigongjiangshi import ShiGongJiangShi
from zombies.shachenbaojiangshi import ShaChenBaoJiangShi
from zombies.xionghaizijiangshi import XiongHaiZiJiangShi
from zombies.lanjiaojiangshi import LanJiaoJiangShi
from zombies.wacaijiangshi import WaCaiJiangShi
from victory import VictoryChecker

class ZombieSpawner:
    def __init__(self, start_tick, round):
        self.start_tick = start_tick
        self.round = round
        self.plan = 50 if round % 4 != 2 else 100
        self.wait = 240 if self.plan == 50 else 90
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
                    return "wacaijiangshi"
                case Season.WINTER:
                    return "lanjiaojiangshi"

    def excute(self, status, event):
        if (status.global_ticks - self.start_tick) % self.wait == 0:
            zombie_name = self.random_zombie(status) if self.plan < 100 else "zhihuijiangshi"
            if zombie_name == "zhihuijiangshi":
                self.plan -= 1
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
                case "zhihuijiangshi":
                    z = ShiGongJiangShi(
                        pos=pos,
                        json_path=status.zombie_configs[zombie_name]["json_path"],
                        name=item_name,
                        tick=status.global_ticks,
                        life=status.zombie_configs[zombie_name]["life"],
                        item_name=item_name,
                    )
                case "shachenbaojiangshi":
                    z = ShaChenBaoJiangShi(
                        pos=pos,
                        json_path=status.zombie_configs[zombie_name]["json_path"],
                        name=item_name,
                        tick=status.global_ticks,
                        life=status.zombie_configs[zombie_name]["life"],
                        item_name=item_name,
                    )
                case "xionghaizijiangshi":
                    z = XiongHaiZiJiangShi(
                        pos=pos,
                        json_path=status.zombie_configs[zombie_name]["json_path"],
                        name=item_name,
                        tick=status.global_ticks,
                        life=status.zombie_configs[zombie_name]["life"],
                        item_name=item_name,
                    )
                case "lanjiaojiangshi":
                    status.winter_zombie_cnt += 1
                    z = LanJiaoJiangShi(
                        pos=pos,
                        json_path=status.zombie_configs[zombie_name]["json_path"],
                        name=item_name,
                        tick=status.global_ticks,
                        life=status.zombie_configs[zombie_name]["life"],
                        item_name=item_name,
                    )
                case "wacaijiangshi":
                    aim = [randint(0, 8), randint(0, 4)]
                    posx = PLANT_AREA.left + (aim[0] * 2 + 1) * GRID_SIZE[0] / 2
                    z = WaCaiJiangShi(
                        pos=[posx, -60],
                        json_path=status.zombie_configs[zombie_name]["json_path"],
                        name=item_name,
                        tick=status.global_ticks,
                        life=status.zombie_configs[zombie_name]["life"],
                        item_name=item_name,
                        aim=aim
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
            if status.zombie_round >= 15:
                status.executors.append(VictoryChecker())
                return False
            status.executors.append(ZombieSpawner(status.global_ticks, status.zombie_round))
            if status.zombie_round == 3:
                status.season = Season.SPRING
            elif status.zombie_round == 7:
                status.season = Season.SUMMER
            elif status.zombie_round == 11:
                status.season = Season.AUTUMN
            status.zombie_round += 1
            return False
        return True