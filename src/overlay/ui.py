# import ui

# class Interface():
#   def __init__(self, player : Player):
#     self.player = player

#     #init variables, offset means how far from 0,0 the bars are located from
#     self.h_radius = 75
#     self.m_radius = 80
#     self.h_offset = 15  #h = health
#     self.m_offset = 20  #m = mana

#     # how this works is 3.14 = 1/2 of the circle 6.28 = entire circle
#     self.start_angle = 4.71
#     self.end_angle = 6.28  # 1/4 circle

#     # the bar difference
#     self.max_arc = self.end_angle - self. start_angle

#     #end angle of health
#     self.h_end_angle = 0

#   def on_draw(self, surface : pg.Surface):
#     surface.blit(self.player.ui_pfp, (0, 0))     #draws our placeholder frog located in the top left

#     pg.draw.arc(surface, "red", (-self.h_radius + self.h_offset, -self.h_radius + self.h_offset, 2 * self.h_radius, 2 * self.h_radius),
#                     self.start_angle, self.h_end_angle, 4)
#     pg.draw.arc(surface, "blue", (-self.m_radius + self.m_offset, -self.m_radius + self.m_offset, 2 * self.m_radius, 2 * self.m_radius),
#                     self.start_angle, self.end_angle, 4)

#   def on_update(self):
#     h_ratio = self.player.health / self.player.max_health #percent health
#     self.h_end_angle = self.start_angle + self.max_arc * h_ratio # start angle + remaining health ratio in angle

#   #this handles the events of the player,
#   #in the future if we want to character to blink red or something else we can code it in here...
#   def on_event(self):
#     pass

# '''