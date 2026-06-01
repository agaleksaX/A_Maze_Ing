from maze.cell import Cell


class Maze:

    def __init__(self, width: int, height: int):

        self.width = width
        self.height = height
        self.cells: list[list[Cell]] = self._create_cells()

    def _create_cells(self) -> list[list[Cell]]:

        cells: list[list[Cell]] = []

        for y in range(self.height):
            row: list[Cell] = []

            for x in range(self.width):
                row.append(Cell(x, y))

            cells.append(row)

        return cells

    def get_cell(self, x: int, y: int) -> Cell:
        return self.cells[y][x]

    def is_inside(self, x: int, y: int) -> bool:

        return 0 <= x < self.width and 0 <= y < self.height
