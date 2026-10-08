"""
Obstacle: a scrolling wall pair with a gap the helicopter must fly
through.

import pygame
"""

import pygame


class Obstacle:
    def __init__(
        self,
        x,
        gap_y,
        gap_height,
        wall_width,
        screen_height,
        speed
    ):
        self.x = x
        self.gap_y = gap_y
        self.gap_height = gap_height
        self.wall_width = wall_width
        self.screen_height = screen_height
        self.speed = speed

        self.scored = False
        self.absorbed = False

    def update(self):
        self.x -= self.speed

    def is_off_screen(self):
        return self.x + self.wall_width < 0

    def get_top_rect(self):
        top_height = self.gap_y - self.gap_height / 2

        return pygame.Rect(
            int(self.x),
            0,
            self.wall_width,
            int(top_height)
        )

    def get_bottom_rect(self):
        bottom_y = self.gap_y + self.gap_height / 2

        return pygame.Rect(
            int(self.x),
            int(bottom_y),
            self.wall_width,
            int(self.screen_height - bottom_y)
        )

    def check_collision(self, helicopter):
        if self.absorbed:
            return False
        
        helicopter_rect = helicopter.get_rect()


        top_collision = helicopter_rect.colliderect(
            self.get_top_rect()
        )

        bottom_collision = helicopter_rect.colliderect(
            self.get_bottom_rect()
        )

        return top_collision or bottom_collision
