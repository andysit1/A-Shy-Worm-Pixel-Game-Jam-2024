# Example file showing a basic pygame "game loop"
import pygame
from random import randint, uniform
from .module.settings import WIDTH, HEIGHT, SCREEN_RECT
from .module.SteeringManager import Fish

# pygame setup
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
running = True

MAX_FORCE = 10
vec = pygame.math.Vector2
frect = pygame.rect.FRect
# Mob properties
MOB_SIZE = 32
MAX_SPEED = 4
MAX_FORCE = 0.4
RAND_TARGET_TIME = 500
WANDER_RING_DISTANCE = 150
WANDER_RING_RADIUS = 50
WANDER_TYPE = 2




#class to handle the angle/positioning of the head for mouse point of few
class PlayerPOVCaluclator():
    def __init__(self):
        self.vel = vec(0, 0)
        self.acc = vec(0, 0)

        #set this to the rect hand in softbody...
        #or the relate positioning we want
        self.pos : vec = None

        self.power = 15
        self.tracking_strength = 7


    def seek(self, target : vec):
        dest = (self.pos - target).normalize()

        #fixed the jitters
        change_to_dest = self.vel - dest * self.tracking_strength

        if change_to_dest.length() > self.power:
            change_to_dest.scale_to_length(self.power)

        return change_to_dest

    def update(self, delta):
        #adjust the velocity by the acting forces

        self.acc = self.seek(pygame.mouse.get_pos())
        self.vel += self.acc

        if self.vel.length() > self.power:
            self.vel.scale_to_length(self.power * delta)
        print(self.power * delta, delta, self.power)
        self.pos += self.vel



class EntityMovementAI():
    def __init__(self):
        self.pos = vec(100, 100)
        self.vel = vec(MAX_SPEED, 0).rotate(uniform(0, 360))
        self.acc = vec(0, 0)
        self.head : frect = None
        self.collision_zone : frect = SCREEN_RECT

    def seek(self, target):
        self.desired = (target - self.pos).normalize() * MAX_SPEED
        steer = (self.desired - self.vel)
        if steer.length() > MAX_FORCE:
            steer.scale_to_length(MAX_FORCE)
        return steer

    def wander_improved(self):
        future = self.pos + self.vel.normalize() * WANDER_RING_DISTANCE
        #add a bias to make the AI go towards the center
        target = future + vec(WANDER_RING_RADIUS, 0).rotate(uniform(0, 360))
        self.displacement = target
        return self.seek(target)

    def update(self):
        if WANDER_TYPE == 1:
            self.acc = self.wander()
        else:
            if not self.head.colliderect(self.collision_zone):
                self.acc = self.seek(vec(self.collision_zone.center[0], self.collision_zone.center[1])) #redirects to the center point
            else:
                self.acc = self.wander_improved()


        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED)
        self.pos += self.vel


#Softbody: These are made up of dots.
class SoftBody():
    def __init__(self):
        self.body_length : int = 8
        self.part_offset : int = 20
        self.body_parts : list[pygame.Vector2] = []
        self.head : frect = frect(0, 0, 25, 25)
        self.pos = None
        self.size = 13

        self.attack_line_length = 50

    def add_body(self, part : pygame.Vector2) -> bool:
        if len(self.body_parts) == 0:
            self.body_parts.append(part)
            return True
        else:
            if not self.add_conditions_ai(part):
                return False

            if len(self.body_parts) > self.body_length:
                self.body_parts.pop()
                self.body_parts.insert(0, part)
            else:
                self.body_parts.insert(0, part)
            return True

    @property
    def body_part_length(self):
        return len(self.body_parts)

    def to_vector_2d(self, pos):
        if isinstance(pos, vec):
            return pos

        return pygame.Vector2(pos[0], pos[1])

    def add_conditions(self) -> bool:
        if self.body_part_length > 0:
          if (self.body_parts[0] -  self.to_vector_2d(pygame.mouse.get_pos())).magnitude() > self.part_offset:
              return True

    def add_conditions_ai(self, location) -> bool:
        if self.body_part_length > 0:


            if (self.body_parts[0] - self.to_vector_2d(location)).magnitude() > self.part_offset:
                return True

    def update(self):
        if not self.pos:
            self.add_body(part=pygame.mouse.get_pos())
            self.head.center = self.body_parts[0]

        if self.pos:
            self.add_body(part=self.pos.copy())

        self.head.center = self.body_parts[0]


    def draw(self, surface):
        size = self.size
        prev = None
        for part in self.body_parts:
            size -= 1.2
            if prev:
                pygame.draw.line(surface, "black", prev, part, 1)
            pygame.draw.circle(surface, "white", part, radius=size)
            prev = part

        if not self.pos:
            pygame.draw.circle(surface, "black", self.head.center, 30)
        pygame.draw.rect(surface, "blue", self.head)

