import pygame
from Winning_Move import *
from Draw import *
from Minimax import *
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

        # --- Player Move ---
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and interact and turn == 0:
            col = event.pos[0] // COIN_SIZE
            row = get_next_open_row(board, col)
            if row is not None:
                # Place player piece
                board[row][col] = 0  # 0 = player (red)
                position_coin = (col * COIN_SIZE + COIN_SIZE//2, UI_HEIGHT + row * COIN_SIZE + COIN_SIZE//2)
                coins.append(Coin(position_coin, "red"))
                print(f"Player red placed at row {row}, column {col}")

                # Check for win/draw
                if winning_move(board, 0):
                    winner = "red"
                    game_over = True
                elif Drawcheck(board):
                    winner = ""
                    game_over = True

                turn = 1  # AI turn

    # --- AI Move ---
    if turn == 1 and not game_over and interact:
        col, _ = minimax(board, 4, -math.inf, math.inf, True)
        row = get_next_open_row(board, col)
        if row is not None:
            board[row][col] = 1  # 1 = AI (blue)
            position_coin = (col * COIN_SIZE + COIN_SIZE//2, UI_HEIGHT + row * COIN_SIZE + COIN_SIZE//2)
            coins.append(Coin(position_coin, "blue"))
            print(f"Player blue placed at row {row}, column {col}")

            # Check for win/draw
            if winning_move(board, 1):
                winner = "blue"
                game_over = True
            elif Drawcheck(board):
                winner = ""
                game_over = True

            turn = 0  # back to player

    # --- Drawing ---
    screen.fill("black")
    for coin in coins:
        coin.draw(screen)
    screen.blit(obstacle, (0, UI_HEIGHT))

    # --- UI Drawing ---
    if not game_over:
        turn_text = f"{'Red' if turn == 0 else 'Blue'}'s Turn"
        text_color = "red" if turn == 0 else "dodgerblue"
        text_surface = UI_FONT.render(turn_text, True, text_color)
        text_rect = text_surface.get_rect(center=(screen.get_width() / 2, UI_HEIGHT / 2))
        screen.blit(text_surface, text_rect)

    # --- Draw Winner Overlay ---
    if game_over:
        overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        interact = False
        winner_text = (f"Player '{winner.capitalize()}' Wins!" if winner else "It's a Draw!")
        winner_surface = WINNER_FONT.render(winner_text, True, "gold")
        winner_rect = winner_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
        screen.blit(winner_surface, winner_rect)

    pygame.display.flip()
    dt = clock.tick(60) / 1000

pygame.quit()
