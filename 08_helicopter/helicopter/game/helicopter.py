"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.2


import pygame

THRUST = 0.2


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.hit_boundary = False

        self.vy = 0.0

        # -1 = up, 1 = down, 0 = no previous direction
        self.last_direction = 0

    def handle_input(self, keys_pressed):

        direction = 0

        if keys_pressed[pygame.K_UP]:
            direction = -1

        elif keys_pressed[pygame.K_DOWN]:
            direction = 1

        # If the player changes direction, immediately cancel
        # the velocity from the previous direction.
        if direction != 0 and direction != self.last_direction:
            self.vy = 0.0

        if direction == -1:
            self.vy -= THRUST

        elif direction == 1:
            self.vy += THRUST

        if direction != 0:
            self.last_direction = direction

    def update(self, height_bound):

        self.y += self.vy

        # ---------------------------------------------------------
        # Top boundary
        # ---------------------------------------------------------
        # self.y is the CENTER of the helicopter, so account for
        # half its height.
        if self.y - self.height / 2 < 0:
            self.hit_boundary = True
            self.y = self.height / 2
            self.vy = 0.0

        # ---------------------------------------------------------
        # Bottom boundary
        # ---------------------------------------------------------
        if self.y + self.height / 2 > height_bound:
            self.hit_boundary = True
            self.y = height_bound - self.height / 2
            self.vy = 0.0

    def get_rect(self):

        return pygame.Rect(
            int(self.x - self.width / 2),
            int(self.y - self.height / 2),
            self.width,
            self.height,
        )
