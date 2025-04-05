import pygame
import json

class Item:
    '''
    # Item
    items in game
    ## attribute
    1. pos: (x: float, y: float, z: int)
    2. size: (width: float, height: float)
    3. image_path: str, image show on this item.
    4. on_click: function called when the item is clicked
    '''
    def __init__(self, pos, json_path, name):
        with open(json_path, "r") as f:
            config = json.load(f)
        
        self.size = pygame.Vector2(config["size"][0], config["size"][1])
        self.pos = pygame.Vector2(pos[0] - self.size.x / 2, pos[1] - self.size.y / 2)
        self.rect = pygame.Rect(self.pos, self.size)
        self.name = name
        self.image = pygame.transform.smoothscale(pygame.image.load(config["image_paths"]["normal"]).convert(), self.size)

    def update(self, event, status):
        '''
        Implemented by derived class
        '''
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)