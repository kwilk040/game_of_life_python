# To create & start using python venv:
#       python -m venv venv
#       source venv/bin/activate

# Install specific modules with pip:
# f.e.:   pip install pygame

# Requirements
# 1. Make simulation real time
# 2. Add pause / resume logic
# 3. Add save / load logic

# High-level logic
# 1. Create and init the simulation grid
# 2. Start the simulation with a tick interval of <n> seconds
# 3. At each tick:
#   3.1. Update the grid - loop over each element of the board
#   3.2. Render new generation

# General approach
# 1. Plan & write down the general workflow
#  1.1. Define Input&Output
#  1.2. Consider adding validation
# 2. Separate the main algorithms / actors in the code. Try to abstract as much common code as possible
# 3. Define communication between the objects
# 4. List the patterns you could apply
# 5. Build PoCs (Proof of concepts). Try to separate implementation of specific steps. Prepare smaller modules
#    and combine them into a complete application
# 6. Refine if needed

# Deadline - 14th of January 2024)
# Mail with:
# 1. short screen recording demonstrating the new features
# 2. Linked code
# 3. Short description of the changes. Which design patterns you used and how you applied them.

import pygame

from rule import Rule, Ruleset, RulesetFactory
from board import Board
from ui import RendererSettings, PygameRenderer, Color, Button

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 100, 100
cell_width = width // n_cells_x
cell_height = height // n_cells_y

# Button dimensions
button_width, button_height = 200, 50
button_x, button_y = (width - button_width) // 2, height - button_height - 10

next_generation_button: Button = Button(button_x, button_y, button_width, button_height, Color.MUTED, "Next generation")

ruleset: Ruleset = RulesetFactory.get_ruleset(Rule.CONWAYS_LIFE)
board: Board = Board(n_cells_x, n_cells_y, ruleset)
renderer_settings: RendererSettings = RendererSettings(height, width, n_cells_x, n_cells_y, cell_height, cell_width)
renderer: PygameRenderer = PygameRenderer(screen, renderer_settings, [next_generation_button])

board.randomize_board()

running = True
while running:
    renderer.draw(board.current_generation)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if (
                    next_generation_button.x <= event.pos[0] <= next_generation_button.x + next_generation_button.width
                    and next_generation_button.y <= event.pos[
                1] <= next_generation_button.y + next_generation_button.height
            ):
                board.next_generation()
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                board.change_cell_state(x, y)

pygame.quit()
