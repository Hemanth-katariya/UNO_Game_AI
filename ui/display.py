import random
import pygame
import sys

# --- Color mappings (define FIRST!) ---
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

# --- Pygame and constants ---
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

# --- For animated UNO symbols in the background ---
class UnoSymbol:
    def __init__(self, symbol, color, x, y, angle, size, alpha, dx, dy, glitch_timer):
        self.symbol = symbol
        self.color = color
        self.x = x
        self.y = y
        self.angle = angle
        self.size = size
        self.alpha = alpha
        self.dx = dx  # movement in x
        self.dy = dy  # movement in y
        self.glitch_timer = glitch_timer  # for glitch effect

background_uno_symbols = []

def init_uno_symbols():
    global background_uno_symbols
    uno_symbols = [
        ("0", color_map["Red"]),
        ("1", color_map["Green"]),
        ("2", color_map["Blue"]),
        ("3", color_map["Yellow"]),
        ("4", color_map["Red"]),
        ("5", color_map["Green"]),
        ("6", color_map["Blue"]),
        ("7", color_map["Yellow"]),
        ("8", color_map["Red"]),
        ("9", color_map["Green"]),
        ("<->", color_map["Blue"]),      # Reverse
        ("(/)", color_map["Yellow"]),    # Skip
        ("+2", color_map["Red"]),        # Draw Two
        ("WILD", (200, 200, 200)),       # Wild
        ("W+4", (200, 200, 200)),        # Wild Draw Four
    ]
    background_uno_symbols = []
    for _ in range(18):
        symbol, color = random.choice(uno_symbols)
        # Make the color darker
        dark_color = tuple(max(0, int(c * 0.3)) for c in color)
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        angle = random.randint(-30, 30)
        size = random.randint(36, 64)
        alpha = random.randint(40, 70)
        dx = random.uniform(-0.15, 0.15)  # very slow movement
        dy = random.uniform(-0.15, 0.15)
        glitch_timer = random.randint(30, 120)
        background_uno_symbols.append(UnoSymbol(symbol, dark_color, x, y, angle, size, alpha, dx, dy, glitch_timer))

init_uno_symbols()

