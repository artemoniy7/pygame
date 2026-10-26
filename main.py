import random
import pygame


# Window and game settings
WIDTH = 800
HEIGHT = 600
FPS = 60

BACKGROUND = (25, 30, 45)
WHITE = (245, 245, 245)
BLUE = (70, 160, 255)
YELLOW = (255, 210, 70)
RED = (240, 80, 90)
GREEN = (100, 220, 150)


class Player:
    """The character controlled by the player."""

    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 20, HEIGHT - 80, 40, 40)
        self.speed = 5

    def update(self, keys):
        """Move using WASD or the arrow keys."""
        dx = 0
        dy = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            dy -= self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            dy += self.speed

        self.rect.x += dx
        self.rect.y += dy

        # Keep the player inside the window.
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect, border_radius=8)


class Coin:
    """A coin that gives one point when collected."""

    def __init__(self):
        self.radius = 12
        self.x = random.randint(self.radius, WIDTH - self.radius)
        self.y = random.randint(80, HEIGHT - self.radius)
        self.rect = pygame.Rect(
            self.x - self.radius,
            self.y - self.radius,
            self.radius * 2,
            self.radius * 2,
        )

    def draw(self, screen):
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), self.radius)


class Enemy:
    """A simple enemy that moves from side to side."""

    def __init__(self):
        self.rect = pygame.Rect(100, 250, 55, 30)
        self.speed = 4

    def update(self):
        self.rect.x += self.speed

        # Reverse direction when the enemy reaches an edge.
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.speed *= -1

    def draw(self, screen):
        pygame.draw.rect(screen, RED, self.rect, border_radius=6)


class Game:
    """Runs the game loop and connects all the game objects."""

    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Collect the Coins")
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 32)
        self.big_font = pygame.font.Font(None, 64)

        self.player = Player()
        self.coin = Coin()
        self.enemy = Enemy()
        self.score = 0
        self.running = True
        self.game_over = False

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                if self.game_over and event.key == pygame.K_r:
                    self.restart()

    def update(self):
        if self.game_over:
            return

        keys = pygame.key.get_pressed()
        self.player.update(keys)
        self.enemy.update()

        # Collect the coin and place a new one.
        if self.player.rect.colliderect(self.coin.rect):
            self.score += 1
            self.coin = Coin()

        # Touching the enemy ends the round.
        if self.player.rect.colliderect(self.enemy.rect):
            self.game_over = True

    def draw_text(self, text, font, color, center):
        image = font.render(text, True, color)
        rect = image.get_rect(center=center)
        self.screen.blit(image, rect)

    def draw(self):
        self.screen.fill(BACKGROUND)

        self.coin.draw(self.screen)
        self.enemy.draw(self.screen)
        self.player.draw(self.screen)

        score_image = self.font.render(f"Coins: {self.score}", True, WHITE)
        self.screen.blit(score_image, (20, 20))

        help_image = self.font.render("Move: WASD / arrows   Esc: quit", True, WHITE)
        self.screen.blit(help_image, (20, HEIGHT - 35))

        if self.game_over:
            # A dark overlay makes the end message easier to read.
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 170))
            self.screen.blit(overlay, (0, 0))
            self.draw_text("Game over!", self.big_font, WHITE, (WIDTH // 2, HEIGHT // 2 - 35))
            self.draw_text(
                f"You collected {self.score} coin(s)",
                self.font,
                GREEN,
                (WIDTH // 2, HEIGHT // 2 + 15),
            )
            self.draw_text(
                "Press R to play again",
                self.font,
                WHITE,
                (WIDTH // 2, HEIGHT // 2 + 60),
            )

        pygame.display.flip()

    def restart(self):
        self.player = Player()
        self.coin = Coin()
        self.enemy = Enemy()
        self.score = 0
        self.game_over = False

    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()


if __name__ == "__main__":
    Game().run()
