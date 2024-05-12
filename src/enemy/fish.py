from enemyAI import EntityMovementAI
from softbody import SoftBody
import pygame as pg

frect = pg.FRect
vec2 = pg.Vector2

class BoidEntityMovementAI(EntityMovementAI):
  def __init__(self):
      super().__init__()
      self.behaviours = { 'max_force': 0.2,
                          'max_speed': 5,
                          'seek_radius': 300,
                          'flee_radius': 400,
                          'wall_limit': 80,
                          'wander_ring_radius': 50,
                          'wander_ring_distance': 150,
                          'neighbor_radius': 50,
                          'sep_weight': 1.5,
                          'ali_weight': 0.8,
                          'coh_weight': 1
                          }

  def average_group(self, group):
      # find averages for group members
      count = 0
      avg_pos = vec2(0, 0)
      avg_dist = vec2(0, 0)
      avg_vel = vec2(0, 0)
      for obj in group:
          if obj != self:
              d = self.pos.distance_to(obj.pos)
              if d < self.behaviors['neighbor_radius']:
                  avg_pos += obj.pos
                  avg_vel += obj.vel
                  avg_dist += (self.pos - obj.pos).normalize() / d
                  count += 1
      if count > 0:
          avg_pos /= count
          avg_vel /= count
          avg_dist /= count
      return count, avg_pos, avg_dist, avg_vel

  def separation(self, avg_dist):
      # desire to move away from nearby mobs
      desired = avg_dist.normalize() * self.behaviors['max_speed']
      steer = desired - self.host.vel
      if steer.length() > self.behaviors['max_force']:
          steer.scale_to_length(self.behaviors['max_force'])
      return steer

  def alignment(self, avg_vel):
      # desire to move in dir of nearby mobs
      desired = avg_vel.normalize() * self.behaviors['max_speed']
      steer = desired - self.host.vel
      if steer.length() > self.behaviors['max_force']:
          steer.scale_to_length(self.behaviors['max_force'])

      return steer

  def cohesion(self, avg_pos):
      # desire to move to center of nearby mobs
      desired = (avg_pos - self.host.pos).normalize() * self.behaviors['max_speed']
      steer = desired - self.host.vel
      if steer.length() > self.behaviors['max_force']:
          steer.scale_to_length(self.behaviors['max_force'])
      return steer

  def flock(self, group):
      # get averages for group members w/in range
      count, avg_pos, avg_dist, avg_vel = self.get_averages(group)
      if count > 0:
          sep = self.separation(avg_dist) * self.behaviors['sep_weight']
          ali = self.alignment(avg_vel) * self.behaviors['ali_weight']
          coh = self.cohesion(avg_pos) * self.behaviors['coh_weight']
          self.steering += sep + ali + coh

class Fish(pg.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.image = pg.Surface([5, 5])
    self.rect = self.image.get_rect()

    self.entity_ai = EntityMovementAI()
    self.pos = self.entity_ai.pos
    self.entity_ai.head = self.rect


  def update(self):
    self.entity_ai.update()

    if self.pos:
      self.rect.center = self.pos



if __name__ == "__main__":
   fish_ai = BoidEntityMovementAI()





#   running = True
#   grp = pg.sprite.Group()
#   screen = pg.display.set_mode((1280, 720))
#   clock = pg.time.Clock()


#   fish = Fish(grp)

#   while running:
#       # poll for events
#       # pygame.QUIT event means the user clicked X to close your window
#       for event in pg.event.get():
#           if event.type == pg.QUIT:
#               running = False


#       grp.update()
#       screen.fill("purple")
#       grp.draw(screen)


#       pg.display.flip()
#       clock.tick(60)

#   pg.quit()