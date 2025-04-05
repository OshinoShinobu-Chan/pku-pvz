from enum import Enum, auto
class GamePhase(Enum):
    START = auto()
    GAME_START = auto()
    GAME = auto()
    GAME_OVER = auto()
    END = auto()

class Status:
    def __init__(self, screen, clock):
        self.game_phase = GamePhase.START
        self.running = True
        self.items = {}
        self.static_items = {}
        self.backgrounds = []
        self.executors = []
        self.screen = screen
        self.clock = clock
        self.selected_plants = [None for _ in range(8)]
        self.selected_plants_cnt = 0
        with open("./configs/plant_cards/plant_cards.json", "r", encoding="utf8") as f:
            import json
            des = json.load(f)
            self.plant_card_descriptions = {k: des[k]["description"] for k in des.keys()}