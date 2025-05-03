from merge import Merge
from utils import resource_path
from status import GamePhase, Season
from start import Start

class Victory:
    def __init__(self, tick, is_victory):
        self.start_tick = tick
        self.initailized = False
        self.is_victory = is_victory

    def excute(self, status, event):
        if status.global_ticks - self.start_tick >= 150:
            status.game_phase = GamePhase.START
            status.items = [{} for _ in range(6)]
            status.static_items.clear()
            status.backgrounds.clear()
            status.executors.clear()
            status.selected_plants = [None for _ in range(8)]
            status.selected_plants_cnt = 0
            status.global_ticks = 0
            status.mouse_available = True
            status.mouse = None
            status.sun = 0
            status.planted_plant = [[None for _ in range(5)] for _ in range(9)]
            status.planted_plant_cnt = 0
            status.planted_single_harm = [[0 for _ in range(5)] for _ in range(9)]
            status.planted_aoe_harm = [[0 for _ in range(5)] for _ in range(9)]
            status.zombies = [[{} for _ in range(5)] for _ in range(11)]
            status.zombies_cnt = 0
            status.zombies_harm = [[0 for _ in range(5)] for _ in range(11)]
            status.zombies_total_life = 0
            status.zombies_origin_total_life = 0
            status.zombie_round = 0
            status.zombie_can_move = [[True for _ in range(5)] for _ in range(11)]
            status.winter_zombie_cnt = 0
            status.bullets = [[{} for _ in range(5)] for _ in range(9)]
            status.bullets_cnt = 0
            status.suanzao_aim = None
            status.season = Season.SPRING
            status.victory = None
            from game import GameBackground
            status.executors.append(GameBackground())
            status.executors.append(Start())
            return True
        if not self.initailized:
            self.initailized = True
            if self.is_victory:
                json_path = resource_path("./configs/texts/victory.json")
            else:
                json_path = resource_path("./configs/texts/lose.json")
            status.items[5]["victory"] = Merge(
                pos=[640, 360],
                json_path=json_path,
                name="victory",
                start_tick=status.global_ticks,
                duration_ms=1000,
                static_time=90
            )
        return True

class VictoryChecker:
    def excute(self, status, event):
        if status.zombies_total_life <= 0:
            status.executors.append(Victory(
                status.global_ticks,
                True
            ))
            return False
        return True