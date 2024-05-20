
from state import State
from enemy.sandworm import Sandworm
from enemy.softbody import SoftBody, PlayerPOVCaluclator
from enemy.module.SteeringManager import Fish
import pygame as pg

from enemy.module.settings import sprites, SCREEN_RECT, seaweed, flowers, random_spots,WORM_COUNTDOWN, FISH_COUNTDOWN
from random import randint


class Seaweed(pg.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.index = 0
    self.image = seaweed[self.index].convert_alpha()
    self.rect = self.image.get_rect()


    self.rect.x = randint(0, SCREEN_RECT.width)
    self.rect.y = randint(0, SCREEN_RECT.height)

    self.seaweed_frame_change_speed = .5

  def update(self, delta):
    self.seaweed_frame_change_speed -= 1 * delta

    if self.seaweed_frame_change_speed < 0:
      self.index += 1

      self.image = seaweed[self.index % 3]
      self.seaweed_frame_change_speed = .5

class FLower(pg.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)

    randint(0, 3)
    self.image = flowers[randint(0, 3)].convert_alpha()
    self.rect = self.image.get_rect()

    self.rect.x = randint(0, SCREEN_RECT.width)
    self.rect.y = randint(0, SCREEN_RECT.height)

    self.change_timer = .10

  def update(self, delta):
    self.change_timer -= delta * 1

    if self.change_timer < 0 :
      if randint(0, 4) == 0:
        self.image = pg.transform.flip(self.image, True, False)

      self.change_timer = .10

class Spots(pg.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)

    randint(0, 3)
    self.image = random_spots[randint(0, 2)].convert_alpha()
    self.rect = self.image.get_rect()

    self.rect.x = randint(0, SCREEN_RECT.width)
    self.rect.y = randint(0, SCREEN_RECT.height)

class AirPocket(pg.sprite.Sprite):
  def __init__(self, groups):
    super().__init__(groups)
    self.image = pg.transform.scale(sprites['crack'].convert_alpha(), (32, 32))
    self.rect = self.image.get_rect()

    self.rect.x = randint(0, SCREEN_RECT.width)
    self.rect.y = randint(0, SCREEN_RECT.height)

    self.bubble_respawn_timer = .4
    self.shots = []

  def create_shot(self):
    x_offset = randint(1, 20) - 10
    y_offset = randint(1, 20) - 10
    speed = randint(6, 8)

    return {
            'surface' :  self.bubble_transform(sprites['bubble'].convert_alpha()),
            'position' : pg.Vector2(self.rect.x - x_offset,  self.rect.y - y_offset),
            'speed' : speed,
            'direction' : pg.Vector2(0, -1),
            'radius' : 7,
            'life' : 0.5
          }

  def bubble_transform(self, surface) -> pg.Surface:
    scale_amount = randint(2, 3) / 2
    return pg.transform.scale(surface, (16 * scale_amount, 16 * scale_amount))

    #handles remove and update
  def update_shot(self, dt):
    for shot in self.shots:
      shot['position'] += shot['direction'] * shot['speed']
      shot['life'] -= 1 * dt

      if shot['life'] < 0:
        try:
          self.shots.remove(shot)
        except:
          pass

  def draw_shot(self, surface: pg.Surface):
    for shot in self.shots:
      if shot:
        surface.blit(shot['surface'], shot['position'])

  def update(self, dt):
    self.update_shot(dt)


    self.bubble_respawn_timer -= 1 * dt
    if self.bubble_respawn_timer < 0:
      for _ in range(3):
        self.shots.append(self.create_shot())
      self.bubble_respawn_timer = .2


class GameState(State):
  def __init__(self, engine):
    super().__init__(engine)
    self.POV = PlayerPOVCaluclator()
    self.enemy_group_sandworms = pg.sprite.Group()
    self.enemy_group_fish = pg.sprite.Group()


    self.total_timer = 0
    self.pause = False

    # self.generate_entities()

    self.player_group = pg.sprite.Group()

    self.player = Sandworm(self.player_group)
    self.player.size = 30
    self.player.body_length = 20
    self.player.part_offset = 10


    #steering mechanic..
    self.POV.pos = pg.Vector2(self.player.rect.center)
    self.player.pos = self.POV.pos

    self.attack_rect = pg.rect.Rect(0,0, 50, 50)
    self.attack_line = None
    self.attack_points = []

    self.is_dashing = False
    self.dash_timer = 4
    self.dash_timer_current = 0
    self.seaweed_count = 100
    self.flower_count = 100
    self.spot_count = 100

    self.shots = []

    self.air_pocket : pg.sprite.Group = pg.sprite.Group()
    self.front_layer : pg.sprite.Group = pg.sprite.Group()
    self.background_layer: pg.sprite.Group = pg.sprite.Group()


    self.worm_timer = WORM_COUNTDOWN
    self.fish_timer = FISH_COUNTDOWN

    self.generate_air_pocket()
    self.generate_seaweed_flower()
    self.air_capacity = 10
    self.player_air_capacity = 10

    self.max_health = 5
    self.player_health = 5

    self.bubble_cool_down = .3

  def on_change_menu(self):
    from states.menu import MenuState
    self.engine.machine.current = MenuState(self.engine, self.total_timer)

  def generate_seaweed_flower(self):
    for _ in range(self.seaweed_count):
      Seaweed(self.front_layer)

    for _ in range(self.flower_count):
      FLower(self.background_layer)

    for _ in range(self.spot_count):
      Spots(self.background_layer)

  def bubble_transform(self, surface) -> pg.Surface:
    scale_amount = randint(2, 3) / 2
    return pg.transform.scale(surface, (16 * scale_amount, 16 * scale_amount))

  def create_shot(self):
    POV_direct = self.POV.vel.normalize()

    x_offset = randint(1, 20) - 10 - (POV_direct.x * 40)
    y_offset = randint(1, 20) - 10 - (POV_direct.y * 40)
    speed = randint(6, 8)

    return {
            'surface' :  self.bubble_transform(sprites['bubble'].convert_alpha()),
            'position' : pg.Vector2(self.player.rect.midtop[0] - x_offset, self.player.rect.midtop[1] - y_offset),
            'speed' : speed,
            'direction' : POV_direct,
            'radius' : 7,
            'life' : 0.5

          }


  def get_rect(self, obj):
    return pg.Rect(obj['position'][0],
                    obj['position'][1],
                    obj['surface'].get_width(),
                    obj['surface'].get_height())

  #handles remove and update
  def update_shot(self, dt):
    for shot in self.shots:
      shot['position'] += shot['direction'] * shot['speed']
      shot['life'] -= 1 * dt
      print(shot['life'])

      if not self.get_rect(shot).colliderect(SCREEN_RECT):
        self.shots.remove(shot)

      if shot['life'] < 0:
        try:
          self.shots.remove(shot)
        except:
          pass

  def draw_shot(self, surface: pg.Surface):
    for shot in self.shots:
      if shot:
        surface.blit(shot['surface'], shot['position'])

    for sprite in self.air_pocket:
      sprite.draw_shot(surface)

  def set_player_power(self, power):
    self.POV.power = power
    self.POV.tracking_strength = 7

  def generate_air_pocket(self):
    for _ in range(6):
      AirPocket(self.air_pocket)

  def generate_entities(self):
    for _ in range(5):
      Sandworm(self.enemy_group_sandworms)

    for _ in range(30):
      Fish(self.enemy_group_fish)

  def generate_enetities_long_term(self, delta):
    self.worm_timer -= delta * 1
    self.fish_timer -= delta * 1

    if self.worm_timer < 0:
      self.worm_timer = WORM_COUNTDOWN
      Sandworm(self.enemy_group_sandworms)



    if self.fish_timer < 0:
      self.fish_timer = FISH_COUNTDOWN
      Fish(self.enemy_group_fish)


  def update_dash(self, delta):
    self.dash_timer_current -= delta * 1

    if not self.dash_timer_current > 0:
      self.set_player_power(15)

  def on_draw(self, surface : pg.Surface):
    surface.fill(pg.Color(0,187,255))
    self.background_layer.draw(surface=surface)
    self.air_pocket.draw(surface=surface)


    self.enemy_group_sandworms.draw(surface=surface)
    self.enemy_group_fish.draw(surface=surface)
    self.attack_points.clear()

    self.draw_shot(surface=surface)

    self.player_group.draw(surface=surface)
    self.front_layer.draw(surface=surface)

  def update_air_logic(self, delta):
    self.player_air_capacity -= delta * 1

    if self.player_air_capacity < 0:
      self.player_health -= delta * 1

    if pg.sprite.groupcollide(self.player_group, self.air_pocket, dokilla=False, dokillb=False):
      if self.player_air_capacity < self.air_capacity:
        self.player_air_capacity += delta * 3

  def check_win_condition(self):
    if self.player_health < 0:
      print("LOSSSSS", self.total_timer)
      self.pause = True
      self.on_change_menu()

  def on_update(self, delta):
    if not self.pause:

      self.generate_enetities_long_term(delta=delta)

      self.total_timer += 1 * delta

      self.check_win_condition()

      self.background_layer.update(delta)

      self.front_layer.update(delta)

      self.bubble_cool_down -= 1 * delta

      self.update_air_logic(delta)

      self.update_air_logic(delta=delta)

      self.update_shot(delta)

      self.update_dash(delta)

      self.air_pocket.update(delta)
      self.enemy_group_sandworms.update(delta)
      self.enemy_group_fish.update(delta)

      self.player_group.update(delta)
      self.POV.update(delta)

    return super().on_update(delta)

  def on_event(self, event):

    keys = pg.key.get_pressed()
    if keys[pg.K_z]:
      if self.bubble_cool_down < 0:
        for _ in range(2):
          self.shots.append(self.create_shot())
          self.bubble_cool_down = 0.05

    if event.type == pg.KEYUP:
       if event.key == pg.K_SPACE:
         self.set_player_power(20)
         self.dash_timer_current = self.dash_timer
