import pygame
import math
from settings import COIN_COLOR, COIN_OUTLINE, COIN_RADIUS


class Coin:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.collected = False
        self.anim_frame = 0

    def update(self):
        self.anim_frame += 0.08

    def draw(self, surface, offset_x):
        if self.collected:
            return

        screen_x = int(self.x - offset_x)
        bob = int(math.sin(self.anim_frame) * 4)
        draw_y = self.y + bob

        glow_surf = pygame.Surface((COIN_RADIUS * 4, COIN_RADIUS * 4), pygame.SRCALPHA)
        for r in range(COIN_RADIUS + 8, COIN_RADIUS, -1):
            alpha = max(0, 30 - (r - COIN_RADIUS) * 3)
            if alpha > 0:
                pygame.draw.circle(glow_surf, (*COIN_COLOR, alpha),
                                   (COIN_RADIUS * 2, COIN_RADIUS * 2), r)
        surface.blit(glow_surf, (screen_x - COIN_RADIUS * 2, draw_y - COIN_RADIUS * 2))

        pygame.draw.circle(surface, COIN_COLOR, (screen_x, draw_y), COIN_RADIUS)
        pygame.draw.circle(surface, COIN_OUTLINE, (screen_x, draw_y), COIN_RADIUS, 2)

        dollar = COIN_RADIUS * 0.45
        pygame.draw.line(surface, COIN_OUTLINE,
                         (screen_x, draw_y - int(dollar)),
                         (screen_x, draw_y + int(dollar)), 2)

    def get_rect(self):
        return pygame.Rect(self.x - COIN_RADIUS, self.y - COIN_RADIUS,
                           COIN_RADIUS * 2, COIN_RADIUS * 2)
