import pygame
import sys

# --- Initialization ---
pygame.init()
pygame.font.init()

# --- Screen and UI Constants ---
SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700
UI_FONT = pygame.font.Font(None, 36)
TITLE_FONT = pygame.font.Font(None, 80)
BG_COLOR = (20, 20, 40) # Dark blue
TEXT_COLOR = (230, 230, 230) # Off-white
BUTTON_COLOR = (60, 60, 90)
BUTTON_HOVER_COLOR = (90, 90, 130)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Connect 4 - Main Menu")

# --- UI Component Class ---

class Button:
    """A clickable button with hover effects."""
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.is_hovered = False

    def draw(self, surface):
        color = BUTTON_HOVER_COLOR if self.is_hovered else BUTTON_COLOR
        pygame.draw.rect(surface, color, self.rect, border_radius=10)
        
        text_surf = UI_FONT.render(self.text, True, TEXT_COLOR)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.is_hovered:
                return True
        return False


def main_menu():
    """Function to run the main menu loop."""
    # --- Create UI Elements ---
    color_label = UI_FONT.render("Select Your Color:", True, TEXT_COLOR)
    red_button = Button(150, 250, 180, 50, "Red")
    blue_button = Button(370, 250, 180, 50, "Blue")

    difficulty_label = UI_FONT.render("Select Difficulty:", True, TEXT_COLOR)
    easy_button = Button(150, 380, 120, 50, "Easy")
    medium_button = Button(290, 380, 120, 50, "Medium")
    hard_button = Button(430, 380, 120, 50, "Hard")
    
    start_button = Button(250, 520, 200, 60, "Start Game")
    
    # --- Menu State ---
    selected_color = "Red" # Default value
    selected_difficulty = "Medium" # Default value
    
    # --- Main Menu Loop ---
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Handle events for each UI element
            if red_button.handle_event(event):
                selected_color = "Red"
            if blue_button.handle_event(event):
                selected_color = "Blue"

            if easy_button.handle_event(event):
                selected_difficulty = "Easy"
            if medium_button.handle_event(event):
                selected_difficulty = "Medium"
            if hard_button.handle_event(event):
                selected_difficulty = "Hard"

            if start_button.handle_event(event):
                print(f"Starting game with Color: {selected_color}, Difficulty: {selected_difficulty}")
                return selected_color, selected_difficulty # Return selections to start the game

        # --- Drawing ---
        screen.fill(BG_COLOR)
        
        # Title
        title_surf = TITLE_FONT.render("Connect 4", True, TEXT_COLOR)
        title_rect = title_surf.get_rect(center=(SCREEN_WIDTH / 2, 100))
        screen.blit(title_surf, title_rect)
        
        # Color Buttons
        screen.blit(color_label, (150, 220))
        red_button.draw(screen)
        blue_button.draw(screen)

        # Highlight selected color
        if selected_color == "Red":
            pygame.draw.rect(screen, "gold", red_button.rect, 3, border_radius=10)
        else:
            pygame.draw.rect(screen, "gold", blue_button.rect, 3, border_radius=10)

        # Difficulty Buttons
        screen.blit(difficulty_label, (150, 350))
        easy_button.draw(screen)
        medium_button.draw(screen)
        hard_button.draw(screen)

        # Highlight selected difficulty
        if selected_difficulty == "Easy":
            pygame.draw.rect(screen, "gold", easy_button.rect, 3, border_radius=10)
        elif selected_difficulty == "Medium":
            pygame.draw.rect(screen, "gold", medium_button.rect, 3, border_radius=10)
        else:
            pygame.draw.rect(screen, "gold", hard_button.rect, 3, border_radius=10)
        
        # Start Button
        start_button.draw(screen)
        
        pygame.display.flip()

if __name__ == '__main__':
    selections = main_menu()
    if selections:
        # Here you would call your main game function, passing the selections
        # For example: run_game(color=selections[0], difficulty=selections[1])
        print("Game would start now...")
        pygame.quit()
        sys.exit()