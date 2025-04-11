from enum import Enum, auto
from utils import resource_path
import pygame

class GamePhase(Enum):
    START = auto()
    GAME_START = auto()
    GAME = auto()
    GAME_OVER = auto()
    END = auto()

PLANT_AREA = pygame.Rect(250, 120, 900, 600)

class Status:
    def __init__(self, screen, clock):
        self.game_phase = GamePhase.START
        self.running = True
        self.items = {}
        self.static_items = {}
        self.backgrounds = []
        self.executors = []
        self.pause_items = []
        self.screen = screen
        self.clock = clock
        self.selected_plants = [None for _ in range(8)]
        self.selected_plants_cnt = 0
        self.global_ticks = 0
        self.tps = 1000 / 60
        self.pause = False
        self.mouse_available = True
        self.mouse = None
        self.plant_id = 0
        self.sun = 0
        self.planted_plant = [[None for _ in range(5)] for _ in range(6)]
        self.planted_plant_cnt = 0
        import json
        with open(resource_path("./configs/plant_cards/plant_cards.json"), "r", encoding="utf8") as f:
            des = json.load(f)
            self.plant_card_descriptions = {k: des[k]["description"] for k in des.keys()}
            self.plant_json_paths = {des[k]["name"]: des[k]["json_path"] for k in des.keys()}
        with open(resource_path("./configs/zombies/zombies.json"), "r", encoding='utf-8') as f:
            des = json.load(f)
            self.zombie_descriptions = {k: des[k]["description"] for k in des.keys()}