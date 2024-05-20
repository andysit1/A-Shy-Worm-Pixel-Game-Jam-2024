from enemy.module.settings import WIDTH, HEIGHT
from states.game import GameState


import pygame
import os
import sys
# Setup the environment by appending the current directory to the system path.
current_dir = os.path.dirname(__file__)
sys.path.append(current_dir)

import asyncio
import time


class State():

    def __init__(self, engine):
        self.engine = engine

    def on_draw(self, surface):
        pass

    def on_event(self, event):
        pass

    def on_update(self, delta):
        ""
        pass

    def handle_movement(self):
        pass

class Machine:
    """
    Manages transitions between different game states.
    """
    def __init__(self):
        """
        Initialize a Machine object.
        """
        self.current = None
        self.next_state = None

    def update(self):
        """
        Update the current state.
        """
        if self.next_state:
            self.current = self.next_state
            self.next_state = None


class DisplayEngine:
    """
    Manages the main game loop and display functionality.
    """
    def __init__(self, caption, fps, width, height, flags=0):

        pygame.display.set_caption(caption)
        self.surface = pygame.display.set_mode((width, height), flags)
        self.rect = self.surface.get_rect()
        self.clock = pygame.time.Clock()
        self.running = True
        self.delta = 0
        self.fps = fps
        self.machine = Machine()

    def run(self, state):
        self.machine.current = state
        self.loop()

async def main():
    running = True
    pygame.init()

    engine = DisplayEngine('A Shy Worm', 60, WIDTH, HEIGHT)
    engine.machine.current = GameState(engine)

    previous_time = time.time()
    while running:

        dt = time.time() - previous_time
        previous_time = time.time()

        engine.machine.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                engine.machine.current.on_event(event)

        engine.machine.current.on_update(dt)
        engine.machine.current.on_draw(engine.surface)

        pygame.display.flip()
        await asyncio.sleep(0)



asyncio.run(main())




