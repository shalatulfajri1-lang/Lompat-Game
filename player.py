import pygame
import math
from settings import (PLAYER_WIDTH, PLAYER_HEIGHT, GRAVITY, JUMP_FORCE,
                      BASE_PLAYER_SPEED, SPEED_PER_LEVEL, MAX_PLAYER_SPEED,
                      COYOTE_MAX, BLUE, DARK_BLUE, WHITE, BLACK)


class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, PLAYER_WIDTH, PLAYER_HEIGHT)
        self.vx = BASE_PLAYER_SPEED
        self.vy = 0
        self.on_ground = False
        self.coyote_frames = 0
        self.score = 0
        self.run_frame = 0

    def set_speed(self, level):
        self.vx = min(BASE_PLAYER_SPEED + (level - 1) * SPEED_PER_LEVEL,
                      MAX_PLAYER_SPEED)

    def jump(self):
        if self.on_ground or self.coyote_frames > 0:
            self.vy = JUMP_FORCE
            self.on_ground = False
            self.coyote_frames = 0
            return True
        return False

    def update(self):
        self.vy += GRAVITY
        if self.vy > 15:
            self.vy = 15

        self.rect.x += self.vx
        self.rect.y += self.vy

        self.run_frame += 0.25

        if self.on_ground:
            self.coyote_frames = COYOTE_MAX
        elif self.coyote_frames > 0:
            self.coyote_frames -= 1

        self.on_ground = False

    def draw(self, surface, offset_x):
        sx = int(self.rect.x - offset_x)
        sy = int(self.rect.y)

        shadow = pygame.Rect(sx + 4, sy + 4, PLAYER_WIDTH, PLAYER_HEIGHT)
        pygame.draw.rect(surface, (0, 0, 0, 30), shadow, border_radius=4)

        body = pygame.Rect(sx, sy, PLAYER_WIDTH, PLAYER_HEIGHT)
        pygame.draw.rect(surface, BLUE, body, border_radius=4)
        pygame.draw.rect(surface, DARK_BLUE, body, 2, border_radius=4)

        head = pygame.Rect(sx + 4, sy - 6, PLAYER_WIDTH - 8, 14)
        pygame.draw.ellipse(surface, BLUE, head)
        pygame.draw.ellipse(surface, DARK_BLUE, head, 2)

        eye_y = sy - 1
        pygame.draw.circle(surface, WHITE, (sx + 9, eye_y), 4)
        pygame.draw.circle(surface, WHITE, (sx + 19, eye_y), 4)
        pygame.draw.circle(surface, BLACK, (sx + 10, eye_y), 2)
        pygame.draw.circle(surface, BLACK, (sx + 20, eye_y), 2)

        leg_swing = int(math.sin(self.run_frame) * 6)
        lx = sx + 4
        rx = sx + 16
        by = sy + PLAYER_HEIGHT - 4

        left_leg = pygame.Rect(lx, by, 8, max(2, 10 - leg_swing))
        right_leg = pygame.Rect(rx, by, 8, max(2, 10 + leg_swing))
        pygame.draw.rect(surface, DARK_BLUE, left_leg)
        pygame.draw.rect(surface, DARK_BLUE, right_leg)
