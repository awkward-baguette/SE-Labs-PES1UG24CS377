"""
GameEngine: owns the helicopter and all obstacles.

Handles:
- helicopter movement
- obstacle spawning
- collision detection
- game over
- distance scoring
- shield activation
- restarting the game
"""

import random
import pygame

from game.helicopter import Helicopter
from game.obstacle import Obstacle
from game.renderer import WIDTH, HEIGHT

SPAWN_INTERVAL_FRAMES = 90
GAP_HEIGHT = 150
WALL_WIDTH = 60
SCROLL_SPEED = 3


class GameEngine:
    def __init__(self):
        self._reset()

    def _reset(self):
        """Reset the entire game to its initial state."""

        self.helicopter = Helicopter(
            x=100,
            y=HEIGHT / 2
        )

        self.obstacles = []

        self.frames_until_spawn = 0

        self.game_over = False

        # Distance traveled through the scrolling world
        self.distance = 0.0

        # Shield starts inactive
        self.shield_active = False

    def _spawn_obstacle(self):
        margin = 60

        gap_y = random.randint(
            margin + GAP_HEIGHT // 2,
            HEIGHT - margin - GAP_HEIGHT // 2
        )

        self.obstacles.append(
            Obstacle(
                x=WIDTH,
                gap_y=gap_y,
                gap_height=GAP_HEIGHT,
                wall_width=WALL_WIDTH,
                screen_height=HEIGHT,
                speed=SCROLL_SPEED,
            )
        )

    def handle_input(self, keys_pressed):
        """Handle continuously-held controls."""

        self.helicopter.handle_input(keys_pressed)

    def handle_keydown(self, key):
        """Handle controls that happen once per key press."""

        # Activate shield
        if key == pygame.K_SPACE:
            if not self.game_over and not self.shield_active:
                self.shield_active = True

        # Restart after game over
        elif key == pygame.K_r:
            if self.game_over:
                self._reset()

    def update(self):
        """Update all game objects and game state."""

        self.helicopter.update(HEIGHT)
        if(self.helicopter.hit_boundary):
            self.game_over = True
                                
        # ---------------------------------------------------------
        # Distance
        # ---------------------------------------------------------
        # The helicopter remains at a fixed x position while the
        # world moves toward it. Therefore the scrolling distance
        # represents the distance traveled.
        self.distance += SCROLL_SPEED

        # ---------------------------------------------------------
        # Spawn obstacles
        # ---------------------------------------------------------
        self.frames_until_spawn -= 1

        if self.frames_until_spawn <= 0:
            self._spawn_obstacle()
            self.frames_until_spawn = SPAWN_INTERVAL_FRAMES

        # ---------------------------------------------------------
        # Update obstacles and check collisions
        # ---------------------------------------------------------
        for obstacle in self.obstacles:

            obstacle.update()

            if obstacle.check_collision(self.helicopter):

                if self.shield_active:
                    # Shield absorbs exactly one collision
                    self.shield_active = False
                    # Mark this specific obstacle as already absorbed.
                    obstacle.absorbed = True

                else:
                    # No shield -> game over
                    self.game_over = True
                    break

        # Remove obstacles that have left the screen
        self.obstacles = [
            obstacle
            for obstacle in self.obstacles
            if not obstacle.is_off_screen()
        ]

    def draw(self, surface, font):
        from game import renderer

        renderer.draw_scene(
            surface,
            self.helicopter,
            self.obstacles,
            self.distance,
            self.shield_active,
            self.game_over,
            font,
        )
