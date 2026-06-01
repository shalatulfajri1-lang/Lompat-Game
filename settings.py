import pygame
import math
import array
import random

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

SKY_BLUE = (26, 26, 46)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (52, 152, 219)
DARK_BLUE = (41, 128, 185)
COIN_COLOR = (241, 196, 15)
COIN_OUTLINE = (243, 156, 18)
PLATFORM_COLOR = (230, 126, 34)
PLATFORM_TOP = (211, 84, 0)
PLATFORM_BOTTOM = (180, 70, 0)
GROUND_COLOR = (39, 174, 96)
GROUND_TOP = (46, 204, 113)
BORDER_COLOR = (44, 62, 80)

GRAVITY = 0.5
JUMP_FORCE = -12

PLAYER_WIDTH = 28
PLAYER_HEIGHT = 36
BASE_PLAYER_SPEED = 5
SPEED_PER_LEVEL = 0.5
MAX_PLAYER_SPEED = 15
COYOTE_MAX = 8

PLATFORM_HEIGHT = 18

COIN_RADIUS = 10

LEVEL_UP_INTERVAL = 3600
GENERATION_AHEAD = 1000
CLEANUP_BEHIND = 600
BASE_MIN_GAP = 100
BASE_MAX_GAP = 180
GAP_PER_LEVEL = 6
BASE_MIN_PLAT_W = 120
BASE_MAX_PLAT_W = 170
PLAT_W_PER_LEVEL = 6
MIN_PLATFORM_Y = 180
MAX_PLATFORM_Y = 480
COINS_PER_PLATFORM_MIN = 1
COINS_PER_PLATFORM_MAX = 3

WORLD_HEIGHT = 2000

FULLSCREEN_FLAGS = pygame.SCALED


def generate_sound(frequency, duration, volume=0.3):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = array.array('h', [0]) * n_samples
    max_amp = int(volume * 32767)
    for i in range(n_samples):
        t = float(i) / sample_rate
        value = int(max_amp * math.sin(2 * math.pi * frequency * t))
        buf[i] = value
    return pygame.mixer.Sound(buffer=buf)


def generate_chirp(freq_start, freq_end, duration, volume=0.3):
    sample_rate = 22050
    n_samples = int(sample_rate * duration)
    buf = array.array('h', [0]) * n_samples
    max_amp = int(volume * 32767)
    for i in range(n_samples):
        t = float(i) / sample_rate
        freq = freq_start + (freq_end - freq_start) * (t / duration)
        value = int(max_amp * math.sin(2 * math.pi * freq * t))
        buf[i] = value
    return pygame.mixer.Sound(buffer=buf)


def generate_background_stars(count=80):
    stars = []
    for _ in range(count):
        x = random.randint(0, 3000)
        y = random.randint(0, SCREEN_HEIGHT // 2)
        radius = random.uniform(0.5, 2.0)
        brightness = random.randint(100, 255)
        stars.append((x, y, radius, brightness))
    return stars
