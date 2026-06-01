import pygame
import os
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, SKY_BLUE, WHITE, BLACK, RED,
                      FPS, WORLD_HEIGHT, LEVEL_UP_INTERVAL,
                      generate_sound, generate_chirp)
from world import World
from player import Player
from camera import Camera
from menu import Menu


class Game:
    def __init__(self, screen, screen_w, screen_h):
        self.screen = screen
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 64)
        self.small_font = pygame.font.Font(None, 22)

        self.menu = Menu()
        self.menu.fullscreen_on = True
        self.state = "MAIN_MENU"
        self.sound_enabled = True
        self.level = 1
        self.frame_count = 0
        self.paused = False
        self.fullscreen = True

        self.player = None
        self.camera = None
        self.world = None

        try:
            self.jump_sound = generate_sound(300, 0.12, 0.15)
        except Exception:
            self.jump_sound = None

        self.coin_sounds = []
        import sys
        if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
            base_dir = sys._MEIPASS
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))
        sound_dir = os.path.join(base_dir, "sound")

        try:
            coin1_path = os.path.join(sound_dir, "coin1.mp3")
            coin2_path = os.path.join(sound_dir, "coin2.mp3")
            if os.path.exists(coin1_path):
                self.coin_sounds.append(pygame.mixer.Sound(coin1_path))
            if os.path.exists(coin2_path):
                self.coin_sounds.append(pygame.mixer.Sound(coin2_path))
        except Exception:
            pass

        if not self.coin_sounds:
            try:
                self.coin_sounds.append(generate_sound(880, 0.08, 0.15))
            except Exception:
                pass

        self.game_over_sound = None
        try:
            go_path = os.path.join(sound_dir, "game_over.mp3")
            if os.path.exists(go_path):
                self.game_over_sound = pygame.mixer.Sound(go_path)
        except Exception:
            pass

        if not self.game_over_sound:
            try:
                self.game_over_sound = generate_chirp(400, 100, 0.6, 0.25)
            except Exception:
                pass

    def _toggle_fullscreen(self):
        self.fullscreen = not self.fullscreen
        if self.fullscreen:
            self.screen = pygame.display.set_mode(
                (self.screen_w, self.screen_h),
                pygame.FULLSCREEN | pygame.SCALED)
        else:
            self.screen = pygame.display.set_mode(
                (SCREEN_WIDTH, SCREEN_HEIGHT))

    def start_game(self):
        self.player = Player(50, SCREEN_HEIGHT - 80 - 36)
        self.camera = Camera(SCREEN_WIDTH, SCREEN_HEIGHT)
        self.world = World(self.player, level=1)
        self.world.coin_sounds = self.coin_sounds
        self.state = "PLAYING"
        self.level = 1
        self.frame_count = 0
        self.paused = False

    def restart(self):
        self.menu.state = "MAIN"
        self.menu.selected = 0
        self.state = "MAIN_MENU"

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    self._toggle_fullscreen()
                    self.menu.fullscreen_on = self.fullscreen
                elif event.key == pygame.K_ESCAPE:
                    if self.state == "SETTINGS":
                        self.state = "MAIN_MENU"
                        self.menu.state = "MAIN"
                        self.menu.selected = 0
                        continue
                    else:
                        return False

            if self.state in ("MAIN_MENU", "SETTINGS"):
                action = self.menu.handle_events(event)
                if action == "start":
                    self.start_game()
                elif action == "quit":
                    return False
                elif action == "toggle_sound":
                    self.sound_enabled = self.menu.sound_on
                    vol = 1.0 if self.sound_enabled else 0.0
                    if self.jump_sound:
                        self.jump_sound.set_volume(vol)
                    if self.game_over_sound:
                        self.game_over_sound.set_volume(vol)
                    for s in self.coin_sounds:
                        s.set_volume(vol)
                elif action == "toggle_fullscreen":
                    self._toggle_fullscreen()
                    self.menu.fullscreen_on = self.fullscreen

            elif self.state == "PLAYING":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player.jump() and self.jump_sound:
                            self.jump_sound.play()
                    elif event.key == pygame.K_p:
                        self.paused = not self.paused

            elif self.state == "GAME_OVER":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.restart()

        return True

    def update(self):
        if self.state != "PLAYING" or self.paused:
            return

        self.frame_count += 1
        new_level = self.frame_count // LEVEL_UP_INTERVAL + 1
        if new_level != self.level:
            self.level = new_level
            self.world.on_level_up(self.level)

        self.player.update()
        self.camera.update(self.player.rect.x)
        self.world.generate_ahead(self.camera.offset_x)
        self.world.cleanup(self.camera.offset_x)
        self.world.update()

        if self.player.rect.y > WORLD_HEIGHT:
            self.state = "GAME_OVER"
            if self.game_over_sound:
                self.game_over_sound.play()

    def _draw_hud(self):
        minutes = self.frame_count // 3600
        seconds = (self.frame_count // 60) % 60
        time_str = f"{minutes}:{seconds:02d}"

        score_surf = self.font.render(f"Score: {self.player.score}", True, WHITE)
        level_surf = self.font.render(f"Level: {self.level}", True, WHITE)
        time_surf = self.font.render(f"Time: {time_str}", True, WHITE)

        self.screen.blit(score_surf, (20, 15))
        self.screen.blit(level_surf, (20, 50))
        self.screen.blit(time_surf, (20, 85))

        ctrl = "[F] Fullscreen  [P] Pause  [Space] Jump"
        ctrl_surf = self.small_font.render(ctrl, True, WHITE)
        self.screen.blit(ctrl_surf, (SCREEN_WIDTH - ctrl_surf.get_width() - 15, 15))

    def _draw_pause(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(160)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        pause_text = self.big_font.render("PAUSED", True, WHITE)
        hint_text = self.font.render("Press P to Resume", True, WHITE)
        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2
        self.screen.blit(pause_text, (cx - pause_text.get_width() // 2, cy - 40))
        self.screen.blit(hint_text, (cx - hint_text.get_width() // 2, cy + 10))

    def _draw_game_over(self):
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(160)
        overlay.fill(BLACK)
        self.screen.blit(overlay, (0, 0))

        go_text = self.big_font.render("GAME OVER", True, RED)
        final_text = self.font.render(f"Final Score: {self.player.score}", True, WHITE)
        level_text = self.font.render(f"Level Reached: {self.level}", True, WHITE)
        restart_text = self.font.render("Press R to Restart", True, WHITE)

        cx = SCREEN_WIDTH // 2
        cy = SCREEN_HEIGHT // 2

        self.screen.blit(go_text, (cx - go_text.get_width() // 2, cy - 80))
        self.screen.blit(final_text, (cx - final_text.get_width() // 2, cy - 20))
        self.screen.blit(level_text, (cx - level_text.get_width() // 2, cy + 15))
        self.screen.blit(restart_text, (cx - restart_text.get_width() // 2, cy + 50))

    def draw(self):
        if self.state in ("MAIN_MENU", "SETTINGS"):
            self.menu.draw(self.screen)
            return

        self.screen.fill(SKY_BLUE)
        self.world.draw(self.screen, self.camera.offset_x)
        self._draw_hud()

        if self.paused:
            self._draw_pause()

        if self.state == "GAME_OVER":
            self._draw_game_over()

    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(FPS)
