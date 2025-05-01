from button import Button
from enum import Enum, auto
from plant import Plant
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
    def __init__(self, pos, json_path, name, cold_time, sun, start_tick, life, plant_name):
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
            case "baojingxiaokumai":
                self.plant = BaoJingXiaoKuMai(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="BaoJingXiaoKuMai")
            case "luomo":
                self.plant = LuoMo(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="luomo")
            case "dongqingweimao":
                self.plant = DongQingWeiMao(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="dongqingweimao")
            case "dihuang":
                self.plant = DiHuang(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="dihuang")
            case "banzhongcao":
                self.plant = BanZhongCao(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="banzhongcao")
            case "huangcimei":
                self.plant = HuangCiMei(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="huangcimei")
            case "li":
                self.plant = Li(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="li")
            case "lamei":
                self.plant = LaMei(pos=pos,
                                        json_path=json_path,
                                        name="planted_" + plant_name,
                                        tick=start_tick,
                                        life=life,
                                        sun=sun,
                                        to_cold_time=to_cold_time_wrapper(self),
                                        item_name="lamei")
            case _:
                self.plant = Plant(pos=pos, 
                                json_path=json_path, 
                                name="planted_" + plant_name, 
                                tick=start_tick, 
                                life=life,
                                sun=sun,
                                to_cold_time=to_cold_time_wrapper(self),
                                item_name="template_plant")
        super().__init__(pos, on_click_wrapper(name, self.plant, json_path, plant_name), json_path, name)
        self.status = PlantCardStatus.NORMAL
        self.cold_time = cold_time * 60
        self.sun = sun
        self.already_cold_time = 0  # Time that already in cold status
        self.start_tick = start_tick
        self.life = life

    def check_enable_(self, sun, on_mouse):
        return self.status != PlantCardStatus.COLDTIME and sun >= self.sun and on_mouse is None
    
    def update(self, event, status):
        # if (status.global_ticks - self.start_tick) % 3 != 0:
        #     super().update(event, status)
        #     return True
        if self.status == PlantCardStatus.COLDTIME:
            self.already_cold_time += 1
        if self.already_cold_time >= self.cold_time:
            self.status = PlantCardStatus.NORMAL
            self.already_cold_time = 0
        self.enable = self.check_enable_(status.sun, status.mouse)
        super().update(event, status)
        return True