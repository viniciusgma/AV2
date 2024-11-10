import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pygame
from src.model import ForestFire
from src.agent import TreeCell, Water, Fireman, River

# Colors dictionary for agents
COLORS = {
    "Fine": (0, 170, 0),  # Green
    "On Fire": (255, 111, 111),  # Light Red
    "Burned Out": (0, 0, 0),  # Black
    "Water": (0, 0, 255),  # Blue
    "River": (173, 216, 230),  # Light Blue
    "Fireman": (255, 255, 0),  # Yellow
}

# Screen settings
WIDTH, HEIGHT = 1000, 1000  # Pixel dimensions for the window
CELL_SIZE = 10  # Size of each cell in pixels


def draw_grid(screen, model):
    for x in range(model.grid.width):
        for y in range(model.grid.height):
            cell = model.grid[x][y]
            if cell:
                agent = cell[0]
                color = COLORS.get("Burned Out")
                if isinstance(agent, TreeCell):
                    if agent.condition > 0.7:
                        color = COLORS["Fine"]
                    elif agent.condition > 0:
                        color = COLORS["On Fire"]
                elif isinstance(agent, Water):
                    color = COLORS["Water"]
                elif isinstance(agent, River):
                    color = COLORS["River"]
                elif isinstance(agent, Fireman):
                    color = (
                        COLORS["Fireman"]
                        if agent.condition > 0
                        else COLORS["Burned Out"]
                    )

                # Draw the cell
                pygame.draw.rect(
                    screen,
                    color,
                    pygame.Rect(x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE),
                )


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Forest Fire Simulation")
    clock = pygame.time.Clock()
    running = True

    # Initialize the Forest Fire model
    model = ForestFire(
        width=WIDTH // CELL_SIZE,
        height=HEIGHT // CELL_SIZE,
        tree_density=0.6,
        water_density=0.5,
    )

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Step the model
        model.step()

        # Clear screen
        screen.fill((0, 0, 0))

        # Draw the grid based on model state
        draw_grid(screen, model)

        # Update the display
        pygame.display.flip()

        # Limit to 10 frames per second (or as preferred)
        clock.tick(10)

    pygame.quit()


if __name__ == "__main__":
    main()
