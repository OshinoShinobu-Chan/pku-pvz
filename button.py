import pygame
from item import Item
import json
from status import GamePhase
from game import GameBackground, GameStart, GameCountDown
from start import Start
from plant import Plant
from utils import resource_path

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
    status.executors.append(GameCountDown(status.global_ticks))

def click_end_game(status):
    status.game_phase = GamePhase.START
    status.items.clear()
    status.backgrounds.clear()
    status.static_items.clear()
    status.executors.append(GameBackground())
    status.executors.append(Start())
    status.selected_plants = [None for _ in range(8)]
    status.selected_plants_cnt = 0

def no_action(status):
    pass

def focus_showing_zombie_wrapper(name):
    def focus_showing_zombie(status):
        status.static_items["plant_description"].set_text(status.zombie_descriptions[name])
    return focus_showing_zombie

def check_start_game_enble(status, event):
    return status.selected_plants_cnt != 0

def click_plant_card_slot_wrapper(index, init_pos):
    def click_plant_card_clot(status, event):
        plant_name = status.selected_plants[index]
        # status.items[plant_name + str(status.plant_id)] = Plant(
        #     pos=init_pos,
            
        # )


class Button(Item):
    def __init__(self, pos, on_click, json_path, name, on_focus=None, lose_fucus=None, check_enable=None):
        super().__init__(pos, json_path, name)
        with open(resource_path(json_path), "r") as f:
            config = json.load(f)
        images = {k: pygame.image.load(resource_path(config["image_paths"][k])).convert() for k in config["image_paths"].keys()}
        self.images = {k: pygame.transform.smoothscale(images[k], self.size) for k in images.keys()}
        self.on_click = on_click
        self.on_focus = on_focus
        self.lose_focus = lose_fucus
        self.check_enable = check_enable
        self.focus = False
        self.focus_image = self.images["focus"] if "focus" in self.images else self.images["normal"]
        self.disable_image = self.images["diable"] if "diable" in self.images else self.images["normal"]
        self.normal_image = self.images["normal"]
        self.enable = True
    
    def update(self, event, status):
        # check enable
        if self.check_enable is not None:
            self.enable = self.check_enable(status, event)
        if not status.mouse_available:
            return True
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
            if self.enable and e.type == pygame.MOUSEBUTTONUP and e.button == 1:
                self.on_click(status)
                break
        return True