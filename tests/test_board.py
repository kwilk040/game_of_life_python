import unittest

import numpy as np
from ddt import ddt, data

from src.board import Board
from src.cell import CellState
from src.rule import Rule, Ruleset, RulesetFactory


@ddt
class BoardTest(unittest.TestCase):
    def setUp(self):
        self.ruleset: Ruleset = RulesetFactory.get_ruleset(Rule.CONWAYS_LIFE)
        self.board: Board = Board(5, 5, self.ruleset)

    @data((CellState.DEAD, CellState.ALIVE), (CellState.ALIVE, CellState.DEAD))
    def test_changeCellState_changesCellStateToAOppositeState(self, cell_states):
        x: int = 0
        y: int = 0
        initial_state: CellState = cell_states[0]
        self.board.set_cell_state(x, y, initial_state)
        expected: CellState = cell_states[1]

        self.board.change_cell_state(x, y)
        actual: CellState = self.board.get_current_generation()[x, y]

        self.assertEqual(actual, expected)

    def test_nextGeneration_generatesNextGeneration_accordingToConwaysRuleset(self):
        self.board.set_cell_state(2, 3, CellState.ALIVE)
        self.board.set_cell_state(2, 1, CellState.ALIVE)
        self.board.set_cell_state(2, 2, CellState.ALIVE)
        expected: np.ndarray = np.zeros((5, 5))
        expected[1, 2] = CellState.ALIVE
        expected[2, 2] = CellState.ALIVE
        expected[3, 2] = CellState.ALIVE

        self.board.next_generation()
        actual = self.board.get_current_generation()

        np.testing.assert_array_equal(expected, actual)
