"""
Helicopter: the player-controlled vehicle. Moves vertically based on
held Up/Down keys.
"""

import pygame

THRUST = 0.2


class Helicopter:
    def __init__(self, x, y, width=40, height=24):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vy = 0.0
        self.last_direction = 0

    def handle_input(self, keys_pressed):
        direction = 0

        if keys_pressed[pygame.K_UP]:
            direction = -1
        elif keys_pressed[pygame.K_DOWN]:
            direction = 1

        # If direction changed, immediately stop the old velocity
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
        if self.y < 0:
            self.y = 0
            self.vy = 0

        # Bottom boundary
        if self.y + self.height / 2 > height_bound:
            self.y = height_bound - self.height / 2
            self.vy = 0
        # NOTE: no corresponding check against the bottom boundary

    def get_rect(self):
        return pygame.Rect(
            int(self.x - self.width / 2), int(self.y - self.height / 2),
            self.width, self.height,
        )
