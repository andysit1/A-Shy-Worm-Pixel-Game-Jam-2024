
from softbody import SoftBody
from enemyAI import EntityMovementAI
import pygame as pg

frect = pg.FRect
vec2 = pg.Vector2

#class to hold data pretty much
class SandwormBody(pg.sprite.Sprite):
    def __init__(self, groups):
      super().__init__(groups)
      self.image = pg.Surface([25, 25])
      self.image.fill("white")
      self.rect = self.image.get_rect()

    def set_pos(self, pos):
       self.rect.center = pos

class Sandworm(pg.sprite.Sprite, SoftBody):
  def __init__(self, groups):
    super().__init__(groups)


    self.image = pg.Surface([50, 50])
    self.body_part_group : list[SandwormBody] = []
    self.rect = self.image.get_rect()

    self.body_length : int = 8
    self.part_offset : int = 20
    self.body_parts : list[vec2] = []
    self.pos = None

    self.head_rect : pg.rect = pg.Rect(400, 400, 40, 100)



    self.entity_ai = EntityMovementAI()
    self.pos = self.entity_ai.pos
    self.entity_ai.head = self.rect

    self.init_body_parts(groups)

  def init_body_parts(self, grp):
    for _ in range(self.body_length):
       self.body_part_group.append(SandwormBody(grp))

  def update_body_sprite(self):
    index = 0
    for part in self.body_parts:
      if index != 0:
        self.body_part_group[index - 1].set_pos(part)
      index += 1

  def update(self):
    self.entity_ai.update()

    if self.pos:
      self.add_body(part=self.pos.copy())
      self.rect.center = self.body_parts[0]

    self.update_body_sprite()

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