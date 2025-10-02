import pygame
from Winning_Move import *
from Draw import *
import time

# --- Initialization ---
pygame.init()
UI_HEIGHT = 100
screen = pygame.display.set_mode((700, 600 + UI_HEIGHT))
pygame.display.set_caption("Connect 4")
clock = pygame.time.Clock()
running = True
dt = 0
interact = True
# --- Constants ---
GRAVITY = 1000  # pixels per second^2
COIN_SIZE = 100

# --- Font Setup ---
UI_FONT = pygame.font.Font(None, 48)
WINNER_FONT = pygame.font.Font(None, 72)

# --- Load Coin Assets ---
try:
    RED_COIN_IMG = pygame.image.load('assets/images/coin_red.png').convert_alpha()
    BLUE_COIN_IMG = pygame.image.load('assets/images/coin_blue.png').convert_alpha()
    RED_COIN = pygame.transform.scale(RED_COIN_IMG, (COIN_SIZE, COIN_SIZE))
    BLUE_COIN = pygame.transform.scale(BLUE_COIN_IMG, (COIN_SIZE, COIN_SIZE))
except pygame.error as e:
    print(f"Error loading coin assets: {e}")
    running = False

# --- Original Board Creation ---
obstacle = pygame.Surface((700, 600), pygame.SRCALPHA)
obstacle.fill((0, 0, 180))
for x in range(0, 700, COIN_SIZE):
    for y in range(0, 600, COIN_SIZE):
        pygame.draw.circle(obstacle, (0, 0, 0, 0), (x + COIN_SIZE//2, y + COIN_SIZE//2), COIN_SIZE // 2 - 5)

# --- Coin Class ---
class Coin:
    def __init__(self, pos, color_name):
        if color_name == "red":
            self.image = RED_COIN
        elif color_name == "blue":
            self.image = BLUE_COIN
        self.rect = self.image.get_rect(center=pos)
        self.velocity_y = 0
        self.settled = False

    def update(self, dt, screen_height, coins):
        if not self.settled:
            self.velocity_y += GRAVITY * dt
            self.rect.y += self.velocity_y * dt

            if self.rect.bottom >= screen_height:
                self.rect.bottom = screen_height
                self.velocity_y = 0
                self.settled = True

            for coin in coins:
                if coin != self and self.rect.colliderect(coin.rect):
                    if self.velocity_y > 0:
                        self.rect.bottom = coin.rect.top
                        self.velocity_y = 0
                        self.settled = True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# --- Game State Variables ---
coins = []
turns = ["red", "blue"]
turn = 0
board = [[None for _ in range(7)] for _ in range(6)]
game_over = False
winner = None

# --- Main Game Loop ---
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and interact:  # left click
            if coins != [] and coins[-1].settled == False:
                break
            color = turns[turn]
            position_coin = (event.pos[0] // 100 * 100 + 50, event.pos[1] // 100 * 100 + 50)
            print(position_coin)
            coins.append(Coin(position_coin, color))
            turn = (turn + 1) % 2
            for coin in coins:
                if coin != coins[-1] and coin.rect.colliderect(coins[-1].rect):
                    coins.remove(coins[-1])
                    print("Collision on spawn, coin not added.")
                    turn = (turn - 1) % 2
                    break
    screen.fill("black")

    # --- UI Drawing ---
    if not game_over:
        if turn == 0:
            turn_text = "Red's Turn"
            text_color = "red"
        else:
            turn_text = "Blue's Turn"
            text_color = "dodgerblue"
        text_surface = UI_FONT.render(turn_text, True, text_color)
        text_rect = text_surface.get_rect(center=(screen.get_width() / 2, UI_HEIGHT / 2))
        screen.blit(text_surface, text_rect)

    for coin in coins:
        if not coin.settled:
            coin.update(dt, screen.get_height(), coins)
        else:
            row = (coin.rect.centery - UI_HEIGHT) // 100
            col = coin.rect.centerx // 100
            if 0 <= row < 6 and 0 <= col < 7 and board[row][col] is None:
                last_player_index = (turn - 1) % 2
                board[row][col] = last_player_index
                print(board)
                if Horcheck(board, last_player_index) or Vercheck(board, last_player_index) or Diag1check(board, last_player_index) or Diag2check(board, last_player_index):
                    winner = turns[last_player_index]
                    game_over = True
                if Drawcheck(board):
                    winner = ""
                    game_over = True
        coin.draw(screen)
    
    screen.blit(obstacle, (0, UI_HEIGHT))

    # --- Draw Winner Screen if Game Over ---
    if game_over:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        interact=False
        winner_text = (f"Player '{winner.capitalize()}' Wins!" if winner else "It's a Draw!")
        winner_surface = WINNER_FONT.render(winner_text, True, "gold")
        winner_rect = winner_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(winner_surface, winner_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()