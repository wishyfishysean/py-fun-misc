import pygame
import random
import time

# Initialize pygame
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h  # Auto-detect screen size
GRID_SIZE = 20  # Cell size
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
BG_COLOR = (0, 0, 0)  # Black background

# Symbols and Colors
ALIVE_SYMBOLS = ['@', '*', '+', '&', 'Q','A','C', 'O']  # Different symbols for life stages
COLORS = [(0, 255, 0), (0, 200, 200), (255, 255, 0), (255, 165, 0), (0, 255, 0), (0, 200, 200), (255, 255, 0), (255, 165, 0)]  # Green, Cyan, Yellow, Orange
DESTROYED_COLOR = (255, 0, 0)  # Red
DEAD_SYMBOL = '0'
DEAD_COLOR = (50, 50, 50)  # Dark Grey

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Virtual World Simulation")
font = pygame.font.Font(None, GRID_SIZE)

grid = [[(DEAD_SYMBOL, DEAD_COLOR) for _ in range(COLS)] for _ in range(ROWS)]

def draw_grid():
    screen.fill(BG_COLOR)
    for row in range(ROWS):
        for col in range(COLS):
            char, color = grid[row][col]
            text_surface = font.render(char, True, color)
            screen.blit(text_surface, (col * GRID_SIZE, row * GRID_SIZE))
    pygame.display.flip()

def bring_to_life():
    for row in range(ROWS):
        for col in range(COLS):
            stage = random.randint(0, len(ALIVE_SYMBOLS)-1)
            grid[row][col] = (ALIVE_SYMBOLS[stage], COLORS[stage])
        draw_grid()
        time.sleep(0.15)  # Slowed down by factor of 3

def virus_spread():
    start_row, start_col = random.randint(0, ROWS-1), random.randint(0, COLS-1)
    affected_cells = [(start_row, start_col)]
    
    for _ in range(random.randint(10, 30)):
        if not affected_cells:
            break
        row, col = affected_cells.pop(0)
        grid[row][col] = ('#', DESTROYED_COLOR)
        neighbors = [(row+1, col), (row-1, col), (row, col+1), (row, col-1),
                     (row+1, col+1), (row-1, col-1), (row+1, col-1), (row-1, col+1)]
        
        for r, c in neighbors:
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c][0] != '#':
                if random.random() < 0.8:  # 80% chance to spread
                    affected_cells.append((r, c))

def multiple_events():
    event_types = [virus_spread, bring_to_life]
    random.shuffle(event_types)
    for event in event_types:
        event()
        time.sleep(1.5)  # Slow delay

def main():
    running = True
    while running:
        bring_to_life()
        time.sleep(3)  # Extended time before destruction
        multiple_events()
        time.sleep(3)  # Pause before regeneration

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

    pygame.quit()

if __name__ == "__main__":
    main()
