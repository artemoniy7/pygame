import pygame

# Размер окна
WIDTH = 800
HEIGHT = 600


class Paddle:
    def __init__(self, x):
        self.rect = pygame.Rect(x, HEIGHT // 2 - 50, 15, 100)
        self.speed = 6

    def move(self, direction):
        self.rect.y += direction * self.speed
        self.rect.clamp_ip(pygame.Rect(0, 0, WIDTH, HEIGHT))

    def draw(self, screen):
        pygame.draw.rect(screen, (240, 240, 240), self.rect)


class Ball:
    def __init__(self):
        self.rect = pygame.Rect(WIDTH // 2 - 10, HEIGHT // 2 - 10, 20, 20)
        self.speed_x = 5
        self.speed_y = 4

    def update(self, player, bot):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

        # Отскок от верхней и нижней стен
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

        # Отскок от пластин
        if self.rect.colliderect(player.rect) and self.speed_x < 0:
            self.speed_x *= -1
        if self.rect.colliderect(bot.rect) and self.speed_x > 0:
            self.speed_x *= -1

    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 220, 80), self.rect)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Простой пинг-понг")
    clock = pygame.time.Clock()

    player = Paddle(30)
    bot = Paddle(WIDTH - 45)
    ball = Ball()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Игрок управляет своей пластиной стрелками вверх и вниз
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            player.move(-1)
        if keys[pygame.K_DOWN]:
            player.move(1)

        # Самый простой бот: двигается к мячу по вертикали
        if bot.rect.centery < ball.rect.centery:
            bot.move(1)
        elif bot.rect.centery > ball.rect.centery:
            bot.move(-1)

        ball.update(player, bot)

        # Если мяч вылетел за край, начинаем заново
        if ball.rect.right < 0 or ball.rect.left > WIDTH:
            ball = Ball()

        screen.fill((25, 30, 45))

        # Пунктирная линия посередине поля
        for y in range(0, HEIGHT, 30):
            pygame.draw.rect(screen, (90, 95, 110), (WIDTH // 2 - 2, y, 4, 15))

        player.draw(screen)
        bot.draw(screen)
        ball.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
