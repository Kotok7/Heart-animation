# pip install pygame
# pip install pywin32
import math
import random
import pygame
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, WS_EX_TOPMOST, GWL_EXSTYLE, LWA_COLORKEY, SWP_NOMOVE, SWP_NOSIZE, HWND_TOPMOST
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes, SetWindowPos, SetParent, GetDesktopWindow

BORDER_THICKNESS = 3
MARGIN = 50
DOT_RADIUS = 3

TRANSPARENT_COLOR = (1, 2, 3)
DOT_COLOR = (80, 30, 30)
HEART_DARK = (120, 10, 10)
HEART_LIGHT = (255, 50, 50)

NUM_DOTS = 150
TRANSITION_TIME = 3      # seconds after 2 seconds delay
PULSE_PERIOD = 2000      # milliseconds
DRIFT_AMPLITUDE = 5

def generate_random_dots(num, width, height):
    return [(random.randint(MARGIN, width - MARGIN), random.randint(MARGIN, height - MARGIN)) for _ in range(num)]

def generate_heart_shape(num, width, height):
    heart_dots = []
    for i in range(num):
        t = math.pi * (i / (num / 2))
        x = int(16 * math.sin(t) ** 3 * 20 + width // 2)
        y = int(-((13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)) * 20) + height // 2 - 50)
        heart_dots.append((x, y))
    return heart_dots

def setup_display(width, height):
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption("Pulsating Heart Overlay")
    hwnd = pygame.display.get_wm_info()["window"]
    # Make window a child of the desktop so it overlays current screen content
    desktop_hwnd = GetDesktopWindow()
    SetParent(hwnd, desktop_hwnd)
    styles = GetWindowLong(hwnd, GWL_EXSTYLE)
    new_styles = styles | WS_EX_LAYERED | WS_EX_TRANSPARENT | WS_EX_TOPMOST
    SetWindowLong(hwnd, GWL_EXSTYLE, new_styles)
    # Use TRANSPARENT_COLOR as colorkey so it's see-through
    SetLayeredWindowAttributes(hwnd, TRANSPARENT_COLOR[0] | (TRANSPARENT_COLOR[1] << 8) | (TRANSPARENT_COLOR[2] << 16), 0, LWA_COLORKEY)
    SetWindowPos(hwnd, HWND_TOPMOST, 0, 0, 0, 0, SWP_NOMOVE | SWP_NOSIZE)
    return screen

def main():
    pygame.init()
    display_info = pygame.display.Info()
    WIDTH, HEIGHT = display_info.current_w, display_info.current_h
    screen = setup_display(WIDTH, HEIGHT)
    dots = generate_random_dots(NUM_DOTS, WIDTH, HEIGHT)
    heart_positions = generate_heart_shape(NUM_DOTS, WIDTH, HEIGHT)
    dot_color_phases = [random.uniform(0, 2 * math.pi) for _ in range(NUM_DOTS)]
    dot_drift_phases_x = [random.uniform(0, 2 * math.pi) for _ in range(NUM_DOTS)]
    dot_drift_phases_y = [random.uniform(0, 2 * math.pi) for _ in range(NUM_DOTS)]
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    running = True

    while running:
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000.0
        screen.fill(TRANSPARENT_COLOR)
        if elapsed_time > 2:
            pulse_time = (current_time - start_time - 2000) % PULSE_PERIOD
            global_pulse = (math.sin(2 * math.pi * pulse_time / PULSE_PERIOD) + 1) / 2
        else:
            global_pulse = 0

        for i, (start_x, start_y) in enumerate(dots):
            if elapsed_time > 2:
                progress = min(1.0, (elapsed_time - 2) / TRANSITION_TIME)
                target_x, target_y = heart_positions[i]
                x = int(start_x + (target_x - start_x) * progress)
                y = int(start_y + (target_y - start_y) * progress)
            else:
                x, y = start_x, start_y

            drift_x = DRIFT_AMPLITUDE * math.sin(elapsed_time + dot_drift_phases_x[i])
            drift_y = DRIFT_AMPLITUDE * math.sin(elapsed_time + dot_drift_phases_y[i])
            x += int(drift_x)
            y += int(drift_y)

            if elapsed_time > 2:
                local_pulse = (math.sin(elapsed_time + dot_color_phases[i]) + 1) / 2
                combined_pulse = (global_pulse + local_pulse) / 2
                dot_color = (
                    int(HEART_DARK[0] + combined_pulse * (HEART_LIGHT[0] - HEART_DARK[0])),
                    int(HEART_DARK[1] + combined_pulse * (HEART_LIGHT[1] - HEART_DARK[1])),
                    int(HEART_DARK[2] + combined_pulse * (HEART_LIGHT[2] - HEART_DARK[2]))
                )
            else:
                dot_color = DOT_COLOR

            pygame.draw.circle(screen, dot_color, (x, y), DOT_RADIUS)

        pygame.draw.rect(screen, (255, 255, 255), (0, 0, WIDTH, HEIGHT), BORDER_THICKNESS)
        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
