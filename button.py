import pygame
from item import Item
import json
from status import GamePhase
from game import GameBackground, GameStart
from start import Start

def click_start(status):
    status.game_phase = GamePhase.GAME_START
    status.items.clear()
    status.backgrounds.clear()
    status.executors.append(GameBackground())
    status.executors.append(GameStart())

def click_end(status):
    status.running = False

def click_plant_card_wrapper(name, json_path):
    def click_plant_card(status):
        index = -1
        for i in range(8):
            if status.selected_plants[i] is None:
                index = i
                break
        if index == -1:
            return
        status.selected_plants[index] = name
        status.selected_plants_cnt += 1
        pos = [status.screen.get_width() / 2 - 160 + (index - 4) * 80 + 40, 50]
        full_name = "selected_plant_cards_" + str(index)
        on_click = click_selected_plant_card_wrapper(full_name, index)
        on_focus = focus_plant_card_wrapper(name)
        status.items[full_name] = Button(pos=pos,
                                    on_click=on_click,
                                    json_path=json_path,
                                    name=full_name,
                                    on_focus=on_focus,
                                    lose_fucus=lose_focus_card)
    return click_plant_card

def focus_plant_card_wrapper(name):
    def focus_plant_card(status):
        status.static_items["plant_description"].set_text(status.plant_card_descriptions[name])
    return focus_plant_card

def plant_card_check_enable(status, event):
    return status.selected_plants_cnt != 8

def lose_focus_card(status):
    status.static_items["plant_description"].set_text("在左侧卡片上左键选择植物，\n在上面卡片上左键取消选择")

def click_selected_plant_card_wrapper(name, index):
    def click_selected_plant_card(status):
        del status.items[name]
        status.selected_plants_cnt -= 1
        status.selected_plants[index] = None
    return click_selected_plant_card

def click_start_game(status):
    status.game_phase = GamePhase.GAME
    status.items.clear()
    status.backgrounds.clear()
    status.static_items.clear()
    status.executors.append(GameBackground())
    # status.executors.append(Game())

def click_end_game(status):
    status.game_phase = GamePhase.START
    status.items.clear()
    status.backgrounds.clear()
    status.static_items.clear()
    status.executors.append(GameBackground())
    status.executors.append(Start())
    status.selected_plants = [None for _ in range(8)]
    status.selected_plants_cnt = 0


class Button(Item):
    def __init__(self, pos, on_click, json_path, name, on_focus=None, lose_fucus=None, check_enable=None):
        super().__init__(pos, json_path, name)
        with open(json_path, "r") as f:
            config = json.load(f)
        images = {k: pygame.image.load(config["image_paths"][k]).convert() for k in config["image_paths"].keys()}
        self.images = {k: pygame.transform.smoothscale(images[k], self.size) for k in images.keys()}
        self.on_click = on_click
        self.on_focus = on_focus
        self.lose_focus = lose_fucus
        self.check_enable = check_enable
        self.focus = False
        self.focus_image = self.images["focus"]
        self.disable_image = self.images["diable"] if "diable" in self.images else self.images["normal"]
        self.normal_image = self.images["normal"]
        self.enable = True
    
    def update(self, event, status):
        # check enable
        if self.check_enable is not None:
            self.enable = self.check_enable(status, event)
        # check focus
        if not self.rect.collidepoint(status.mouse_pos):
            self.image = self.normal_image if self.enable else self.disable_image
            if self.lose_focus is not None and self.focus:
                self.lose_focus(status)
                self.focus = False
            return True
        self.image = self.focus_image if self.enable else self.disable_image
        self.focus = True
        if self.on_focus is not None:
            self.on_focus(status)
        for e in event:
            if e.type == pygame.MOUSEBUTTONUP:
                self.on_click(status)
        return True