

import pygame as pg
#CONSTANT
WIDTH, HEIGHT = 800, 800
SCREEN_RECT = pg.Rect(0, 0, WIDTH, HEIGHT)
FISH_BEHAVIORS = {'max_force': 0.2,
                 'max_speed': 5,
                 'seek_radius': 300,
                 'flee_radius': 400,
                 'wall_limit': 80,
                 'wander_ring_radius': 50,
                 'wander_ring_distance': 150,
                 'neighbor_radius': 50,
                 'sep_weight': 1.5,
                 'ali_weight': 0.8,
                 'coh_weight': 1}

WORM_COUNTDOWN = 10
FISH_COUNTDOWN = 2


import os
BASE = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

bubble_path = os.path.join(BASE, "assets", "bubble.png")
worm_scale = os.path.join(BASE, "assets", "worm_scale.png")
bomb_fish_path = os.path.join(BASE, "assets", "bomb_fish.png")

spot1 = os.path.join(BASE, "assets", "random_spot_1.png")
spot2 = os.path.join(BASE, "assets", "random_spot_2.png")
spot3 = os.path.join(BASE, "assets", "random_spot_3.png")
crack = os.path.join(BASE, "assets", "crack1.png")
worm_head = os.path.join(BASE, "assets", "worm_head.png")

player_body = os.path.join(BASE, "assets", "player_body.png")
overlay_path = os.path.join(BASE, "assets", "overlay.png")

generation = [spot1, spot2, spot3]

sprites = {
  'bubble' : pg.image.load(os.path.normpath(bubble_path)),
  'worm_scale' : pg.image.load(os.path.normpath(worm_scale)),
  'bomb_fish' : pg.image.load(os.path.normpath(bomb_fish_path)),
  'crack' : pg.image.load(os.path.normpath(crack)),
  'worm_head' : pg.transform.scale(pg.image.load(os.path.normpath(worm_head)), (50, 50)),
  'player_body' : pg.image.load(os.path.normpath(player_body)),
  'overlay' : pg.image.load(os.path.normpath(overlay_path))
}


seaweed = []
for i in range(3):
    seaweed_frame_path =  os.path.join(BASE, "assets", "seaweed{}.png".format(str(i + 1)))
    print(seaweed_frame_path)
    frame = pg.image.load(seaweed_frame_path)
    seaweed.append(pg.transform.scale(frame, (60, 60)))


flowers = []
for i in range(4):
    flower_frame_path =  os.path.join(BASE, "assets", "flower{}.png".format(str(i + 1)))
    frame = pg.image.load(flower_frame_path)
    flowers.append(pg.transform.scale(frame, (60, 60)))


random_spots = []
for i in range(3):
    spot_frame_path =  os.path.join(BASE, "assets", "random_spot_{}.png".format(str(i + 1)))
    frame = pg.image.load(spot_frame_path)
    random_spots.append(pg.transform.scale(frame, (60, 60)))

green_fish = []
for i in range(3):
    fish_path =  os.path.join(BASE, "assets", "greenfish{}.png".format(str(i + 1)))
    frame = pg.image.load(fish_path)
    green_fish.append(pg.transform.scale(frame, (25, 25)))

red_fish = []
for i in range(3):
    fish_path =  os.path.join(BASE, "assets", "redfish{}.png".format(str(i + 1)))
    frame = pg.image.load(fish_path)
    red_fish.append(pg.transform.scale(frame, (25, 25)))


def generate_position_out_of_screen() -> pg.math.Vector2:
    from random import choice
    x_offset = [-1, -4, -10, WIDTH + 1, WIDTH + 4, WIDTH + 10]
    y_offset = [-1, -4, -10, HEIGHT + 1, HEIGHT + 4, HEIGHT + 10]

    x = choice(x_offset)
    y = choice(y_offset)

    return pg.math.Vector2(x, y)


