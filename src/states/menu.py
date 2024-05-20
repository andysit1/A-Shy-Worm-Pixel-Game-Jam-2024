
import pygame as pg
from state import State


class MenuState(State):
  def __init__(self, engine, time):
    super().__init__(engine)
    self.engine = engine
    self.timer_text = time
    self.font = pg.font.SysFont('Comic Sans MS', 30)
    self.text_surface = self.font.render("Total Time {}".format(str(self.timer_text)), False, (0, 0, 0))

  def on_change_game_state(self):
    from states.game import GameState
    self.engine.machine.current = GameState(self.engine)

  def on_draw(self, surface : pg.Surface):
    surface.fill("white")
    surface.blit(self.text_surface, (0, 0))

  def on_update(self, delta):
    pass

  def on_event(self, event):
    pass