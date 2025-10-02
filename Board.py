import pygame
from Winning_Move import *
from Draw import *
from Minimax import *
import time

#Initialization
def run_game(player_color="red", difficulty="medium"):
    pygame.init()
    UI_HEIGHT = 100
    screen = pygame.display.set_mode((700, 600 + UI_HEIGHT))
    pygame.display.set_caption("Connect 4")
    clock = pygame.time.Clock()
    running = True
    dt = 0
    interact = True
    #Constants
    GRAVITY = 1000  # pixels per second^2
    COIN_SIZE = 100

    #Font Setup
    UI_FONT = pygame.font.Font(None, 48)
    WINNER_FONT = pygame.font.Font(None, 72)

    #Load Coin Assets
    try:
        RED_COIN_IMG = pygame.image.load('assets/images/coin_red.png').convert_alpha()
        BLUE_COIN_IMG = pygame.image.load('assets/images/coin_blue.png').convert_alpha()
        RED_COIN = pygame.transform.scale(RED_COIN_IMG, (COIN_SIZE, COIN_SIZE))
        BLUE_COIN = pygame.transform.scale(BLUE_COIN_IMG, (COIN_SIZE, COIN_SIZE))
    except pygame.error as e:
        print(f"Error loading coin assets: {e}")
        running = False

    #Original Board Creation
    obstacle = pygame.Surface((700, 600), pygame.SRCALPHA)
    obstacle.fill((0, 0, 180))
    for x in range(0, 700, COIN_SIZE):
        for y in range(0, 600, COIN_SIZE):
            pygame.draw.circle(obstacle, (0, 0, 0, 0), (x + COIN_SIZE//2, y + COIN_SIZE//2), COIN_SIZE // 2 - 5)

    #Coin Class
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
                            time.sleep(0.05)  # Small delay to ensure proper settling of the coin at the bottom.
                            self.settled = True

        def draw(self, surface):
            surface.blit(self.image, self.rect)

    #Game's State Variables
    coins = []
    turns = ["red", "blue"]
    player_color = player_color.lower()
    difficulty = difficulty.lower()
    turn = turns.index(player_color)  # 0 for player, 1 for AI
    is_red= (player_color == "red")
    depth_map = {"easy": 1, "medium": 3, "hard": 5}
    minimax_depth = depth_map.get(difficulty, 4)
    board = [[None for _ in range(7)] for _ in range(6)]
    game_over = False
    winner = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            #Player's Move
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and interact and turn == 0:
                if coins and not coins[-1].settled:
                    break  # wait until the last coin settles before player can click and place the coin.

                color = "red" if is_red else "blue"
                position_coin = (event.pos[0] // 100 * 100 + 50, 50)  # start at the top
                col = event.pos[0] // 100
                row = get_next_open_row(board, col)
                if row is None:
                    print(f"Column {col} is full. Cannot place coin.")
                    continue  # skip placing coin if a column is full
                coins.append(Coin(position_coin, color))

                # Doesn't change turn yet, waits until coin settles
        screen.fill((0, 0, 0))
        screen.blit(obstacle, (0, UI_HEIGHT))
        # Player's turn preview on hovering cursor.
        if turn == 0 and interact and not game_over:
            update_text_ui(screen, turn, game_over, UI_FONT, UI_HEIGHT,is_red)
            mouse_x, _ = pygame.mouse.get_pos()
            hover_col = mouse_x // COIN_SIZE
            if 0 <= hover_col < 7:
                # Find which row the coin would land in.
                row_preview = get_next_open_row(board, hover_col)
                if row_preview is not None:
                    preview_pos = (hover_col * COIN_SIZE + COIN_SIZE//2, UI_HEIGHT + row_preview * COIN_SIZE + COIN_SIZE//2)
                    # Draw semi-transparent red coin for preview.
                    preview_surf = pygame.Surface((COIN_SIZE, COIN_SIZE), pygame.SRCALPHA)
                    transparency_color= (255, 0, 0, 100)  if is_red else (0, 0, 255, 100)
                    pygame.draw.circle(preview_surf, transparency_color, (COIN_SIZE//2, COIN_SIZE//2), COIN_SIZE//2 - 5)
                    screen.blit(preview_surf, (hover_col * COIN_SIZE, UI_HEIGHT + row_preview * COIN_SIZE))

        #Update Coins list and draw them.
        for coin in coins:
            if not coin.settled:
                coin.update(dt, screen.get_height(), coins)
            else:
                # Only switches turn after the last coin settles
                if coin == coins[-1] and turn == 0:
                    row = (coin.rect.centery - UI_HEIGHT) // 100
                    col = coin.rect.centerx // 100
                    if 0 <= row < 6 and 0 <= col < 7 and board[row][col] is None:
                        board[row][col] = 0
                        print(f"Player {color} placed at row {row}, column {col}")
                        turn = 1-turn
                        if winning_move(board, 0):
                            winner = "Player"
                            game_over = True
                        elif Drawcheck(board):
                            winner = ""
                            game_over = True
            coin.draw(screen)

        #AI's turn
        if turn == 1 and not game_over and interact:
            if coins and not coins[-1].settled:
                pass  # Waits until the latest coin settles, and prevents AI from playing too early
            else:
                update_text_ui(screen, turn, game_over, UI_FONT, UI_HEIGHT,is_red)
                pygame.display.flip()
                col, _ = minimax(board, minimax_depth, -math.inf, math.inf, True)
                row = get_next_open_row(board, col)
                if row is not None:
                    board[row][col] = 1
                    position_coin = (col * COIN_SIZE + COIN_SIZE//2, 50)  # start from top
                    color = "blue" if is_red else "red"
                    coins.append(Coin(position_coin, color))
                    print(f"Player {color} placed at row {row}, column {col}")
                    turn = 1-turn  # back to player
                    if winning_move(board, 1):
                        winner = "AI"
                        game_over = True
                    elif Drawcheck(board):
                        winner = ""
                        game_over = True

        
        screen.blit(obstacle, (0, UI_HEIGHT))

        # Code block to draw an overlay for winner and prevent any further interaction
        if game_over:
            overlay = pygame.Surface((screen.get_width(), screen.get_height()), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))
            screen.blit(overlay, (0, 0))
            interact = False
            winner_text = (f"'{winner}' Wins!" if winner else "It's a Draw!")
            winner_surface = WINNER_FONT.render(winner_text, True, "gold")
            winner_rect = winner_surface.get_rect(center=(screen.get_width() / 2, screen.get_height() / 2))
            screen.blit(winner_surface, winner_rect)

        pygame.display.flip()
        dt = clock.tick(60) / 1000 # Delta time in seconds for an animation of 60 FPS.

    pygame.quit()

def update_text_ui(screen, turn, game_over, UI_FONT, UI_HEIGHT, is_red=True):
#UI Drawing
        if not game_over:
            pygame.draw.rect(screen, (0, 0, 0), (0, 0, screen.get_width(), UI_HEIGHT))
            turn_text = f"{'Red' if (turn+int(is_red)) == 1  else 'Blue'}'s Turn"
            text_color = "red" if (turn+int(is_red)) == 1 else "dodgerblue"
            text_surface = UI_FONT.render(turn_text, True, text_color)
            text_rect = text_surface.get_rect(center=(screen.get_width() / 2, UI_HEIGHT / 2))
            screen.blit(text_surface, text_rect)