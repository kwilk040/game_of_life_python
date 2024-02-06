import argparse
import logging

import pygame

from board import Board, BoardPersistence
from rule import Rule, Ruleset, RulesetFactory
from ui import RendererSettings, PygameRenderer, Color, Button, ButtonFactory

logging.root.setLevel(logging.NOTSET)

parser: argparse = argparse.ArgumentParser(description='Game Of Life')
parser.add_argument('-r', '--ruleset', required=False, type=str,
                    help='Custom ruleset in birth/survival notation. Example: B3/S23.')
args = parser.parse_args()

pygame.init()
pygame.display.set_caption("Game of life")
clock: pygame.time.Clock = pygame.time.Clock()

width, height = 1000, 1000
screen = pygame.display.set_mode((width, height))

n_cells_x, n_cells_y = 100, 100
cell_width = width // n_cells_x
cell_height = height // n_cells_y

button_factory: ButtonFactory = ButtonFactory(height)

if args.ruleset is not None:
    ruleset: Ruleset = RulesetFactory.get_custom_ruleset(args.ruleset)
else:
    ruleset: Ruleset = RulesetFactory.get_ruleset(Rule.CONWAYS_LIFE)

ruleset_name: str = ruleset.get_name() if ruleset.get_rule() is not Rule.CUSTOM else ruleset.get_rulestring()

next_generation_button: Button = button_factory.create_button((width - 200) // 2, 200, Color.MUTED, "Next generation",
                                                              Color.TEXT)
start_stop_button: Button = button_factory.create_button(10, 130, Color.PINE, "Start", Color.BASE)
clear_button: Button = button_factory.create_button(150, 70, Color.MUTED,
                                                    "Clear", Color.TEXT)
randomize_button: Button = button_factory.create_button(230, 160, Color.MUTED,
                                                        "Randomize", Color.TEXT)
rule_button: Button = button_factory.create_button(610, 380, Color.MUTED,
                                                   ruleset_name, Color.TEXT)

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
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                BoardPersistence.save(board)
            if event.key == pygame.K_l:
                try:
                    new_ruleset: str = BoardPersistence.load(board)
                    ruleset = RulesetFactory.get_custom_ruleset(new_ruleset)
                    board.update_ruleset(ruleset)
                    paused = True
                    start_stop_button.label = "Start"
                    start_stop_button.color = Color.PINE
                    rule_button.label = new_ruleset
                except IOError as err:
                    logging.warning(err)
                except ValueError as err:
                    logging.warning(err)

                break
    clock.tick(60)

pygame.quit()
