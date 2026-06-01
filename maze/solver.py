from maze.maze import Maze
from maze.cell import Cell


class MazeSolver:

    def __init__(self, maze: Maze, entry: tuple[int, int], exit: tuple[int, int]):
        self.maze = maze
        self.entry = entry
        self.exit = exit

    def solve(self) -> str:
        start = self.entry
        end = self.exit
        queue: list[tuple[int, int]] = [start]
        visited: set[tuple[int, int]] = {start}
        parent: dict[tuple[int, int], tuple[tuple[int, int], str]] = {}
        while queue:
            current = queue.pop(0)

            if current == end:
                return self._restore_path(parent, end)
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

        result = []

        if not cell.north:
            x = cell.x
            y = cell.y - 1
            if self.maze.is_inside(x, y):
                result.append(("N", self.maze.get_cell(x, y)))

        if not cell.south:
            x = cell.x
            y = cell.y + 1
            if self.maze.is_inside(x, y):
                result.append(("S", self.maze.get_cell(x, y)))

        if not cell.west:
            x = cell.x - 1
            y = cell.y
            if self.maze.is_inside(x, y):
                result.append(("W", self.maze.get_cell(x, y)))

        if not cell.east:
            x = cell.x + 1
            y = cell.y
            if self.maze.is_inside(x, y):
                result.append(("E", self.maze.get_cell(x, y)))

        return result

    def _restore_path(
        self,
        parent: dict[tuple[int, int], tuple[tuple[int, int], str]],
        end_position: tuple[int, int],
    ) -> str:

        path: list[str] = []
        current = end_position

        while current != self.entry:

            previous, direction = parent[current]
            path.append(direction)
            current = previous

        path.reverse()
        htap = "".join(path)

        return htap
