import pygame
import random

# Initialize pygame
pygame.init()
info = pygame.display.Info()
WIDTH, HEIGHT = info.current_w, info.current_h  # Auto-detect screen size
GRID_SIZE = 20  # Cell size
ROWS, COLS = HEIGHT // GRID_SIZE, WIDTH // GRID_SIZE
BG_COLOR = (0, 0, 0)  # Black background
FPS = 30  # Control frame rate

# Symbols and Colors
ALIVE_SYMBOLS = ['@', '*', '+', '&', 'Q', 'A', 'C', 'O']
COLORS = [(0, 255, 0), (0, 200, 200), (255, 255, 0), (255, 165, 0),
          (0, 255, 0), (0, 200, 200), (255, 255, 0), (255, 165, 0)]
DESTROYED_COLOR = (255, 0, 0)
DEAD_SYMBOL = '0'
DEAD_COLOR = (50, 50, 50)

screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
pygame.display.set_caption("Virtual World Simulation")
font = pygame.font.Font(None, GRID_SIZE)
clock = pygame.time.Clock()

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
    changed_cells = []
    for row in range(ROWS):
        for col in range(COLS):
            stage = random.randint(0, len(ALIVE_SYMBOLS) - 1)
            grid[row][col] = (ALIVE_SYMBOLS[stage], COLORS[stage])
            changed_cells.append(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
    pygame.display.update(changed_cells)

def virus_spread():
    start_row, start_col = random.randint(0, ROWS - 1), random.randint(0, COLS - 1)
    affected_cells = [(start_row, start_col)]
    
    while affected_cells:
        clock.tick(FPS)  # Control speed without blocking execution
        row, col = affected_cells.pop(0)
        grid[row][col] = ('#', DESTROYED_COLOR)
        pygame.display.update(pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE))
        
        neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1),
                     (row + 1, col + 1), (row - 1, col - 1), (row + 1, col - 1), (row - 1, col + 1)]
        for r, c in neighbors:
            if 0 <= r < ROWS and 0 <= c < COLS and grid[r][c][0] != '#':
                if random.random() < 0.5:  # Adjusted spread rate
                    affected_cells.append((r, c))

def main():
    running = True
    while running:
        bring_to_life()
        pygame.time.delay(2000)  # Delay before destruction
        virus_spread()
        pygame.time.delay(2000)  # Pause before regeneration

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
    
    pygame.quit()

if __name__ == "__main__":
    main()
