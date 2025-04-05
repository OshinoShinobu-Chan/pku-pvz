import pygame
from item import Item

class Static(Item):
    def __init__(self, pos, json_path, name):
        super().__init__(pos, json_path, name)
    def update(self, event, status):
        return True