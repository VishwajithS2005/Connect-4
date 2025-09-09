import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

GRAVITY = 800  # pixels per second^2
BALL_SIZE = 50

# Ball class
class Ball:
    def __init__(self, pos):
        self.image = pygame.Surface((BALL_SIZE, BALL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (255, 0, 0), (BALL_SIZE // 2, BALL_SIZE // 2), BALL_SIZE // 2)
        self.rect = self.image.get_rect(center=pos)
        self.velocity_y = 0
        self.settled = False

    def update(self, dt, screen_height, balls):
        # Apply gravity
        self.velocity_y += GRAVITY * dt
        self.rect.y += self.velocity_y * dt

        # Stop at the bottom (collision with floor)
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.velocity_y = 0
            self.settled = True

        # Check collision with other balls
        for ball in balls:
            if ball != self:
                if self.rect.colliderect(ball.rect):  # overlap detected
                    if self.velocity_y > 0:  # only if falling
                        self.rect.bottom = ball.rect.top
                        self.velocity_y = 0
                        self.settled = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)


balls = []

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            if balls != [] and balls[-1].settled == False:
                break
            balls.append(Ball(event.pos))
            for ball in balls:
                if ball != balls[-1] and ball.rect.colliderect(balls[-1].rect):
                    balls.remove(balls[-1])
                    print("Collision on spawn, ball not added.")
                    break

    screen.fill("black")

    # Update and draw all balls
    for ball in balls:
        if not ball.settled:
            ball.update(dt, screen.get_height(), balls)
        ball.draw(screen)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
