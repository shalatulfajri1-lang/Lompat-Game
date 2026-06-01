import pygame
import random
from settings import (SCREEN_WIDTH, SCREEN_HEIGHT, PLATFORM_HEIGHT,
                      WHITE, WORLD_HEIGHT, generate_background_stars,
                      GENERATION_AHEAD, CLEANUP_BEHIND,
                      BASE_MIN_GAP, BASE_MAX_GAP, GAP_PER_LEVEL,
                      BASE_MIN_PLAT_W, BASE_MAX_PLAT_W, PLAT_W_PER_LEVEL,
                      MIN_PLATFORM_Y, MAX_PLATFORM_Y,
                      COINS_PER_PLATFORM_MIN, COINS_PER_PLATFORM_MAX)
from platforms import Platform
from coin import Coin


class World:
    def __init__(self, player, level=1):
        self.player = player
        self.level = level
        self.platforms = []
        self.coins = []
        self.coin_sounds = []
        self.bg_stars = generate_background_stars(100)
        self._build_start_area()
        self._update_params()
        self.generate_ahead(0)

    def _build_start_area(self):
        start_w = 500
        start_y = SCREEN_HEIGHT - 80
        self.platforms.append(Platform(0, start_y, start_w, is_ground=True))
        for cx in [80, 230, 380]:
            self.coins.append(Coin(cx, start_y - 28))
        self._next_x = start_w + 80
        self._last_y = start_y

    def _update_params(self):
        self.player.set_speed(self.level)
        self.min_gap = BASE_MIN_GAP + (self.level - 1) * GAP_PER_LEVEL
        self.max_gap = BASE_MAX_GAP + (self.level - 1) * GAP_PER_LEVEL
        self.min_plat_w = max(60, BASE_MIN_PLAT_W - (self.level - 1) * PLAT_W_PER_LEVEL)
        self.max_plat_w = max(90, BASE_MAX_PLAT_W - (self.level - 1) * PLAT_W_PER_LEVEL)

    def on_level_up(self, new_level):
        self.level = new_level
        self._update_params()

    def generate_ahead(self, camera_x):
        limit = camera_x + SCREEN_WIDTH + GENERATION_AHEAD
        while self._next_x < limit:
            gap = random.randint(self.min_gap, self.max_gap)
            w = random.randint(self.min_plat_w, self.max_plat_w)
            dy = random.randint(-80, 120)
            y = max(MIN_PLATFORM_Y, min(MAX_PLATFORM_Y, self._last_y + dy))
            self.platforms.append(Platform(self._next_x, y, w))
            coin_count = random.randint(COINS_PER_PLATFORM_MIN,
                                        COINS_PER_PLATFORM_MAX)
            for i in range(coin_count):
                cx = self._next_x + (w // (coin_count + 1)) * (i + 1)
                self.coins.append(Coin(cx, y - 28))
            self._next_x += w + gap
            self._last_y = y

    def cleanup(self, camera_x):
        threshold = camera_x - CLEANUP_BEHIND
        self.platforms = [p for p in self.platforms
                          if p.rect.x + p.rect.width > threshold]
        self.coins = [c for c in self.coins
                      if c.x > threshold or not c.collected]

    def update(self):
        for coin in self.coins:
            coin.update()
        self._check_collisions()

    def _check_collisions(self):
        for platform in self.platforms:
            if self.player.rect.colliderect(platform.rect):
                prev_bottom = self.player.rect.bottom - self.player.vy
                if self.player.vy >= 0 and prev_bottom <= platform.rect.top + 10:
                    self.player.rect.bottom = platform.rect.top
                    self.player.vy = 0
                    self.player.on_ground = True

        for coin in self.coins:
            if not coin.collected:
                if self.player.rect.colliderect(coin.get_rect()):
                    coin.collected = True
                    self.player.score += 1
                    if self.coin_sounds:
                        random.choice(self.coin_sounds).play()

    def draw(self, surface, offset_x):
        for sx, sy, rad, bright in self.bg_stars:
            screen_x = sx - int(offset_x * 0.3)
            screen_x %= 3000
            screen_x -= 500
            if -5 < screen_x < SCREEN_WIDTH + 5:
                alpha = max(0, min(255, bright))
                if rad < 1.2:
                    surface.set_at((int(screen_x), int(sy)), (alpha, alpha, alpha))
                else:
                    pygame.draw.circle(surface, (alpha, alpha, alpha),
                                       (int(screen_x), int(sy)), int(rad))

        for platform in self.platforms:
            platform.draw(surface, offset_x)

        self.player.draw(surface, offset_x)

        for coin in self.coins:
            coin.draw(surface, offset_x)
