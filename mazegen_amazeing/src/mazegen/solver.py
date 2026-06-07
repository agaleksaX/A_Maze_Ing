from mazegen.cell import Cell
from mazegen.maze import Maze


class MazeSolver:
    """Find shortest path inside a maze."""

    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit_: tuple[int, int],
    ) -> None:
        """Initialize solver with maze and target coordinates."""
        self.maze = maze
        self.entry = entry
        self.exit = exit_

    def solve(self) -> str:
        """Compute shortest path from entry to exit."""
        queue: list[tuple[int, int]] = [self.entry]
        visited: set[tuple[int, int]] = {self.entry}
        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}

        while queue:
            current = queue.pop(0)

            if current == self.exit:
                return self._restore_path(parent, self.exit)

            x, y = current
            current_cell = self.maze.get_cell(x, y)
            neighbors = self._get_neighbors(current_cell)

            for direction, neighbor in neighbors:
                neighbor_position = (neighbor.x, neighbor.y)

                if neighbor_position not in visited:
                    visited.add(neighbor_position)
                    parent[neighbor_position] = (current, direction)
                    queue.append(neighbor_position)

        return ""

    def _get_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:
        """Return reachable neighboring cells."""
        result: list[tuple[str, Cell]] = []

        if not cell.north:
            self._append_if_inside(result, "N", cell.x, cell.y - 1)

        if not cell.south:
            self._append_if_inside(result, "S", cell.x, cell.y + 1)

        if not cell.west:
            self._append_if_inside(result, "W", cell.x - 1, cell.y)

        if not cell.east:
            self._append_if_inside(result, "E", cell.x + 1, cell.y)

        return result

    def _append_if_inside(
        self,
        result: list[tuple[str, Cell]],
        direction: str,
        x: int,
        y: int,
    ) -> None:
        """Append neighbor to result if coordinates are inside maze."""
        if self.maze.is_inside(x, y):
            result.append((direction, self.maze.get_cell(x, y)))

    def _restore_path(
        self,
        parent: dict[tuple[int, int], tuple[tuple[int, int], str]],
        end_position: tuple[int, int],
    ) -> str:
        """Restore path directions from parent mapping."""
        path: list[str] = []
        current = end_position

        while current != self.entry:
            previous, direction = parent[current]
            path.append(direction)
            current = previous

        path.reverse()
        return "".join(path)
