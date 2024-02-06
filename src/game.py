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
import argparse

from rule import Rule, Ruleset, RulesetFactory
from board import Board
from ui import RendererSettings, PygameRenderer, Color, Button, ButtonFactory

parser: argparse = argparse.ArgumentParser(description='Game Of Life')
parser.add_argument('-r', '--ruleset', required=False, type=str,
                    help='Custom ruleset in birth/survival notation. Example: B3/S23.')
args = parser.parse_args()

# Initialize Pygame
pygame.init()

# Screen dimensions
width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

# Grid dimensions
n_cells_x, n_cells_y = 100, 100
cell_width = width // n_cells_x
cell_height = height // n_cells_y

button_factory: ButtonFactory = ButtonFactory(height)

if args.ruleset is not None:
    ruleset: Ruleset = RulesetFactory.get_custom_ruleset(args.ruleset)
else:
    ruleset: Ruleset = RulesetFactory.get_ruleset(Rule.CONWAYS_LIFE)

next_generation_button: Button = button_factory.create_button((width - 200) // 2, 200, Color.MUTED, "Next generation",
                                                              Color.TEXT)
start_stop_button: Button = button_factory.create_button(10, 130, Color.PINE, "Start", Color.BASE)
clear_button: Button = button_factory.create_button(150, 70, Color.MUTED,
                                                    "Clear", Color.TEXT)
randomize_button: Button = button_factory.create_button(230, 160, Color.MUTED,
                                                        "Randomize", Color.TEXT)
rule_button: Button = button_factory.create_button(610, 380, Color.MUTED,
                                                   ruleset.get_name(), Color.TEXT)

board: Board = Board(n_cells_x, n_cells_y, ruleset)
renderer_settings: RendererSettings = RendererSettings(height, width, n_cells_x, n_cells_y, cell_height, cell_width)
renderer: PygameRenderer = PygameRenderer(screen, renderer_settings,
                                          [next_generation_button, start_stop_button, clear_button,
                                           randomize_button, rule_button])

running = True
paused: bool = True
while running:
    renderer.draw(board.current_generation)
    if not paused:
        board.next_generation()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if next_generation_button.is_clicked(event.pos[0], event.pos[1]):
                if paused:
                    board.next_generation()
                break
            if start_stop_button.is_clicked(event.pos[0], event.pos[1]):
                if paused:
                    paused = False
                    start_stop_button.label = "Stop"
                    start_stop_button.color = Color.ROSE
                else:
                    paused = True
                    start_stop_button.label = "Start"
                    start_stop_button.color = Color.PINE
                break
            if clear_button.is_clicked(event.pos[0], event.pos[1]):
                board.clear()
                paused = True
                start_stop_button.label = "Start"
                start_stop_button.color = Color.PINE
                break
            if randomize_button.is_clicked(event.pos[0], event.pos[1]):
                board.randomize()
                break
            if rule_button.is_clicked(event.pos[0], event.pos[1]):
                if event.button == 1:
                    ruleset = RulesetFactory.get_ruleset(ruleset.get_rule().next())
                if event.button == 3:
                    ruleset = RulesetFactory.get_ruleset(ruleset.get_rule().previous())
                rule_button.label = ruleset.get_name()
                board.update_ruleset(ruleset)
            else:
                x, y = event.pos[0] // cell_width, event.pos[1] // cell_height
                board.change_cell_state(x, y)
                break

pygame.quit()
