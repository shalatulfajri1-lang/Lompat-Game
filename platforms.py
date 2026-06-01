import pygame
from settings import PLATFORM_COLOR, PLATFORM_TOP, PLATFORM_HEIGHT, PLATFORM_BOTTOM, GROUND_COLOR, GROUND_TOP


class Platform:
    def __init__(self, x, y, width, is_ground=False):
        self.rect = pygame.Rect(x, y, width, PLATFORM_HEIGHT)
        self.is_ground = is_ground

    def draw(self, surface, offset_x):
        draw_rect = self.rect.copy()
        draw_rect.x -= offset_x

        color = GROUND_COLOR if self.is_ground else PLATFORM_COLOR
        top_color = GROUND_TOP if self.is_ground else PLATFORM_TOP

        shadow = draw_rect.copy()
        shadow.y += 4
        pygame.draw.rect(surface, (0, 0, 0, 40), shadow)

        pygame.draw.rect(surface, color, draw_rect, border_radius=3)
        pygame.draw.rect(surface, top_color, draw_rect, 2, border_radius=3)

        top_line = draw_rect.copy()
        top_line.height = 5
        highlight = pygame.Surface((top_line.width, top_line.height), pygame.SRCALPHA)
        highlight.fill((255, 255, 255, 30))
        surface.blit(highlight, top_line)

        if self.is_ground:
            for i in range(0, draw_rect.width, 40):
                line_x = draw_rect.x + i
                start_x = line_x + 10
                if start_x < draw_rect.x + draw_rect.width - 10:
                    pygame.draw.line(surface, (255, 255, 255, 20),
                                     (start_x, draw_rect.y + 2),
                                     (start_x, draw_rect.y + draw_rect.height - 2), 1)
