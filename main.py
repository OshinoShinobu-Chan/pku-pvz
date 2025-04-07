# Example file showing a circle moving on screen
import pygame
from copy import deepcopy

from item import Item
from button import Button, click_start
from status import Status
from start import Start
from game import GameBackground

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
status = Status(screen=screen, clock=clock)
status.executors.append(Start())
status.executors.append(GameBackground())

while status.running:
   
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            status.running = False
    status.mouse_pos = pygame.mouse.get_pos()
    screen.fill((0, 0, 0))

    if status.pause:
        for item in status.pause_items:
            item.update(status, event)
            item.draw(screen)

        for item in status.static_items.values():
            item.draw(screen)

        for item in status.backgrounds:
            item.draw(screen)
        
        for item in status.items.values():
            item.draw(screen)
        
        # flip() the display to put your work on screen
        pygame.display.update()

        # limits FPS to 60
        real_time = clock.tick(60)
        if status.global_ticks % 10 == 0:
            status.tps = 1000 / real_time

        # update the event
        pygame.event.pump()
        continue

    for b in status.backgrounds:
        b.draw(screen)

    remove_items = []
    remove_executors = []

    # run executors
    for (i, excutor) in enumerate(status.executors):
        if not excutor.excute(status, event):
            remove_executors.append(i)

    # update all items
    items = []
    for item in status.items.keys():
        items.append(deepcopy(item))
    for item in items:
        if item in status.items:
            if not status.items[item].update(events, status):
                remove_items.append(item)
    
    # draw all static items
    for item in status.static_items.values():
        item.draw(screen)

    # draw all items
    for item in status.items.values():
        item.draw(screen)

    # remove items
    for item in remove_items:
        del status.items[item]
    
    # remove executors
    new_executors = [excutor for (i, excutor) in enumerate(status.executors)
                        if i not in set(remove_executors)]
    status.executors = new_executors

    # flip() the display to put your work on screen
    pygame.display.flip()

    # limits FPS to 60
    real_time = clock.tick(60)
    status.global_ticks += 1
    if status.global_ticks % 10 == 0:
        status.tps = 1000 / real_time

    # update the event
    pygame.event.pump()
pygame.quit()