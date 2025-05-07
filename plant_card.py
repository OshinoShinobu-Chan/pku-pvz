from button import Button
from enum import Enum, auto
from plant import Plant
from status import Season
from static import Static
from text import Text
from utils import resource_path
from test_plant import TestPlant
from plants.zhonghuaxiaokumai import ZhongHuaXiaoKuMai
from plants.baojingxiaokumai import BaoJingXiaoKuMai
from plants.luomo import LuoMo
from plants.dongqingweimao import DongQingWeiMao
from plants.dihuang import DiHuang
from plants.banzhongcao import BanZhongCao
from plants.huangcimei import HuangCiMei
from plants.li import Li
from plants.lamei import LaMei
from plants.suanzao import SuanZao
from plants.heidanshu import HeiDanShu
from plants.zihuadiding import ZiHuaDiDing

class PlantCardStatus(Enum):
    NORMAL = auto(),
    COLDTIME = auto(),

def on_click_wrapper(name, plant, json_path, plant_name):
    def on_click(status):
        status.planted_plant_cnt += 1
        match plant_name:
            case "zhonghuaxiaokumai":
                p = ZhongHuaXiaoKuMai(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "baojingxiaokumai":
                p = BaoJingXiaoKuMai(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "luomo":
                p = LuoMo(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "dongqingweimao":
                p = DongQingWeiMao(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "dihuang":
                p = DiHuang(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "banzhongcao":
                p = BanZhongCao(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "huangcimei":
                p = HuangCiMei(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "li":
                p = Li(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "lamei":
                p = LaMei(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "suanzaojianongpao":
                p = SuanZao(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "heidanshu":
                p = HeiDanShu(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case "zihuadiding":
                p = ZiHuaDiDing(
                    pos=plant.pos,
                    json_path=json_path,
                    name=plant.name,
                    tick=status.global_ticks,
                    life=plant.life,
                    sun=plant.sun,
                    to_cold_time=plant.to_cold_time,
                    item_name=name + "_" + str(status.planted_plant_cnt)
                )
            case _:
                p = Plant(pos=plant.pos, 
                        json_path=json_path, 
                        name=plant.name,
                        tick=status.global_ticks,
                        life=plant.life,
                        sun=plant.sun,
                        to_cold_time=plant.to_cold_time,
                        item_name=name + "_" + str(status.planted_plant_cnt))
        status.items[5][name + "_" + str(status.planted_plant_cnt)] = p
    return on_click

def to_cold_time_wrapper(card):
    def to_cold_time():
        card.status = PlantCardStatus.COLDTIME
        card.already_cold_time = 0
    return to_cold_time



class PlantCard(Button):
    def __init__(self, pos, json_path, name, cold_time, sun, start_tick, life, plant_name, index=0):
        self.index = index
        match plant_name:
            case "zhonghuaxiaokumai":
                self.plant = ZhongHuaXiaoKuMai(pos=pos, 
                                        json_path=json_path, 
                                        name="planted_" + plant_name, 
                                        tick=start_tick, 
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="ZhongHuaXiaoKuMai")
                self.season = None
            case "baojingxiaokumai":
                self.plant = BaoJingXiaoKuMai(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="BaoJingXiaoKuMai")
                self.season = None
            case "luomo":
                self.plant = LuoMo(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="luomo")
                self.season = None
            case "dongqingweimao":
                self.plant = DongQingWeiMao(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="dongqingweimao")
                self.season = None
            case "dihuang":
                self.plant = DiHuang(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="dihuang")
                self.season = None
            case "banzhongcao":
                self.plant = BanZhongCao(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="banzhongcao")
                self.season = None
            case "huangcimei":
                self.plant = HuangCiMei(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="huangcimei")
                self.season = Season.SPRING
            case "li":
                self.plant = Li(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="li")
                self.season = Season.SUMMER
            case "lamei":
                self.plant = LaMei(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="lamei")
                self.season = Season.WINTER
            case "suanzaojianongpao":
                self.plant = SuanZao(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="suanzaojianongpao")
                self.season = Season.AUTUMN
            case "heidanshu":
                self.plant = HeiDanShu(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="heidanshu")
                self.season = None
            case "zihuadiding":
                self.plant = ZiHuaDiDing(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="heidanshu")
                self.season = None
            case _:
                self.plant = Plant(pos=pos, 
                                json_path=json_path, 
                                name="planted_" + plant_name, 
                                tick=start_tick, 
                                life=life,
                                sun=sun,
                                to_cold_time=to_cold_time_wrapper(self),
                                item_name="template_plant")
                self.season = None
        super().__init__(pos, on_click_wrapper(name, self.plant, json_path, plant_name), json_path, name)
        self.status = PlantCardStatus.NORMAL
        self.cold_time = cold_time * 60
        self.sun = sun
        self.already_cold_time = 0  # Time that already in cold status
        self.start_tick = start_tick
        self.life = life
        self.masked = False
        self.cold_texted = False

    def check_enable_(self, sun, on_mouse, season):
        return self.status != PlantCardStatus.COLDTIME and\
                sun >= self.sun and\
                on_mouse is None and\
                (self.season is None or\
                self.season == season)
    
    def update(self, event, status):
        if self.status == PlantCardStatus.COLDTIME and not self.cold_texted:
            self.already_cold_time += 1
            left_cold_time_ms = (self.cold_time - self.already_cold_time) / 60
            self.delta = 10 if len(f"{left_cold_time_ms:.1f}") == 3 else 0
            status.items[5]["cold_time_" + str(self.index)] = Text(
                pos=[self.rect.centerx + self.delta, self.rect.centery - 10],
                json_path=resource_path("./configs/texts/cold_time.json"),
                name="cold_time",
                text=f"{left_cold_time_ms:.1f}",
                font_size=40
            )
            self.cold_texted = True
        if self.status == PlantCardStatus.COLDTIME and self.cold_texted:
            self.already_cold_time += 1
            left_cold_time_ms = (self.cold_time - self.already_cold_time) / 60
            if self.delta == 0 and len(f"{left_cold_time_ms:.1f}") == 3:
                self.delta = 10
                status.items[5]["cold_time_" + str(self.index)].pos[0] += 10
                status.items[5]["cold_time_" + str(self.index)].rect.move_ip(10, 0)
            status.items[5]["cold_time_" + str(self.index)].set_text(f"{left_cold_time_ms:.1f}")
        if self.already_cold_time >= self.cold_time:
            del status.items[5]["cold_time_" + str(self.index)]
            self.status = PlantCardStatus.NORMAL
            self.already_cold_time = 0
            self.cold_texted = False
        self.enable = self.check_enable_(status.sun, status.mouse, status.season)
        if not self.enable and not self.masked:
            status.items[5]["mask_" + str(self.index)] = Static(
                pos=self.rect.center,
                json_path=resource_path("./configs/statics/mask.json"),
                name="mask"
            )
            self.masked = True
        if self.enable and self.masked:
            if "mask_" + str(self.index) in status.items[5]:
                del status.items[5]["mask_" + str(self.index)]
            self.masked = False
        super().update(event, status)
        return True