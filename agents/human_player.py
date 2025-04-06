import pygame
from game.player import Player
from ui.display import screen, CARD_WIDTH, CARD_HEIGHT, show_turn, SCREEN_WIDTH, SCREEN_HEIGHT, color_map, font

class HumanPlayer(Player):
    def __init__(self, name="Player"):
        super().__init__(name, self)
        self.is_human = True
        self.hand_y_position = 450  # Must match display.py's draw_hand y_offset

    def select_card(self, hand, top_card, playable_cards, current_color, game_state):
        clock = pygame.time.Clock()
        
        while True:
            show_turn(self.name, top_card, hand, playable_cards)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse click
                        mouse_pos = pygame.mouse.get_pos()
                        
                        # Check card click
                        card_index = self._get_clicked_card_index(mouse_pos, hand)
                        if card_index is not None:
                            card = hand[card_index]
                            if card in playable_cards:
                                print(f"Selected card: {card}")
                                if card.color is None:  # Wild card
                                    selected_color = self._choose_wild_color()
                                    if selected_color:
                                        return card, selected_color
                                else:
                                    return card, card.color
                        
                        # Check draw button click
                        if self._is_draw_button_clicked(mouse_pos):
                            print("Draw button clicked")
                            return None, None
                
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_d:  # Press 'D' to draw
                        return None, None
            
            pygame.display.flip()
            clock.tick(60)

    def _get_clicked_card_index(self, pos, hand):
        """Returns index of clicked card or None"""
        x, y = pos
        total_width = len(hand) * (CARD_WIDTH + 10) - 10
        start_x = (SCREEN_WIDTH - total_width) // 2
        
        for i in range(len(hand)):
            card_x = start_x + i * (CARD_WIDTH + 10)
            card_rect = pygame.Rect(card_x, self.hand_y_position, CARD_WIDTH, CARD_HEIGHT)
            
            if card_rect.collidepoint(x, y):
                return i
        return None

    def _is_draw_button_clicked(self, pos):
        """Check if draw button was clicked"""
        x, y = pos
        button_rect = pygame.Rect(
            SCREEN_WIDTH - 140,  # X position
            SCREEN_HEIGHT - 70,  # Y position
            120,                 # Width
            50                  # Height
        )
        return button_rect.collidepoint(x, y)

    def _choose_wild_color(self):
        """Wild card color selection dialog"""
        colors = ['Red', 'Green', 'Blue', 'Yellow']
        color_rects = []
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))
        
        # Draw color buttons
        for i, color in enumerate(colors):
            rect = pygame.Rect(
                SCREEN_WIDTH // 2 - 200 + i * 110,
                SCREEN_HEIGHT // 2 - 50,
                100,
                100
            )
            pygame.draw.rect(screen, color_map[color], rect, border_radius=10)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2, border_radius=10)
            text = font.render(color, True, (0, 0, 0))
            text_rect = text.get_rect(center=rect.center)
            screen.blit(text, text_rect)
            color_rects.append((color, rect))
        
        pygame.display.flip()
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for color, rect in color_rects:
                        if rect.collidepoint(mouse_pos):
                            return color
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()