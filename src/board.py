import logging
import time
import tkinter
import tkinter.filedialog
from io import StringIO

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

    def randomize(self):
        self.current_generation = np.random.choice([CellState.DEAD, CellState.ALIVE],
                                                   size=(self.n_cells_x, self.n_cells_y), p=[0.8, 0.2])

    def clear(self):
        self.current_generation = np.zeros((self.n_cells_x, self.n_cells_y))

    def update_ruleset(self, ruleset: Ruleset):
        self.ruleset = ruleset

    def set_current_generation(self, new_generation: np.ndarray):
        self.current_generation = new_generation


class BoardPersistence:

    @staticmethod
    def load(board: Board) -> str:
        top = tkinter.Tk()
        top.withdraw()
        file_name = tkinter.filedialog.askopenfilename(parent=top)
        top.destroy()

        if file_name == ():
            raise ValueError("No file selected")

        try:
            reader = open(f'{file_name}', 'r')
        except IOError:
            raise IOError(f'Could not open file {file_name}.')
        else:
            with reader:
                name: str = reader.readline().replace("#Name:", "").strip()
                rulestring: str = reader.readline().replace("#Rulestring:", "").strip()
                board_as_string: list[str] = reader.readlines()

                array_content: list[list[int]] = [[1 if char == '*' else 0 for char in line] for line in
                                                  board_as_string]

                new_generation: np.ndarray = np.fliplr(np.rot90(np.array(array_content), 3))
                board.set_current_generation(new_generation)
                logging.info(f'Loaded {name} with rulestring: {rulestring}')
                return rulestring

    @staticmethod
    def save(board: Board):
        content: StringIO = StringIO()
        current_timestamp: int = int(time.time())
        filename: str = f'{current_timestamp}.pylife'
        rulestring = board.ruleset.get_rulestring()
        content.write(f"#Name:{current_timestamp}\n")
        content.write(f"#Rulestring:{rulestring}\n")

        current_generation: np.ndarray = np.fliplr(
            np.rot90(board.get_current_generation(), 3))

        for x in current_generation:
            for y in x:
                content.write(f'{'*' if y == 1 else '.'}')
            content.write('\n')

        try:
            writer = open(f'saved/{filename}', 'w')
        except IOError as err:
            logging.error(f"Could not save {filename}. Cause: {err}.")
            return
        else:
            with writer:
                writer.write(content.getvalue())
                logging.info(f"Pattern successfully saved to {filename}.")
