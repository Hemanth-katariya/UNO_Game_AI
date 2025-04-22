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

    def draw_uno_symbols_on_background():
  
    # Define possible symbols and their colors
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
    # Randomly scatter symbols across the background
    for _ in range(18):  # Number of symbols to draw
        symbol, color = random.choice(uno_symbols)
        # Random position
        x = random.randint(50, SCREEN_WIDTH - 50)
        y = random.randint(50, SCREEN_HEIGHT - 50)
        # Random rotation and transparency
        angle = random.randint(-30, 30)
        alpha = 60  # Transparency (0-255)
        # Font size for background symbols
        size = random.randint(36, 64)
        symbol_font = pygame.font.SysFont('comicsans', size, bold=True)
        text_surface = symbol_font.render(symbol, True, color)
        # Add transparency
        text_surface.set_alpha(alpha)
        # Rotate the symbol
        text_surface = pygame.transform.rotate(text_surface, angle)
        # Blit to screen
        screen.blit(text_surface, (x, y))