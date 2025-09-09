import pygame
from Winning_Move import *
import time

pygame.init()
screen = pygame.display.set_mode((700, 600))
clock = pygame.time.Clock()
running = True
dt = 0

GRAVITY = 1000  # pixels per second^2
COIN_SIZE = 100

obstacle = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
obstacle.fill((0, 0, 180))
for x in range(0, screen.get_width(), COIN_SIZE):
    for y in range(0, screen.get_height(), COIN_SIZE):
        pygame.draw.circle(obstacle, (0, 0, 0, 0), (x + COIN_SIZE//2, y + COIN_SIZE//2), COIN_SIZE // 2 - 5)

class Coin:
    def __init__(self, pos, color):
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (COIN_SIZE // 2, COIN_SIZE // 2), COIN_SIZE // 2 - 5)
        self.rect = self.image.get_rect(center=pos)
        self.velocity_y = 0
        self.settled = False

    def update(self, dt, screen_height, coins):
        # Apply gravity
        self.velocity_y += GRAVITY * dt
        self.rect.y += self.velocity_y * dt

        # Stop at the bottom (collision with floor)
        if self.rect.bottom >= screen_height:
            self.rect.bottom = screen_height
            self.velocity_y = 0
            self.settled = True

        # Check collision with other coins
        for coin in coins:
            if coin != self:
                if self.rect.colliderect(coin.rect):  # overlap detected
                    if self.velocity_y > 0:  # only if falling
                        self.rect.bottom = coin.rect.top
                        self.velocity_y = 0
                        self.settled = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

coins = []
turns = ["red", "yellow"]
turn = 0
board = [[None for _ in range(7)] for _ in range(6)]

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # left click
            if coins != [] and coins[-1].settled == False:
                break
            color = turns[turn]
            position_coin = (event.pos[0] // 100 * 100 + 50, event.pos[1] // 100 * 100 + 50)
            coins.append(Coin(position_coin, color))
            turn = (turn + 1) % 2
            for coin in coins:
                if coin != coins[-1] and coin.rect.colliderect(coins[-1].rect):
                    coins.remove(coins[-1])
                    print("Collision on spawn, coin not added.")
                    turn = (turn - 1) % 2
                    break

    screen.fill("black")

    for coin in coins:
        if not coin.settled:
            coin.update(dt, screen.get_height(), coins)
        else:
            col = coin.rect.centerx // 100
            row = coin.rect.centery // 100
            if board[row][col] is None:
                board[row][col] = (turn - 1) % 2
                #print(f"Placed {turns[board[row][col]]} at ({row}, {col})")
        coin.draw(screen)
    
    if Horcheck(board, (turn - 1) % 2) or Vercheck(board, (turn - 1) % 2) or Diag1check(board, (turn - 1) % 2) or Diag2check(board, (turn - 1) % 2):
        print(f"Player {turns[(turn - 1) % 2]} wins!")
        time.sleep(2)
        running = False

    screen.blit(obstacle, (0, 0))

    pygame.display.flip()
    dt = clock.tick(60) / 1000
pygame.quit()