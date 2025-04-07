import pygame
from item import Item
from utils import resource_path
import os

class Text(Item):
    def __init__(self, pos, json_path, name, text, font_size):
        super().__init__(pos, json_path, name)
        import json
        with open(resource_path(json_path), "r", encoding='utf-8') as f:
            config = json.load(f)
            self.front_color = config["front_color"]
            self.back_color = config["back_color"]
        if pygame.font:
            self.font = pygame.font.Font(resource_path("./fonts/MSYH.TTC"), font_size)
            texts = text.split('\n')
            self.texts = [self.font.render(text, True, self.front_color, self.back_color)
                          for text in texts]
            self.height = self.font.get_height()
            self.rect = pygame.Rect(self.pos, [self.size[0], self.height / 2])
        else:
            self.font = None
            self.texts = None
    
    def set_text(self, text):
        if self.font is None:
            return
        texts = text.split('\n')
        self.texts = [self.font.render(text, True, self.front_color, self.back_color)
                          for text in texts]

    def draw(self, surface):
        if self.texts is None:
            return
        for (i, text) in enumerate(self.texts):
            surface.blit(text, self.rect.move(0, self.height * i))