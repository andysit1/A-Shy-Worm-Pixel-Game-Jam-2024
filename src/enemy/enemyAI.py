# Example file showing a basic pygame "game loop"
import pygame
from random import uniform
from .module.settings import SCREEN_RECT, generate_position_out_of_screen

MAX_FORCE = 10
vec = pygame.math.Vector2
frect = pygame.rect.FRect
# Mob properties
MOB_SIZE = 32
MAX_SPEED = 2.5
MAX_FORCE = 0.4
RAND_TARGET_TIME = 500
WANDER_RING_DISTANCE = 150
WANDER_RING_RADIUS = 50
WANDER_TYPE = 2


class EntityMovementAI():
    def __init__(self):
        self.pos = generate_position_out_of_screen()
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

    def update(self, delta):
        if WANDER_TYPE == 1:
            self.acc = self.wander()
        else:
            if not self.head.colliderect(self.collision_zone):
                self.acc = self.seek(vec(self.collision_zone.center[0], self.collision_zone.center[1])) #redirects to the center point
            else:
                self.acc = self.wander_improved()


        self.vel += self.acc
        if self.vel.length() > MAX_SPEED:
            self.vel.scale_to_length(MAX_SPEED * delta)
        self.pos += self.vel

if __name__ == "__main__":
    ai = EntityMovementAI()
    ai.update()

