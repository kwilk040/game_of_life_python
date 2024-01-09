import numpy as np
from cell import CellState
from rule import Ruleset


class Board:
    def __init__(self, n_cells_x: int, n_cells_y: int, ruleset: Ruleset):
        self.n_cells_x: int = n_cells_x
        self.n_cells_y: int = n_cells_y
        self.current_generation: np.ndarray = np.zeros((n_cells_x, n_cells_y))
        self.ruleset = ruleset

    def next_generation(self):
        next_generation: np.ndarray = np.copy(self.current_generation)

        for y in range(self.n_cells_y):
            for x in range(self.n_cells_x):
                n_neighbors: int = int(
                    (
                            self.current_generation[(x - 1) % self.n_cells_x, (y - 1) % self.n_cells_y]
                            + self.current_generation[(x) % self.n_cells_x, (y - 1) % self.n_cells_y]
                            + self.current_generation[(x + 1) % self.n_cells_x, (y - 1) % self.n_cells_y]
                            + self.current_generation[(x - 1) % self.n_cells_x, (y) % self.n_cells_y]
                            + self.current_generation[(x + 1) % self.n_cells_x, (y) % self.n_cells_y]
                            + self.current_generation[(x - 1) % self.n_cells_x, (y + 1) % self.n_cells_y]
                            + self.current_generation[(x) % self.n_cells_x, (y + 1) % self.n_cells_y]
                            + self.current_generation[(x + 1) % self.n_cells_x, (y + 1) % self.n_cells_y]
                    )
                )

                next_generation[x, y] = self.ruleset.apply(CellState(self.current_generation[x, y]), n_neighbors)

        self.current_generation = next_generation

    def get_current_generation(self):
        return self.current_generation

    def change_cell_state(self, x: int, y: int):
        self.current_generation[x, y] = not self.current_generation[x, y]

    def set_cell_state(self, x: int, y: int, cell_state: CellState):
        self.current_generation[x, y] = cell_state
