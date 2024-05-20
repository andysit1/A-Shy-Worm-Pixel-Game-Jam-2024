from.module.settings import sprites
from .softbody import SoftBody
from .enemyAI import EntityMovementAI
import pygame as pg

frect = pg.FRect
vec2 = pg.Vector2

class SandwormBody(pg.sprite.Sprite):
    def __init__(self, groups):
      super().__init__(groups)
      self.image = pg.transform.scale(sprites['worm_scale'], (50, 50))
      self.rect = self.image.get_rect()

    def set_pos(self, pos):
       self.rect.center = pos

class Sandworm(pg.sprite.Sprite, SoftBody):
  def __init__(self, groups):
    super().__init__(groups)

    self.image = pg.transform.scale(sprites['worm_head'], (50, 50))
    self.body_part_group : list[SandwormBody] = []
    self.rect = self.image.get_rect()

    self.body_length : int = 8
    self.part_offset : int = 20
    self.body_parts : list[vec2] = []
    self.pos = None

    self.entity_ai = EntityMovementAI()
    self.pos = self.entity_ai.pos
    self.entity_ai.head = self.rect

    self.init_body_parts(groups)

  def subtract_values(self, x, y) -> int:
    re = x - y
    return re

  def rotate(self):
    # pass
    x = self.subtract_values(self.body_part_group[0].rect.x * 1, self.body_part_group[1].rect.x * 1)
    y = self.subtract_values(self.body_part_group[0].rect.y * 1, self.body_part_group[1].rect.y * 1)

    d = vec2(x, y)
    _, angle = d.as_polar()

    self.image = pg.transform.rotozoom(sprites['worm_head'], -angle, 1)
    self.rect = self.image.get_rect(center=self.rect.center)
    self.entity_ai.head = self.rect


  def init_body_parts(self, grp):
    for _ in range(self.body_length):
       self.body_part_group.append(SandwormBody(grp))

  def update_body_sprite(self):
    index = 0
    for part in self.body_parts:
      if index != 0 and index - 1 < len(self.body_part_group):
        self.body_part_group[index - 1].set_pos(part)
      index += 1

  def update(self, delta):
    self.entity_ai.update(delta)

    if self.pos:
      if self.add_body(part=self.pos.copy()):
        self.update_body_sprite()
        self.rect.center = self.body_parts[0]
        self.rotate()




running = True

if __name__ == "__main__":
  grp = pg.sprite.Group()
  screen = pg.display.set_mode((1280, 720))
  clock = pg.time.Clock()
  Sandworm(grp)
  Sandworm(grp)
  Sandworm(grp)
  Sandworm(grp)
  Sandworm(grp)


  while running:
      # poll for events
      # pygame.QUIT event means the user clicked X to close your window
      for event in pg.event.get():
          if event.type == pg.QUIT:
              running = False


      grp.update()
      screen.fill("purple")
      grp.draw(screen)


      pg.display.flip()
      clock.tick(60)

  pg.quit()