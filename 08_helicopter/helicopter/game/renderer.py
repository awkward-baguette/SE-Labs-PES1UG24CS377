"""
renderer: all pygame drawing lives here, kept separate from game logic.

"""

import pygame


WIDTH, HEIGHT = 700, 500

WINDOW_SIZE = (WIDTH, HEIGHT)

COLOR_BG = (140, 200, 230)

COLOR_HELI = (60, 60, 70)

COLOR_OBSTACLE = (70, 150, 80)

COLOR_TEXT = (20, 20, 20)

COLOR_SHIELD = (50, 100, 255)

COLOR_GAME_OVER = (180, 40, 40)


def draw_scene(
    surface,
    helicopter,
    obstacles,
    distance,
    shield_active,
    game_over,
    font
):

    # Background
    surface.fill(COLOR_BG)

    # ---------------------------------------------------------
    # Obstacles
    # ---------------------------------------------------------
    for obstacle in obstacles:

        pygame.draw.rect(
            surface,
            COLOR_OBSTACLE,
            obstacle.get_top_rect()
        )

        pygame.draw.rect(
            surface,
            COLOR_OBSTACLE,
            obstacle.get_bottom_rect()
        )

    # ---------------------------------------------------------
    # Helicopter
    # ---------------------------------------------------------
    helicopter_rect = helicopter.get_rect()

    pygame.draw.rect(
        surface,
        COLOR_HELI,
        helicopter_rect,
        border_radius=4
    )

    # ---------------------------------------------------------
    # Shield
    # ---------------------------------------------------------
    if shield_active:

        center = helicopter_rect.center

        # Draw a circle around the helicopter to make the shield
        # clearly visible.
        radius = max(
            helicopter_rect.width,
            helicopter_rect.height
        )

        pygame.draw.circle(
            surface,
            COLOR_SHIELD,
            center,
            radius,
            width=3
        )

        draw_text(
            surface,
            font,
            "SHIELD ACTIVE",
            (10, 35),
            COLOR_SHIELD
        )

    # ---------------------------------------------------------
    # Distance
    # ---------------------------------------------------------
    distance_text = f"Distance: {int(distance)}"

    draw_text(
        surface,
        font,
        distance_text,
        (10, 10)
    )

    # ---------------------------------------------------------
    # Game Over
    # ---------------------------------------------------------
    if game_over:

        # Dark transparent overlay
        overlay = pygame.Surface(
            surface.get_size(),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 100))

        surface.blit(
            overlay,
            (0, 0)
        )

        draw_banner(
            surface,
            font,
            f"GAME OVER - Distance: {int(distance)}"
        )

        restart_font = pygame.font.SysFont(
            "consolas",
            20
        )

        restart_text = restart_font.render(
            "Press R to restart",
            True,
            (255, 255, 255)
        )

        restart_rect = restart_text.get_rect(
            center=(
                surface.get_width() // 2,
                surface.get_height() // 2 + 40
            )
        )

        surface.blit(
            restart_text,
            restart_rect
        )


def draw_text(
    surface,
    font,
    text,
    pos,
    color=COLOR_TEXT
):

    surface.blit(
        font.render(text, True, color),
        pos
    )


def draw_banner(surface, font, text):

    # Use a larger font for the game-over message
    banner_font = pygame.font.SysFont(
        "consolas",
        32,
        bold=True
    )

    surf = banner_font.render(
        text,
        True,
        COLOR_GAME_OVER
    )

    rect = surf.get_rect(
        center=(
            surface.get_width() // 2,
            surface.get_height() // 2
        )
    )

    surface.blit(
        surf,
        rect
    )
