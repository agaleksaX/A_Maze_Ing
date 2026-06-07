import random
from collections.abc import Callable

from maze.cell import Cell
from maze.maze import Maze


class MazeGenerator:
    """Generate random maze structures."""

    def __init__(
        self,
        maze: Maze,
        seed: int | None = None,
        perfect: bool = True,
        on_step: Callable[[Maze], None] | None = None,
    ) -> None:
        """Initialize maze generator."""
        self.maze = maze
        self.random = random.Random(seed)
        self.perfect = perfect
        self.on_step = on_step
        self.pattern_cells: set[tuple[int, int]] = set()

    def generate(self) -> Maze:
        """Generate and return a maze."""
        self._apply_42_pattern()

        if self.perfect:
            self._generate_dfs()
        else:
            self._generate_prim()
            self._open_extra_walls()

        return self.maze

    def _generate_dfs(self) -> None:
        """Generate perfect maze using depth-first search."""
        start = self.maze.get_cell(0, 0)

        if self._is_pattern_cell(start.x, start.y):
            start = self._find_start_cell()

        start.visited = True
        self._notify_step()

        stack: list[Cell] = [start]

        while stack:
            current = stack[-1]
            neighbors = self._get_unvisited_neighbors(current)

            if neighbors:
                direction, neighbor = self.random.choice(neighbors)
                self._remove_wall(current, neighbor, direction)

                neighbor.visited = True
                self._notify_step()

                stack.append(neighbor)

            else:
                stack.pop()

    def _generate_prim(self) -> None:
        """Generate maze using randomized Prim algorithm."""
        start = self._find_start_cell()
        start.visited = True
        self._notify_step()

        frontier = self._get_unvisited_neighbors(start)

        while frontier:
            index = self.random.randrange(len(frontier))
            _, cell = frontier.pop(index)

            if cell.visited:
                continue

            visited_neighbors = self._get_visited_neighbors(cell)

            if not visited_neighbors:
                continue

            direction, neighbor = self.random.choice(visited_neighbors)

            self._remove_wall(
                cell,
                neighbor,
                direction,
            )

            cell.visited = True
            self._notify_step()

            frontier.extend(self._get_unvisited_neighbors(cell))

    def _open_extra_walls(self) -> None:
        """Open some extra walls to make the maze non-perfect."""
        candidates = self._get_closed_internal_walls()

        if not candidates:
            return

        extra_count = max(1, len(candidates) // 10)
        self.random.shuffle(candidates)

        for current, neighbor, direction in candidates[:extra_count]:
            self._remove_wall(current, neighbor, direction)
            self._notify_step()

    def _get_closed_internal_walls(self) -> list[tuple[Cell, Cell, str]]:
        """Return closed walls between normal neighboring cells."""
        walls: list[tuple[Cell, Cell, str]] = []

        for row in self.maze.cells:
            for cell in row:
                if self._is_pattern_cell(cell.x, cell.y):
                    continue

                self._add_closed_wall(
                    walls,
                    cell,
                    "E",
                    cell.x + 1,
                    cell.y,
                )
                self._add_closed_wall(
                    walls,
                    cell,
                    "S",
                    cell.x,
                    cell.y + 1,
                )

        return walls

    def _add_closed_wall(
        self,
        walls: list[tuple[Cell, Cell, str]],
        cell: Cell,
        direction: str,
        x: int,
        y: int,
    ) -> None:
        """Add closed wall candidate if neighbor is valid."""
        if not self.maze.is_inside(x, y):
            return

        if self._is_pattern_cell(x, y):
            return

        neighbor = self.maze.get_cell(x, y)

        if direction == "E" and cell.east and neighbor.west:
            walls.append((cell, neighbor, direction))

        if direction == "S" and cell.south and neighbor.north:
            walls.append((cell, neighbor, direction))

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

        for direction, x, y in self._neighbor_positions(cell):
            if not self.maze.is_inside(x, y):
                continue

            if self._is_pattern_cell(x, y):
                continue

            neighbor = self.maze.get_cell(x, y)

            if not neighbor.visited:
                neighbors.append((direction, neighbor))

        return neighbors

    def _get_visited_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        """Return all visited neighboring cells."""
        neighbors: list[tuple[str, Cell]] = []

        for direction, x, y in self._neighbor_positions(cell):
            if not self.maze.is_inside(x, y):
                continue

            if self._is_pattern_cell(x, y):
                continue

            neighbor = self.maze.get_cell(x, y)

            if neighbor.visited:
                neighbors.append((direction, neighbor))

        return neighbors

    def _neighbor_positions(self, cell: Cell) -> list[tuple[str, int, int]]:
        """Return neighboring coordinates around a cell."""
        return [
            ("N", cell.x, cell.y - 1),
            ("E", cell.x + 1, cell.y),
            ("S", cell.x, cell.y + 1),
            ("W", cell.x - 1, cell.y),
        ]

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
            # 4
            (0, 0),
            (0, 1),
            (0, 2),
            (1, 2),
            (2, 0),
            (2, 1),
            (2, 2),
            (2, 3),
            (2, 4),
            # 2
            (4, 0),
            (5, 0),
            (6, 0),
            (6, 1),
            (4, 2),
            (5, 2),
            (6, 2),
            (4, 3),
            (4, 4),
            (5, 4),
            (6, 4),
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

    def _notify_step(self) -> None:
        """Call animation callback after generation step."""
        if self.on_step is not None:
            self.on_step(self.maze)
