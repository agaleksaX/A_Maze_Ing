import random

from mazegen.cell import Cell
from mazegen.maze import Maze


class MazeGenerator:
    """Generate random perfect maze structures."""

    def __init__(self, maze: Maze, seed: int | None = None) -> None:
        """Initialize generator with maze object and optional seed."""
        self.maze = maze
        self.random = random.Random(seed)
        self.pattern_cells: set[tuple[int, int]] = set()

    def generate(self) -> Maze:
        """Generate and return a maze."""
        self._apply_42_pattern()
        start = self.maze.get_cell(0, 0)

        if (start.x, start.y) in self.pattern_cells:
            start = self._find_start_cell()

        start.visited = True
        stack: list[Cell] = [start]

        while stack:
            current = stack[-1]
            neighbors = self._get_unvisited_neighbors(current)

            if neighbors:
                direction, neighbor = self.random.choice(neighbors)
                self._remove_wall(current, neighbor, direction)
                neighbor.visited = True
                stack.append(neighbor)
            else:
                stack.pop()

        return self.maze

    def _find_start_cell(self) -> Cell:
        """Return first non-pattern cell as generation start."""
        for row in self.maze.cells:
            for cell in row:
                if not self._is_pattern_cell(cell.x, cell.y):
                    return cell

        raise ValueError("No valid cell available for maze generation")

    def _get_unvisited_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        """Return all unvisited neighboring cells."""
        neighbors: list[tuple[str, Cell]] = []
        directions = [
            ("N", cell.x, cell.y - 1),
            ("E", cell.x + 1, cell.y),
            ("S", cell.x, cell.y + 1),
            ("W", cell.x - 1, cell.y),
        ]

        for direction, nx, ny in directions:
            if not self.maze.is_inside(nx, ny):
                continue

            if self._is_pattern_cell(nx, ny):
                continue

            neighbor = self.maze.get_cell(nx, ny)

            if not neighbor.visited:
                neighbors.append((direction, neighbor))

        return neighbors

    def _remove_wall(
        self,
        current: Cell,
        neighbor: Cell,
        direction: str,
    ) -> None:
        """Open passage between neighboring cells."""
        if direction == "N":
            current.north = False
            neighbor.south = False
        elif direction == "E":
            current.east = False
            neighbor.west = False
        elif direction == "S":
            current.south = False
            neighbor.north = False
        elif direction == "W":
            current.west = False
            neighbor.east = False

    def _apply_42_pattern(self) -> None:
        """Create fully closed cells forming visible 42 pattern."""
        if self.maze.width < 10 or self.maze.height < 7:
            print("Warning: maze is too small to draw 42 pattern")
            self.pattern_cells = set()
            self.maze.pattern_cells = set()
            return

        self.pattern_cells = self._build_42_pattern()
        self.maze.pattern_cells = self.pattern_cells

        for x, y in self.pattern_cells:
            cell = self.maze.get_cell(x, y)
            cell.north = True
            cell.east = True
            cell.south = True
            cell.west = True
            cell.visited = True

    def _build_42_pattern(self) -> set[tuple[int, int]]:
        """Return centered coordinates used to draw the 42 pattern."""
        shape = {
            (0, 0), (0, 1), (0, 2),
            (1, 2),
            (2, 0), (2, 1), (2, 2), (2, 3), (2, 4),
            (4, 0), (5, 0), (6, 0),
            (6, 1),
            (4, 2), (5, 2), (6, 2),
            (4, 3),
            (4, 4), (5, 4), (6, 4),
        }
        pattern_width = 7
        pattern_height = 5
        start_x = (self.maze.width - pattern_width) // 2
        start_y = (self.maze.height - pattern_height) // 2
        result: set[tuple[int, int]] = set()

        for x, y in shape:
            result.add((start_x + x, start_y + y))

        return result

    def _is_pattern_cell(self, x: int, y: int) -> bool:
        """Check whether coordinates belong to the 42 pattern."""
        return (x, y) in self.pattern_cells
