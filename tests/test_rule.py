import unittest
from ddt import ddt, data
from src.rule import Rule, Ruleset, RulesetFactory
from src.cell import CellState


@ddt
class ConwaysRulesetTest(unittest.TestCase):
    def setUp(self):
        self.ruleset: Ruleset = RulesetFactory.get_ruleset(Rule.CONWAYS_LIFE)

    def test_deadCell_comesToLife_IfThereAre3Neighbours(self):
        cell_state: CellState = CellState.DEAD
        expected: CellState = CellState.ALIVE
        neighbours: int = 3

        actual: CellState = self.ruleset.apply(cell_state, neighbours)

        self.assertEqual(actual, expected)

    @data(1, 2, 4, 5, 6)
    def test_deadCell_staysDead_IfThereAreLessOrMoreThan3Neighbours(self, neighbours):
        cell_state: CellState = CellState.DEAD
        expected: CellState = CellState.DEAD

        actual: CellState = self.ruleset.apply(cell_state, neighbours)

        self.assertEqual(actual, expected)

    @data(1, 4, 5, 6)
    def test_aliveCell_dies_ifThereAreLessOrMoreThanTwoOrThreeNeighbours(
            self, neighbours
    ):
        cell_state: CellState = CellState.ALIVE
        expected: CellState = CellState.DEAD

        actual: CellState = self.ruleset.apply(cell_state, neighbours)

        self.assertEqual(actual, expected)

    @data(2, 3)
    def test_aliveCell_staysAlive_ifThereAreTwoOrThreeNeighbours(self, neighbours):
        cell_state: CellState = CellState.ALIVE
        expected: CellState = CellState.ALIVE

        actual: CellState = self.ruleset.apply(cell_state, neighbours)

        self.assertEqual(actual, expected)
