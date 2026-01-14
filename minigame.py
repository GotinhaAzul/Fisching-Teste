import random
import sys
from dataclasses import dataclass

import pygame


@dataclass
class Fish:
    name: str
    resilience: float  # higher means less movement
    progress_modifier: float  # -0.5 slows, +0.1 speeds, etc.
    color: pygame.Color

    def movement_amplitude(self) -> float:
        return max(10.0, 120.0 * (1.0 - self.resilience))


@dataclass
class Rod:
    name: str
    control: float  # positive increases bar size

    def bar_width(self, base_width: int) -> int:
        return max(60, int(base_width * (1.0 + self.control)))


class MiniGame:
    def __init__(self, fish: Fish, rod: Rod) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((900, 200))
        pygame.display.set_caption("Minigame de Pesca")
        self.clock = pygame.time.Clock()

        self.fish = fish
        self.rod = rod

        self.track_rect = pygame.Rect(50, 80, 800, 40)
        self.base_bar_width = 160
        self.bar_speed = 260.0
        self.bar_rect = pygame.Rect(0, 0, 0, self.track_rect.height)
        self.bar_rect.width = rod.bar_width(self.base_bar_width)
        self.bar_rect.center = self.track_rect.center

        self.fish_position = float(self.track_rect.centerx)
        self.fish_velocity = 0.0

        self.progress = 0.0
        self.success_threshold = 6.0
        self.font = pygame.font.SysFont(None, 28)

    def clamp_positions(self) -> None:
        if self.bar_rect.left < self.track_rect.left:
            self.bar_rect.left = self.track_rect.left
        if self.bar_rect.right > self.track_rect.right:
            self.bar_rect.right = self.track_rect.right
        self.fish_position = max(
            self.track_rect.left, min(self.fish_position, self.track_rect.right)
        )

    def update_fish(self, dt: float) -> None:
        change = random.uniform(-1.0, 1.0) * self.fish.movement_amplitude()
        damping = max(0.15, 1.0 - self.fish.resilience)
        self.fish_velocity += change * dt
        self.fish_velocity *= 0.85 + damping * 0.1
        self.fish_position += self.fish_velocity * dt

    def update_bar(self, dt: float, mouse_down: bool) -> None:
        direction = -1 if mouse_down else 1
        self.bar_rect.x += int(direction * self.bar_speed * dt)

    def update_progress(self, dt: float) -> None:
        fish_line = pygame.Rect(int(self.fish_position) - 2, self.track_rect.top - 12, 4, 64)
        if self.bar_rect.colliderect(fish_line):
            progress_speed = 1.0 + self.fish.progress_modifier
            self.progress += dt * max(0.2, progress_speed)
        else:
            self.progress = max(0.0, self.progress - dt * 0.6)

    def render(self) -> None:
        self.screen.fill((20, 20, 30))
        pygame.draw.rect(self.screen, (60, 60, 70), self.track_rect)
        pygame.draw.rect(self.screen, (240, 240, 240), self.bar_rect)

        pygame.draw.line(
            self.screen,
            self.fish.color,
            (int(self.fish_position), self.track_rect.top - 10),
            (int(self.fish_position), self.track_rect.bottom + 10),
            6,
        )

        pygame.draw.rect(
            self.screen,
            (30, 200, 120),
            pygame.Rect(
                self.track_rect.left,
                self.track_rect.bottom + 30,
                int((self.progress / self.success_threshold) * self.track_rect.width),
                16,
            ),
        )

        status = f"Progresso: {self.progress:.1f}s / {self.success_threshold}s"
        label = self.font.render(status, True, (230, 230, 230))
        self.screen.blit(label, (self.track_rect.left, 20))

        pygame.display.flip()

    def run(self) -> None:
        running = True
        mouse_down = False
        while running:
            dt = self.clock.tick(60) / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_down = True
                if event.type == pygame.MOUSEBUTTONUP:
                    mouse_down = False

            self.update_fish(dt)
            self.update_bar(dt, mouse_down)
            self.clamp_positions()
            self.update_progress(dt)

            if self.progress >= self.success_threshold:
                running = False

            self.render()

        pygame.quit()


if __name__ == "__main__":
    example_fish = Fish(
        name="Tilapia elétrica",
        resilience=0.65,
        progress_modifier=-0.2,
        color=pygame.Color(255, 120, 120),
    )

    example_rod = Rod(name="Vara de treino", control=0.25)

    game = MiniGame(example_fish, example_rod)
    game.run()
    sys.exit(0)