class Player(SoftBody):
    def __init__(self):
        super().__init__()

        self.size = 40
        self.body_length = 20
        self.part_offset = 6



if __name__ == "__main__":
  attack_grp = pygame.sprite.Group()
  all_sprites = pygame.sprite.Group()

  for i in range(100):
      Fish(all_sprites)


  POV = PlayerPOVCaluclator()
  entity1 = SoftBody()
  entity1.size = 40
  entity1.body_length = 20
  entity1.part_offset = 6


  POV.pos = vec(entity1.head.center)
  entity1.pos = POV.pos



  entity2 = SoftBody()
  AI1 = EntityMovementAI()


  AI1.head = entity2.head

  entity2.pos = AI1.pos

  entities = []
  ai = []

  for i in range(5):
      bodyobj = SoftBody()
      aiobj = EntityMovementAI()


      aiobj.head = bodyobj.head
      bodyobj.pos = aiobj.pos

      entities.append(bodyobj)
      ai.append(aiobj)


  def update_ai():
      for i in ai:
          i.update()

      for i in entities:
          i.update()

  def draw_entities(surf):
      for i in entities:
          i.draw(surf)



  old_mouse_pos = None
  new_mouse_pos : vec = pygame.mouse.get_pos()
  attack_rect = pygame.rect.Rect(0, 0, 40, 40)

  while running:
      new_mouse_pos = pygame.mouse.get_pos()
      # poll for events
      # pygame.QUIT event means the user clicked X to close your window

      for event in pygame.event.get():
          if event.type == pygame.QUIT:
              running = False



      update_ai()
      POV.update()
      all_sprites.update()
      entity1.update()

      screen.fill(pygame.Color(119, 176, 170))

      #player controled
      entity1.draw(screen)




    #   if attacking:
        #   pygame.draw.rect(screen, "black", )

      #AI controlled
      draw_entities(screen)


      #draw the attack range of
      try:

        # direction = vec(old_mouse_pos[0] - new_mouse_pos[0], old_mouse_pos[1] - new_mouse_pos[1]).normalize() * 100
        # pygame.draw.line(screen, "red", entity1.head.center, new_mouse_pos - direction, 2)

        pygame.draw.line(screen, "red", entity1.head.center, entity1.head.center + POV.acc * 40)
        pygame.draw.line(screen, "green", entity1.head.center, entity1.head.center + POV.vel * 40)


        for sprite in all_sprites:
            sprite.steering.draw_vectors(screen)

        attack_line : vec = entity1.head.center + POV.vel * 40


        #collisions
        c = 0
        c_offset = 1 / 20
        for i in range(20):
            c += c_offset
            point = vec(entity1.head.center).lerp(attack_line, c)
            attack_rect.center = point
            pygame.draw.rect(screen, "purple", attack_rect)
      except:
          pass

      all_sprites.draw(screen)

      pygame.display.flip()
      clock.tick(60)
      old_mouse_pos = new_mouse_pos

  pygame.quit()