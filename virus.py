# language: Python 3.10+
# file: virus.py
# pip install pygame-ce numpy

import pygame
import random
import time
import threading
import sys
import ctypes
import winsound
import numpy as np

# Инициализация WinAPI для удержания окна сверху
user32 = ctypes.windll.user32
winmm = ctypes.windll.winmm

pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h

# Создаем окно без рамок на весь экран
flags = pygame.NOFRAME | pygame.SCALED
screen = pygame.display.set_mode((WIDTH, HEIGHT), flags)
pygame.display.set_caption("SYSTEM ERROR")

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (0, 255, 255), (255, 0, 255), (255, 255, 255)]
font_big = pygame.font.SysFont("Courier", 80, bold=True)
font_small = pygame.font.SysFont("Courier", 30, bold=True)

messages = [
    "CRITICAL ERROR", "SYSTEM HACKED", "ALL FILES ENCRYPTED",
    "WE SEE YOU", "IP: 192.168.1.1", "DON'T TRY TO CLOSE",
    "I'M IN YOUR PC", "YOU CAN'T ESCAPE", "SEND BITCOIN",
    "HELP ME", "HAHAHAHA", "TASK MANAGER WON'T HELP"
]

running = True
blink_state = True

def draw_text(text, x, y, color, font):
    shadow = font.render(text, True, (0, 0, 0))
    surf = font.render(text, True, color)
    screen.blit(shadow, (x + 2, y + 2))
    screen.blit(surf, (x, y))

def generate_scream():
    """Генерирует пронзительный звук сирены."""
    sample_rate = 44100
    duration = 1.5 
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Сирена: частота скачет от 800 до 1500 Гц
    frequency = 1000 + 500 * np.sin(2 * np.pi * 5 * t)
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)
    
    # Белый шум для скрежета
    noise = np.random.uniform(-0.3, 0.3, len(t))
    
    audio = sine_wave + noise
    audio = np.int16(audio / np.max(np.abs(audio)) * 32767)
    return audio.tobytes()

def scream_loop():
    """Бесконечно воспроизводит звук."""
    winmm.waveOutSetVolume(0, 0xFFFF) # Выкручиваем громкость на 100%
    scream_data = generate_scream()
    while running:
        try:
            winsound.PlaySound(scream_data, winsound.SND_MEMORY | winsound.SND_ASYNC | winsound.SND_LOOP)
        except:
            pass
        time.sleep(1)

def glitch_loop():
    global blink_state
    while running:
        blink_state = not blink_state
        time.sleep(0.5)

# Запускаем фоновые потоки
threading.Thread(target=glitch_loop, daemon=True).start()
threading.Thread(target=scream_loop, daemon=True).start()

clock = pygame.time.Clock()
window_id = pygame.display.get_wm_info()['window']

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = True # Игнорируем крестик
        elif event.type == pygame.KEYDOWN:
            pass # Игнорируем ВСЕ клавиши

    # Каждый кадр принудительно ставим окно поверх всех
    try:
        user32.SetWindowPos(window_id, -1, 0, 0, 0, 0, 0x0001 | 0x0002) 
    except:
        pass

    if blink_state:
        screen.fill((0, 0, 0))
    else:
        screen.fill(random.choice(colors))

    for _ in range(15):
        text = random.choice(messages)
        x = random.randint(-100, WIDTH)
        y = random.randint(-100, HEIGHT)
        color = random.choice(colors)
        font = random.choice([font_big, font_small])
        draw_text(text, x, y, color, font)

    if blink_state:
        title = font_big.render("SYSTEM HACKED", True, (255, 0, 0))
        screen.blit(title, (WIDTH // 2 - title.get_width() // 2, HEIGHT // 2 - 50))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
sys.exit()