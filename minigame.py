import random
import pygame

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 300
FPS = 60

BAR_WIDTH = 600
BAR_HEIGHT = 50
BAR_COLOR = (200, 200, 200)
BAR_OUTLINE_COLOR = (120, 120, 120)

PLAYER_BAR_WIDTH = 120
PLAYER_BAR_HEIGHT = BAR_HEIGHT
PLAYER_BAR_COLOR = (0, 0, 0)
PLAYER_SPEED = 260

FISH_WIDTH = 36
FISH_HEIGHT = 20
FISH_COLOR = (0, 150, 220)
FISH_SPEED_MIN = 60
FISH_SPEED_MAX = 160
FISH_DIR_CHANGE_MIN = 0.4
FISH_DIR_CHANGE_MAX = 1.2

BG_COLOR = (250, 250, 250)


def clamp(value: float, min_value: float, max_value: float) -> float:
    return max(min_value, min(value, max_value))


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption("Fisching - Minigame")
    clock = pygame.time.Clock()

    bar_rect = pygame.Rect(
        (WINDOW_WIDTH - BAR_WIDTH) // 2,
        (WINDOW_HEIGHT - BAR_HEIGHT) // 2,
        BAR_WIDTH,
        BAR_HEIGHT,
    )

    player_x = bar_rect.left
    fish_x = bar_rect.left + BAR_WIDTH * 0.5
    fish_speed = random.uniform(FISH_SPEED_MIN, FISH_SPEED_MAX)
    fish_direction = random.choice([-1, 1])
    fish_timer = random.uniform(FISH_DIR_CHANGE_MIN, FISH_DIR_CHANGE_MAX)

    moving_right = False
    running = True

    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                moving_right = True
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                moving_right = False

        # Update player bar
        direction = 1 if moving_right else -1
        player_x += direction * PLAYER_SPEED * dt
        player_x = clamp(player_x, bar_rect.left, bar_rect.right - PLAYER_BAR_WIDTH)

        # Update fish movement
        fish_timer -= dt
        if fish_timer <= 0:
            fish_timer = random.uniform(FISH_DIR_CHANGE_MIN, FISH_DIR_CHANGE_MAX)
            fish_direction = random.choice([-1, 1])
            fish_speed = random.uniform(FISH_SPEED_MIN, FISH_SPEED_MAX)

        fish_x += fish_direction * fish_speed * dt
        if fish_x <= bar_rect.left:
            fish_x = bar_rect.left
            fish_direction = 1
        elif fish_x >= bar_rect.right - FISH_WIDTH:
            fish_x = bar_rect.right - FISH_WIDTH
            fish_direction = -1

        # Draw
        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, BAR_COLOR, bar_rect)
        pygame.draw.rect(screen, BAR_OUTLINE_COLOR, bar_rect, 3)

        fish_rect = pygame.Rect(
            fish_x,
            bar_rect.centery - FISH_HEIGHT / 2,
            FISH_WIDTH,
            FISH_HEIGHT,
        )
        pygame.draw.ellipse(screen, FISH_COLOR, fish_rect)
        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (fish_rect.right - 8, fish_rect.centery - 2),
            3,
        )
        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (fish_rect.right - 8, fish_rect.centery - 2),
            1,
        )

        player_rect = pygame.Rect(
            player_x,
            bar_rect.top,
            PLAYER_BAR_WIDTH,
            PLAYER_BAR_HEIGHT,
        )
        pygame.draw.rect(screen, PLAYER_BAR_COLOR, player_rect)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
