import random
import pygame
import sys

# Initialize pygame and constants
pygame.init()
CARD_WIDTH = 80
CARD_HEIGHT = 120
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
font = pygame.font.SysFont('comicsans', 24)
big_font = pygame.font.SysFont('comicsans', 36)
title_font = pygame.font.SysFont('comicsans', 72, bold=True)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("UNO AI Game")

# Color mappings
color_map = {
    "Red": (255, 50, 50),
    "Green": (50, 200, 50),
    "Blue": (50, 100, 255),
    "Yellow": (255, 230, 50),
    None: (200, 200, 200),  # Wild cards
    "Background": (30, 160, 30),
    "Highlight": (255, 255, 0),
    "Text": (255, 255, 255),
    "Button": (70, 70, 200),
}

def draw_gradient_background():
    """Draw a gradient background"""
    for i in range(SCREEN_HEIGHT):
        color = (30, min(160, 30 + i//5), 30)
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

def draw_card(x, y, card, highlight=False, scale=1.0):
    """Draw a card at position (x,y) with optional highlight and scaling"""
    width = int(CARD_WIDTH * scale)
    height = int(CARD_HEIGHT * scale)
    color = color_map.get(card.color, (100, 100, 100))
    border_color = color_map["Highlight"] if highlight else (0, 0, 0)
    border_width = 4 if highlight else 2
    
    # Card shadow
    pygame.draw.rect(screen, (0, 0, 0, 100), (x+5, y+5, width, height), border_radius=12)
    
    # Card body
    pygame.draw.rect(screen, color, (x, y, width, height), border_radius=12)
    pygame.draw.rect(screen, border_color, (x, y, width, height), border_width, border_radius=12)

    # Card value with updated symbols
    symbol_map = {
        "Skip": "(/)",
        "Reverse": "<->",
        "Draw Two": "W+2",
        "Wild Draw Four": "W+4",
        "Wild": "WILD"
    }
    value_str = symbol_map.get(card.value, str(card.value))
    
    # Adjust font size based on card scaling
    card_font = pygame.font.SysFont('comicsans', int(24 * scale))
    
    # Center the text
    text = card_font.render(value_str, True, (0, 0, 0))
    text_rect = text.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text, text_rect)

def draw_hand(hand, y_offset, playable_cards=None):
    """Draw a player's hand with highlighting"""
    total_width = len(hand) * (CARD_WIDTH + 10) - 10
    x_offset = (SCREEN_WIDTH - total_width) // 2
    
    for i, card in enumerate(hand):
        highlight = playable_cards is not None and card in playable_cards
        draw_card(x_offset, y_offset, card, highlight)
        x_offset += CARD_WIDTH + 10

def show_turn(player_name, top_card, player_hand, playable_cards=None):
    """Display the current game state with enhanced visuals"""
    draw_gradient_background()
    
    # Draw title
    title = big_font.render("UNO GAME", True, color_map["Text"])
    screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 20))
    
    # Draw top card with animation
    draw_card(SCREEN_WIDTH//2 - CARD_WIDTH//2, 150, top_card, True, 1.1)
    
    # Draw player hand with playable cards highlighted
    draw_hand(player_hand, 450, playable_cards)
    
    # Turn info with better styling
    turn_text = font.render(f"{player_name}'s Turn", True, color_map["Text"])
    pygame.draw.rect(screen, (0, 0, 0, 150), (20, 80, turn_text.get_width()+20, turn_text.get_height()+10), border_radius=10)
    screen.blit(turn_text, (30, 85))
    
    # Enhanced draw button
    pygame.draw.rect(screen, color_map["Button"], (SCREEN_WIDTH-140, SCREEN_HEIGHT-70, 120, 50), border_radius=10)
    draw_text = font.render("Draw Card", True, color_map["Text"])
    screen.blit(draw_text, (SCREEN_WIDTH-130, SCREEN_HEIGHT-55))
    
    pygame.display.update()

def show_welcome_screen():
    """Display a welcome screen with team credits"""
    running = True
    clock = pygame.time.Clock()
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False
        
        # Draw animated background
        draw_gradient_background()
        
        # Draw title with shadow effect
        title = title_font.render("Welcome to UNO", True, (255, 255, 255))
        title_shadow = title_font.render("Welcome to UNO", True, (0, 0, 0))
        
        screen.blit(title_shadow, (SCREEN_WIDTH//2 - title.get_width()//2 + 3, 150 + 3))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 150))
        
        # Draw team credits
        team_text = big_font.render("Developed by:", True, (255, 255, 255))
        screen.blit(team_text, (SCREEN_WIDTH//2 - team_text.get_width()//2, 250))
        
        members = [
            "2301AI05", "2301AI06", "2301AI36",
            "2301CS19", "2301CS22", "2301CS73"
        ]
        
        y_offset = 300
        for i, member in enumerate(members):
            color = (
                (255, 100, 100) if i < 3 else (100, 100, 255)
            )  # Different colors for AI and CS
            member_text = font.render(member, True, color)
            screen.blit(member_text, (SCREEN_WIDTH//2 - member_text.get_width()//2, y_offset))
            y_offset += 40
        
        # Draw instruction
        instruction = font.render("Press any key to continue...", True, (200, 200, 200))
        screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 550))
        
        pygame.display.flip()
        clock.tick(30)

def draw_menu():
    """Display the game mode selection menu with enhanced visuals"""
    show_welcome_screen()  # Show welcome screen first
    
    running = True
    selected = 0
    options = [
        "AI vs AI (MCTS vs Rule-based)",
        "Human vs AI",
        "Human vs Human",
        "Tournament Mode"
    ]
    
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                if event.key == pygame.K_RETURN:
                    return selected + 1
                if event.key == pygame.K_1: return 1
                if event.key == pygame.K_2: return 2
                if event.key == pygame.K_3: return 3
                if event.key == pygame.K_4: return 4
        
        draw_gradient_background()
        
        # Draw title
        title = big_font.render("Select Game Mode", True, color_map["Text"])
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        
        # Draw options
        y_pos = 200
        for i, option in enumerate(options):
            color = color_map["Highlight"] if i == selected else color_map["Text"]
            text = font.render(f"{i+1}. {option}", True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 60
        
        # Draw instruction
        instruction = font.render("Use arrow keys to select and ENTER to confirm", True, (200, 200, 200))
        screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 500))
        
        pygame.display.flip()
        pygame.time.delay(100)

def show_winner_screen(winner_name):
    """Display the winner screen with celebration effects"""
    clock = pygame.time.Clock()
    particles = []
    
    # Create celebration particles
    for _ in range(100):
        particles.append([
            random.randint(0, SCREEN_WIDTH),
            random.randint(0, SCREEN_HEIGHT),
            random.randint(2, 5),
            random.choice([(255, 215, 0), (255, 50, 50), (50, 200, 50), (50, 100, 255)])
        ])
    
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                waiting = False
        
        screen.fill((10, 10, 10))
        
        # Draw particles
        for p in particles:
            pygame.draw.circle(screen, p[3], (p[0], p[1]), p[2])
            p[0] += random.randint(-2, 2)
            p[1] += random.randint(1, 3)
            if p[1] > SCREEN_HEIGHT:
                p[1] = 0
                p[0] = random.randint(0, SCREEN_WIDTH)
        
        # Draw winner text
        winner_text = title_font.render(f"{winner_name} Wins!", True, (255, 215, 0))
        screen.blit(winner_text, (SCREEN_WIDTH//2 - winner_text.get_width()//2, 250))
        
        # Draw celebration emoji
        celebration = big_font.render("🎉 🏆 🎊", True, (255, 255, 255))
        screen.blit(celebration, (SCREEN_WIDTH//2 - celebration.get_width()//2, 320))
        
        # Draw instruction
        instruction = font.render("Press any key to exit...", True, (200, 200, 200))
        screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 400))
        
        pygame.display.flip()
        clock.tick(30)
    
    pygame.quit()