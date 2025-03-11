# requires pygame and pywin to work
import math
import random
import pygame
from win32con import WS_EX_LAYERED, WS_EX_TRANSPARENT, GWL_EXSTYLE, LWA_COLORKEY
from win32gui import SetWindowLong, GetWindowLong, SetLayeredWindowAttributes

def generate_random_dots(num: int, width: int, height: int) -> list[tuple[int, int]]:
    """
    Generate a list of random dot positions on the screen.
    
    Args:
        num: Number of dots to generate.
        width: Width of the screen.
        height: Height of the screen.
    
    Returns:
        A list of (x, y) positions.
    """
    margin = 50
    return [(random.randint(margin, width - margin), random.randint(margin, height - margin))
            for _ in range(num)]

def generate_heart_shape(num: int, width: int, height: int) -> list[tuple[int, int]]:
    """
    Generate positions in the shape of a heart.
    
    Args:
        num: Number of points (dots) to generate.
        width: Width of the screen.
        height: Height of the screen.
    
    Returns:
        A list of (x, y) positions forming a heart shape.
    """
    heart_dots = []
    for i in range(num):
        t = math.pi * (i / (num / 2))
        x = int(16 * math.sin(t) ** 3 * 20 + width // 2)
        y = int(-((13 * math.cos(t) - 5 * math.cos(2 * t) -
                    2 * math.cos(3 * t) - math.cos(4 * t)) * 20) + height // 2 - 50)
        heart_dots.append((x, y))
    return heart_dots

def setup_display(width: int, height: int) -> pygame.Surface:
    """
    Initialize and return the pygame display with a transparent window.
    
    Args:
        width: Width of the display.
        height: Height of the display.
    
    Returns:
        The initialized pygame display surface.
    """
    screen = pygame.display.set_mode((width, height), pygame.NOFRAME)
    pygame.display.set_caption("Pulsujące serce")
    
    hwnd = pygame.display.get_wm_info()["window"]
    styles = GetWindowLong(hwnd, GWL_EXSTYLE)
    SetWindowLong(hwnd, GWL_EXSTYLE, styles | WS_EX_LAYERED | WS_EX_TRANSPARENT)
    SetLayeredWindowAttributes(hwnd, 0, 0, LWA_COLORKEY)
    
    return screen

def main() -> None:
    pygame.init()
    
    display_info = pygame.display.Info()
    WIDTH, HEIGHT = display_info.current_w, display_info.current_h

    BACKGROUND_COLOR = (0, 0, 0)
    DOT_COLOR = (80, 30, 30)
    HEART_DARK = (120, 10, 10)
    HEART_LIGHT = (255, 50, 50)
    
    NUM_DOTS = 150
    TRANSITION_TIME = 3
    PULSE_PERIOD = 2000

    screen = setup_display(WIDTH, HEIGHT)
    
    dots = generate_random_dots(NUM_DOTS, WIDTH, HEIGHT)
    heart_positions = generate_heart_shape(NUM_DOTS, WIDTH, HEIGHT)
    
    clock = pygame.time.Clock()
    start_time = pygame.time.get_ticks()
    running = True

    while running:
        screen.fill(BACKGROUND_COLOR)
        current_time = pygame.time.get_ticks()
        elapsed_time = (current_time - start_time) / 1000.0

        if elapsed_time > 2:
            pulse_time = (current_time - start_time - 2000) % PULSE_PERIOD
            pulse_factor = (math.sin(2 * math.pi * pulse_time / PULSE_PERIOD) + 1) / 2
            heart_color = (
                int(HEART_DARK[0] + pulse_factor * (HEART_LIGHT[0] - HEART_DARK[0])),
                int(HEART_DARK[1] + pulse_factor * (HEART_LIGHT[1] - HEART_DARK[1])),
                int(HEART_DARK[2] + pulse_factor * (HEART_LIGHT[2] - HEART_DARK[2]))
            )
        else:
            heart_color = DOT_COLOR

        for i, (x, y) in enumerate(dots):
            if elapsed_time > 2:
                progress = min(1.0, (elapsed_time - 2) / TRANSITION_TIME)
                target_x, target_y = heart_positions[i]
                x = int(x + (target_x - x) * progress)
                y = int(y + (target_y - y) * progress)
            pygame.draw.circle(screen, heart_color, (x, y), 3)

        pygame.display.update()
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
