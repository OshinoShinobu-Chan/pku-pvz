import pygame
from static import Static
from text import Text
import json
from status import GamePhase
from random import randint
from utils import resource_path

class GameBackground:
    def excute(self, status, event):
        match status.game_phase:
            case GamePhase.START:
                status.backgrounds.append(Static(pos=[status.screen.get_width() / 2,
                                        status.screen.get_height() / 2, 3],
                    json_path=resource_path("./configs/statics/start_background.json"),
                    name="start-background"))
            case GamePhase.GAME_START:
                status.backgrounds.append(Static(pos=[status.screen.get_width() / 2,
                                                status.screen.get_height() / 2, 3],
                    json_path=resource_path("./configs/statics/start_game_background.json"),
                    name="start-game-background"))
            case GamePhase.GAME:
                status.backgrounds.append(Static(pos=[status.screen.get_width() / 2,
                                                status.screen.get_height() / 2, 3],
                    json_path=resource_path("./configs/statics/game_background.json"),
                    name="game-background"))
        return False

class GameStart:
    def excute(self, status, event):
        from button import Button, click_plant_card_wrapper, \
                        focus_plant_card_wrapper, lose_focus_card, \
                        plant_card_check_enable, click_start_game, \
                        click_end_game, no_action, focus_showing_zombie_wrapper, \
                        check_start_game_enble
        # description text
        status.static_items["plant_description"] = Text(pos=[status.screen.get_width() / 4,
                                                             status.screen.get_height() * 2 / 5],
                            json_path=resource_path("./configs/texts/plant-description.json"),
                            name="plant-description",
                            text="在左侧卡片上左键选择植物，\n在上面卡片上左键取消选择",
                            font_size=24)
        # plant cards
        with open(resource_path("./configs/plant_cards/plant_cards.json"), "r", encoding='utf-8') as f:
            plant_cards = json.load(f)
        for (i, (key, plant_card)) in enumerate(plant_cards.items()):
            index = [i // 6, i % 6]
            pos = [status.screen.get_width() / 6 + ((index[1] - 2) * 2 + 1) * 40,
                   status.screen.get_height() * 2 / 5 + (index[0] * 2 + 1) * 60]
            status.items[plant_card["name"] + "_card"] = (Button(pos=pos, 
                                       on_click=click_plant_card_wrapper(plant_card["name"], plant_card["json_path"]),
                                       json_path=resource_path(plant_card["json_path"]),
                                       name=plant_card["name"] + "_card",
                                       on_focus=focus_plant_card_wrapper(key),
                                       lose_fucus=lose_focus_card,
                                       check_enable=plant_card_check_enable))
        # zombies
        with open(resource_path("./configs/zombies/zombies.json"), "r", encoding='utf-8') as f:
            zombies = json.load(f)
        for zombie in zombies.values():
            for i in range(3):
                index = [randint(0, 2), randint(0, 3)]
                pos = [status.screen.get_width() * 2 / 3 + (index[0] * 2 + 1) * 15,
                       100 + (index[1] * 2 + 1) * 60]
                status.items[zombie["name"] + "_" + str(i)] = Button(pos=pos,
                                                    on_click=no_action,
                                                    json_path=resource_path(zombie["json_path"]),
                                                    name=zombie["name"],
                                                    on_focus=focus_showing_zombie_wrapper(zombie["name"]),
                                                    lose_fucus=lose_focus_card)
        # start button
        status.items["start-button"] = Button(pos=[status.screen.get_width() / 4, 
                                        status.screen.get_height() - 60, 1],
                    json_path=resource_path("./configs/buttons/start_button.json"),
                    on_click=click_start_game,
                    name="start-button",
                    check_enable=check_start_game_enble)
        # end button
        status.items["end-button"] = Button(pos=[status.screen.get_width() * 3 / 4, 
                                        status.screen.get_height() - 60, 1],
                    json_path=resource_path("./configs/buttons/end_button.json"),
                    on_click=click_end_game,
                    name="end-button")
        return False

class GameCountDown:
    
    def __init__(self, tick):
        self.start_tick = tick
        self.status = 4
    
    def excute(self, status, event):
        from merge import Merge 
        if self.status == 4 and status.global_ticks >= self.start_tick:
            status.items["count_down_3"] = Merge(pos=[status.screen.get_width() / 2, 
                                                     status.screen.get_height() / 2],
                                                json_path=resource_path("./configs/texts/number3.json"),
                                                name="count_down_3",
                                                start_tick=status.global_ticks,
                                                duration_ms=1000)
            self.status = 3
        elif self.status == 3 and status.global_ticks >= self.start_tick + 60:
            status.items["count_down_2"] = Merge(pos=[status.screen.get_width() / 2, 
                                                     status.screen.get_height() / 2],
                                                json_path=resource_path("./configs/texts/number2.json"),
                                                name="count_down_2",
                                                start_tick=status.global_ticks,
                                                duration_ms=1000)
            self.status = 2
        elif self.status == 2 and status.global_ticks >= self.start_tick + 120:
            status.items["count_down_1"] = Merge(pos=[status.screen.get_width() / 2, 
                                                     status.screen.get_height() / 2],
                                                json_path=resource_path("./configs/texts/number1.json"),
                                                name="count_down_1",
                                                start_tick=status.global_ticks,
                                                duration_ms=1000)
            self.status = 1
        elif self.status == 1 and status.global_ticks >= self.start_tick + 180:
            status.items["count_down_start"] = Merge(pos=[status.screen.get_width() / 2, 
                                                     status.screen.get_height() / 2],
                                                json_path=resource_path("./configs/texts/start.json"),
                                                name="count_down_start",
                                                start_tick=status.global_ticks,
                                                duration_ms=1000)
            self.status = 0
            return False
        return True

class Game:
    def __init__(self, tick):
        self.start_tick = tick
        self.initialized = False

    def excute(self, status, event):
        # first start
        if not self.initialized:
            # selected plant cards
            for (i, plant) in enumerate(status.selected_plants):
                if plant is None:
                    continue
                pos = [status.screen.get_width() / 2  - 160 + (i - 4) * 80 + 40, 50]

