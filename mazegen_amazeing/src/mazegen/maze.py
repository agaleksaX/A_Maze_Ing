from mazegen.cell import Cell


class Maze:
    """Represent a maze composed of connected cells."""

    def __init__(self, width: int, height: int) -> None:
        """Initialize maze size, cells, and pattern metadata."""
        self.width = width
        self.height = height
        self.pattern_cells: set[tuple[int, int]] = set()
        self.cells: list[list[Cell]] = self._create_cells()

    def _create_cells(self) -> list[list[Cell]]:
        """Create and initialize maze cells."""
        cells: list[list[Cell]] = []

        for y in range(self.height):
            row: list[Cell] = []

            for x in range(self.width):
                row.append(Cell(x, y))

            cells.append(row)

        return cells

    def get_cell(self, x: int, y: int) -> Cell:
        """Return the cell at given coordinates."""
        return self.cells[y][x]

    def is_inside(self, x: int, y: int) -> bool:
        """Check whether coordinates belong to the maze."""
        return 0 <= x < self.width and 0 <= y < self.height
