import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, SKY_BLUE, WHITE, generate_background_stars


class Menu:
    def __init__(self):
        self.state = "MAIN"
        self.selected = 0
        self.sound_on = True
        self.fullscreen_on = False
        self.font_title = pygame.font.Font(None, 72)
        self.font_option = pygame.font.Font(None, 46)
        self.font_small = pygame.font.Font(None, 22)
        self.bg_stars = generate_background_stars(60)

    def _draw_background(self, surface):
        surface.fill(SKY_BLUE)
        for sx, sy, rad, bright in self.bg_stars:
            screen_x = sx % 3000 - 500
            if -5 < screen_x < SCREEN_WIDTH + 5:
                alpha = max(0, min(255, bright))
                if rad < 1.2:
                    surface.set_at((int(screen_x), int(sy)), (alpha, alpha, alpha))
                else:
                    pygame.draw.circle(surface, (alpha, alpha, alpha),
                                       (int(screen_x), int(sy)), int(rad))

    def handle_events(self, event):
        if event.type != pygame.KEYDOWN:
            return None

        if self.state == "MAIN":
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected == 0:
                    return "start"
                elif self.selected == 1:
                    self.state = "SETTINGS"
                    self.selected = 0
                    return "goto_settings"
                elif self.selected == 2:
                    return "quit"

        elif self.state == "SETTINGS":
            if event.key == pygame.K_UP:
                self.selected = (self.selected - 1) % 3
            elif event.key == pygame.K_DOWN:
                self.selected = (self.selected + 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.selected == 0:
                    self.sound_on = not self.sound_on
                    return "toggle_sound"
                elif self.selected == 1:
                    self.fullscreen_on = not self.fullscreen_on
                    return "toggle_fullscreen"
                elif self.selected == 2:
                    self.state = "MAIN"
                    self.selected = 0
                    return "back_to_menu"
            elif event.key == pygame.K_ESCAPE:
                self.state = "MAIN"
                self.selected = 0
                return "back_to_menu"

        return None

    def draw(self, surface):
        self._draw_background(surface)
        cx = SCREEN_WIDTH // 2

        if self.state == "MAIN":
            title = self.font_title.render("COIN RUNNER", True, WHITE)
            shadow = self.font_title.render("COIN RUNNER", True, (40, 40, 70))
            surface.blit(shadow, (cx - title.get_width() // 2 + 4, 84))
            surface.blit(title, (cx - title.get_width() // 2, 80))

            pygame.draw.line(surface, (80, 80, 120), (cx - 160, 148), (cx + 160, 148), 2)

            options = ["Mulai", "Setting", "Keluar"]
            start_y = 210
            spacing = 70

            for i, opt in enumerate(options):
                color = (255, 255, 255) if i == self.selected else (140, 140, 170)
                prefix = "> " if i == self.selected else "  "
                text = self.font_option.render(f"{prefix}{opt}", True, color)
                surface.blit(text, (cx - text.get_width() // 2, start_y + i * spacing))

            footer = "[F] Fullscreen  [Up/Down] Navigate  [Enter] Select  [ESC] Quit"
            f_surf = self.font_small.render(footer, True, (100, 100, 130))
            surface.blit(f_surf, (cx - f_surf.get_width() // 2, SCREEN_HEIGHT - 40))

        elif self.state == "SETTINGS":
            title = self.font_title.render("SETTINGS", True, WHITE)
            shadow = self.font_title.render("SETTINGS", True, (40, 40, 70))
            surface.blit(shadow, (cx - title.get_width() // 2 + 4, 84))
            surface.blit(title, (cx - title.get_width() // 2, 80))

            s_label = f"Sound:  {'ON' if self.sound_on else 'OFF'}"
            fs_label = f"Fullscreen:  {'ON' if self.fullscreen_on else 'OFF'}"
            options = [s_label, fs_label, "Kembali"]
            start_y = 210
            spacing = 70

            for i, opt in enumerate(options):
                color = (255, 255, 255) if i == self.selected else (140, 140, 170)
                prefix = "> " if i == self.selected else "  "
                text = self.font_option.render(f"{prefix}{opt}", True, color)
                surface.blit(text, (cx - text.get_width() // 2, start_y + i * spacing))

            hint = "[Enter] Toggle  [ESC] Back"
            h_surf = self.font_small.render(hint, True, (100, 100, 130))
            surface.blit(h_surf, (cx - h_surf.get_width() // 2, SCREEN_HEIGHT - 40))
