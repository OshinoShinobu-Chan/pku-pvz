import pygame
from item import Item
from utils import resource_path
import os

class Text(Item):
    def __init__(self, pos, json_path, name, text, font_size, update=None, alpha=255):
        super().__init__(pos, json_path, name)
        self.update_function = update
        self.alpha = alpha
        import json
        with open(resource_path(json_path), "r", encoding='utf-8') as f:
            config = json.load(f)
            self.front_color = config["front_color"]
            self.back_color = config["back_color"] if len(config["back_color"]) == 3 else None
        if pygame.font:
            self.font = pygame.font.Font(resource_path("./fonts/MSYH.TTC"), font_size)
            texts = text.split('\n')
            self.texts = [self.font.render(text, True, self.front_color, self.back_color)
                          for text in texts]
            for text in self.texts:
                text.set_alpha(self.alpha)
            self.height = self.font.get_height()
            self.rect = pygame.Rect(self.pos, [self.size[0], self.height * len(self.texts)])
        else:
            self.font = None
            self.texts = None
    
    def set_text(self, text):
        if self.font is None:
            return
        texts = text.split('\n')
        self.texts = [self.font.render(text, True, self.front_color, self.back_color)
                          for text in texts]
        for text in self.texts:
            text.set_alpha(self.alpha)
    
    def update(self, event, status):
        if self.update_function is not None:
            return self.update_function(event, status)
        return True

    def draw(self, surface, _tick):
        if self.texts is None:
            return
        for (i, text) in enumerate(self.texts):
            surface.blit(text, self.rect.move(0, self.height * i))