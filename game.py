import pygame
from static import Static
from text import Text
import json
from status import GamePhase

class GameBackground:
    def excute(self, status, event):
        match status.game_phase:
            case GamePhase.START:
                status.backgrounds.append(Static(pos=[status.screen.get_width() / 2,
                                        status.screen.get_height() / 2, 3],
                    json_path="./configs/statics/start_background.json",
                    name="start-background"))
            case GamePhase.GAME_START:
                status.backgrounds.append(Static(pos=[status.screen.get_width() / 2,
                                                status.screen.get_height() / 2, 3],
                                    json_path="./configs/statics/game_background.json",
                                    name="game-background"))
        return False

class GameStart:
    def excute(self, status, event):
        from button import Button, click_plant_card_wrapper
        from button import focus_plant_card_wrapper, lose_focus_card
        from button import plant_card_check_enable
        from button import click_start_game, click_end_game
        # description text
        status.static_items["plant_description"] = Text(pos=[status.screen.get_width() / 4,
                                                             status.screen.get_height() / 2],
                                                    json_path="./configs/texts/plant-description.json",
                                                    name="plant-description",
                                                    text="在左侧卡片上左键选择植物，\n在上面卡片上左键取消选择",
                                                    font_size=24)
        # plant cards
        with open("./configs/plant_cards/plant_cards.json", "r", encoding='utf-8') as f:
            plant_cards = json.load(f)
        for (i, plant_card) in enumerate(plant_cards.values()):
            index = [i // 4, i % 4]
            pos = [status.screen.get_width() / 4 + ((index[1] - 2) * 2 + 1) * 40,
                   status.screen.get_height() / 2 + (index[0] * 2 + 1) * 40]
            status.items[plant_card["name"] + "_card"] = (Button(pos=pos, 
                                       on_click=click_plant_card_wrapper(plant_card["name"], plant_card["json_path"]),
                                       json_path=plant_card["json_path"],
                                       name=plant_card["name"] + "_card",
                                       on_focus=focus_plant_card_wrapper(plant_card["name"]),
                                       lose_fucus=lose_focus_card,
                                       check_enable=plant_card_check_enable))
        # start button
        status.items["start-button"] = Button(pos=[status.screen.get_width() / 2, 
                                        status.screen.get_height() / 2 - 60, 1],
                    json_path="./configs/buttons/start_button.json",
                    on_click=click_start_game,
                    name="start-button")
        # end button
        status.items["end-button"] = Button(pos=[status.screen.get_width() / 2, 
                                        status.screen.get_height() / 2 + 60, 1],
                    json_path="./configs/buttons/end_button.json",
                    on_click=click_end_game,
                    name="end-button")
        return False