def draw_gradient_background():
    """Draw a vertical gradient background with square tiles and shiny layer."""
    # Gradient background
    for i in range(SCREEN_HEIGHT):
        r = 10
        g = 10
        b = min(255, 100 + i // 2)
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

    # Square tile settings
    tile_size = 100
    shadow_offset = 6

    for y in range(0, SCREEN_HEIGHT, tile_size):
        for x in range(0, SCREEN_WIDTH, tile_size):
            # Define square points
            square_points = [
                (x, y),
                (x + tile_size, y),
                (x + tile_size, y + tile_size),
                (x, y + tile_size)
            ]

            # Shadow
            shadow_points = [(px + shadow_offset, py + shadow_offset) for (px, py) in square_points]
            pygame.draw.polygon(screen, (0, 0, 0, 60), shadow_points)

            # Main square tile
            pygame.draw.polygon(screen, (30, 144, 255), square_points)

            # Shiny highlight on top
            highlight = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            pygame.draw.polygon(highlight, (255, 255, 255, 50), [
                (10, 10),
                (tile_size - 10, 10),
                (tile_size - 30, tile_size // 3),
                (30, tile_size // 3),
            ])
            screen.blit(highlight, (x, y))
def draw_light_orange_glitter_background():
    """Draw a light orange gradient background with square tiles, shadow, and glittering effect."""
    # Light orange vertical gradient
    for i in range(SCREEN_HEIGHT):
        r = min(255, 255)
        g = min(255, 200 + i // 8)
        b = min(255, 120 + i // 12)
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

    # Square tile settings
    tile_size = 100
    shadow_offset = 7

    for y in range(0, SCREEN_HEIGHT, tile_size):
        for x in range(0, SCREEN_WIDTH, tile_size):
            # Define square points
            square_points = [
                (x, y),
                (x + tile_size, y),
                (x + tile_size, y + tile_size),
                (x, y + tile_size)
            ]

            # Shadow (soft, slightly offset)
            shadow_points = [(px + shadow_offset, py + shadow_offset) for (px, py) in square_points]
            pygame.draw.polygon(screen, (0, 0, 0, 60), shadow_points)

            # Main square tile (light orange)
            pygame.draw.polygon(screen, (255, 220, 160), square_points)

            # Glittering: random sparkles on some tiles
            if random.random() < 0.18:
                glitter_surf = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
                for _ in range(random.randint(2, 5)):
                    gx = random.randint(10, tile_size-10)
                    gy = random.randint(10, tile_size-10)
                    gr = random.randint(2, 4)
                    ga = random.randint(120, 200)
                    pygame.draw.circle(glitter_surf, (255, 255, 255, ga), (gx, gy), gr)
                screen.blit(glitter_surf, (x, y))

            # Shiny highlight on top (subtle white polygon)
            highlight = pygame.Surface((tile_size, tile_size), pygame.SRCALPHA)
            pygame.draw.polygon(highlight, (255, 255, 255, 40), [
                (10, 10),
                (tile_size - 10, 10),
                (tile_size - 30, tile_size // 3),
                (30, tile_size // 3),
            ])
            screen.blit(highlight, (x, y))
           
def draw_light_green_trapezium_background():
    """Draw a shiny light green gradient background with trapezium tiles and reflecting shadow."""
    # Light green vertical gradient
    for i in range(SCREEN_HEIGHT):
        r = min(255, 180 + i // 8)
        g = min(255, 255)
        b = min(255, 200 + i // 16)
        color = (r, g, b)
        pygame.draw.line(screen, color, (0, i), (SCREEN_WIDTH, i))

    # Trapezium tile settings
    tile_w = 120
    tile_h = 80
    shadow_offset = 12

    for y in range(0, SCREEN_HEIGHT, tile_h):
        for x in range(0, SCREEN_WIDTH, tile_w):
            # Trapezium points (top shorter than bottom)
            top_shrink = 24
            points = [
                (x + top_shrink, y),
                (x + tile_w - top_shrink, y),
                (x + tile_w, y + tile_h),
                (x, y + tile_h)
            ]

            # Reflecting shadow (drawn below and slightly offset)
            shadow_points = [(px, py + shadow_offset) for (px, py) in points]
            pygame.draw.polygon(screen, (60, 120, 60, 60), shadow_points)

            # Main trapezium tile (shiny light green)
            pygame.draw.polygon(screen, (180, 255, 180), points)

            # Shiny highlight (simulate gloss)
            highlight = pygame.Surface((tile_w, tile_h), pygame.SRCALPHA)
            pygame.draw.polygon(
                highlight,
                (255, 255, 255, 60),
                [
                    (top_shrink + 8, 8),
                    (tile_w - top_shrink - 8, 8),
                    (tile_w - top_shrink - 24, tile_h // 3),
                    (top_shrink + 24, tile_h // 3)
                ]
            )
            screen.blit(highlight, (x, y))

            # Glittering: random sparkles on some tiles
            if random.random() < 0.15:
                glitter_surf = pygame.Surface((tile_w, tile_h), pygame.SRCALPHA)
                for _ in range(random.randint(2, 4)):
                    gx = random.randint(10, tile_w-10)
                    gy = random.randint(10, tile_h-10)
                    gr = random.randint(2, 4)
                    ga = random.randint(120, 200)
                    pygame.draw.circle(glitter_surf, (255, 255, 255, ga), (gx, gy), gr)
                screen.blit(glitter_surf, (x, y))


def draw_uno_symbols_on_background():
    for s in background_uno_symbols:
        # Glitch effect: occasionally jump a few pixels
        if s.glitch_timer <= 0:
            s.x += random.randint(-5, 5)
            s.y += random.randint(-5, 5)
            s.angle += random.randint(-10, 10)
            s.glitch_timer = random.randint(30, 120)
        else:
            s.glitch_timer -= 1

        # Move slowly
        s.x += s.dx
        s.y += s.dy

        # Wrap around screen
        if s.x < 0: s.x = SCREEN_WIDTH
        if s.x > SCREEN_WIDTH: s.x = 0
        if s.y < 0: s.y = SCREEN_HEIGHT
        if s.y > SCREEN_HEIGHT: s.y = 0

        # Draw symbol (dark, shiny, semi-transparent)
        symbol_font = pygame.font.SysFont('comicsans', s.size, bold=True)
        text_surface = symbol_font.render(s.symbol, True, s.color)
        text_surface.set_alpha(s.alpha)
        text_surface = pygame.transform.rotate(text_surface, s.angle)
        screen.blit(text_surface, (int(s.x), int(s.y)))

        # Shiny overlay (white, very transparent, offset for shine)
        shine = pygame.Surface(text_surface.get_size(), pygame.SRCALPHA)
        pygame.draw.ellipse(shine, (255,255,255,30), (0, 0, text_surface.get_width(), text_surface.get_height()//3))
        screen.blit(shine, (int(s.x), int(s.y)), special_flags=pygame.BLEND_RGBA_ADD)

def draw_card(x, y, card, highlight=False, scale=1.0, pulse_time=None, show_tooltip=False):
    """
    Draw a card at position (x, y) with optional highlight, scaling, pulsing animation, and tooltip.
    - pulse_time: time in seconds (float), used for pulsing highlight animation.
    - show_tooltip: if True, display a tooltip with card details above the card.
    """
    width = int(CARD_WIDTH * scale)
    height = int(CARD_HEIGHT * scale)
    color = color_map.get(card.color, (100, 100, 100))
    border_color = color_map["Highlight"] if highlight else (0, 0, 0)
    border_width = 4 if highlight else 2

    # --- Animated pulsing border if highlighted ---
    if highlight and pulse_time is not None:
        # Pulse border width between 4 and 10 pixels
        import math
        pulse = 4 + int(6 * (0.5 + 0.5 * math.sin(pulse_time * 3)))
        border_width = pulse
        # Optionally, pulse the border color brightness
        border_color = tuple(min(255, int(c * (1.0 + 0.2 * math.sin(pulse_time * 3)))) for c in color_map["Highlight"])

    # Card shadow (with alpha)
    shadow_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    shadow_surf.fill((0, 0, 0, 80))
    screen.blit(shadow_surf, (x+5, y+5))

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

    # Accessible, high-contrast text
    text_color = (0, 0, 0) if sum(color) > 400 else (255, 255, 255)
    card_font = pygame.font.SysFont('comicsans', int(28 * scale), bold=True)
    text = card_font.render(value_str, True, text_color)
    text_rect = text.get_rect(center=(x + width//2, y + height//2))
    screen.blit(text, text_rect)

    # --- Tooltip on hover ---
    if show_tooltip:
        tooltip_font = pygame.font.SysFont('arial', 18, bold=True)
        tooltip_text = f"{card.color} {card.value}"
        tooltip_surf = tooltip_font.render(tooltip_text, True, (255,255,255), (0,0,0))
        tooltip_rect = tooltip_surf.get_rect(midbottom=(x + width//2, y - 5))
        screen.blit(tooltip_surf, tooltip_rect)

    # --- Optional: Fade-in animation (call this in your main loop, not here) ---
    # To fade in, draw a semi-transparent white/black surface over the card and decrease its alpha over time.

# Example usage in your main loop:
# pulse_time = pygame.time.get_ticks() / 1000.0  # seconds
# draw_card(x, y, card, highlight=is_selected, scale=1.0, pulse_time=pulse_time, show_tooltip=mouse_over_card)


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
    draw_light_orange_glitter_background()
    draw_uno_symbols_on_background()

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
        draw_uno_symbols_on_background()

        # def show_welcome_screen():
   
    running = True
    clock = pygame.time.Clock()

    # Fonts for title and credits
    title_font = pygame.font.SysFont("lucidahandwriting,arial", 72, bold=True, italic=True)
    big_font = pygame.font.SysFont("verdana,arial", 36, bold=True)
    font = pygame.font.SysFont("tahoma,arial", 28)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                running = False

        # Draw animated background
        draw_gradient_background()
        draw_uno_symbols_on_background()

        # --- Draw Title ---
        title_text = "Welcome to UNO"
        title_surface = title_font.render(title_text, True, (80, 40, 120))  # Dark purple
        title_shadow = title_font.render(title_text, True, (60, 60, 60))  # Grey shadow with opacity

        # Add background rectangle for the title
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 150))
        pygame.draw.rect(screen, (220, 220, 255), (title_rect.x - 20, title_rect.y - 10, title_rect.width + 40, title_rect.height + 20), border_radius=12)
        screen.blit(title_shadow, (title_rect.x + 3, title_rect.y + 3))  # Shadow offset
        screen.blit(title_surface, title_rect)

        # --- Draw "Developed By" Box ---
        team_text = big_font.render("Developed by:", True, (0, 100, 0))  # Dark green
        team_box_rect = team_text.get_rect(center=(SCREEN_WIDTH // 2, 250))
        pygame.draw.rect(screen, (200, 255, 200), (team_box_rect.x - 20, team_box_rect.y - 10, team_box_rect.width + 40, team_box_rect.height + 20), border_radius=12)
        screen.blit(team_text, team_box_rect)

        # --- Draw Roll Numbers ---
        members = [
            "2301AI05", "2301AI06", "2301AI36",
            "2301CS19", "2301CS22", "2301CS73"
        ]
        y_offset = 300

        for i, member in enumerate(members):
            member_color = (2, 15, 100)  # Golden yellow for roll numbers
            member_surface = font.render(member, True, member_color)

            # Add background rectangle for roll numbers
            member_rect = member_surface.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
            pygame.draw.rect(screen, (255, 240, 200), (member_rect.x - 20, member_rect.y - 10, member_rect.width + 40, member_rect.height + 20), border_radius=12)
            screen.blit(member_surface, member_rect)

            y_offset += 50

        # --- Draw Instruction ---
        instruction_text = "Press any key to continue..."
        instruction_surface = font.render(instruction_text, True, (120, 66, 189))
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100))
        screen.blit(instruction_surface, instruction_rect)

        pygame.display.flip()
        clock.tick(30)


        # Draw instruction
        # instruction = font.render("Press any key to continue...", True, (200, 200, 200))
        # screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 550))

        # pygame.display.flip()
        # clock.tick(30)

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

        draw_light_green_trapezium_background()
        draw_uno_symbols_on_background()

        # Draw title
        title_font = pygame.font.SysFont('comicsans', 36, bold=True)
        title = title_font.render("Select Game Mode", True, (255, 0, 0))
        screen.blit(title, (SCREEN_WIDTH//2 - title.get_width()//2, 100))
        # Draw options
        y_pos = 200
        for i, option in enumerate(options):
            dark_maroon = (80, 0, 0)
            color = color_map["Highlight"] if i == selected else dark_maroon
            option_rect = pygame.Rect(
            SCREEN_WIDTH//2 - 200,  # Center the rectangle horizontally
            y_pos - 10,             # Add padding above the text
            400,                    # Fixed width for the background
            50                      # Fixed height for the background
            )
            pygame.draw.rect(screen, (255, 165, 0), option_rect, border_radius=20)
            text = font.render(f"{i+1}. {option}", True, color)
            screen.blit(text, (SCREEN_WIDTH//2 - text.get_width()//2, y_pos))
            y_pos += 60
 
        # Draw instruction
        instruction = font.render("Use arrow keys to select and ENTER to confirm", True, (160, 62, 210))
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
        instruction = font.render("Press any key to exit...", True, (36, 20, 230))
        screen.blit(instruction, (SCREEN_WIDTH//2 - instruction.get_width()//2, 400))

        pygame.display.flip()
        clock.tick(30)

    pygame.quit()
