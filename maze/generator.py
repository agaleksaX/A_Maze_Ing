import random
from maze.maze import Maze
from maze.cell import Cell


class MazeGenerator:

    def __init__(self, maze: Maze, seed: int | None = None):
        self.maze = maze
        self.random = random.Random(seed)

    def generate(self) -> Maze:
        start = self.maze.get_cell(0, 0)
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
                stack.pop(-1)

        return self.maze

    def _get_unvisited_neighbors(self, cell: Cell) -> list[tuple[str, Cell]]:

        neighbors: list[tuple[str, Cell]] = []

        nx = cell.x
        ny = cell.y - 1
        if self.maze.is_inside(nx, ny):
            neighbor = self.maze.get_cell(nx, ny)

            if not neighbor.visited:
                neighbors.append(("N", neighbor))

        nx = cell.x + 1
        ny = cell.y
        if self.maze.is_inside(nx, ny):
            neighbor = self.maze.get_cell(nx, ny)

            if not neighbor.visited:
                neighbors.append(("E", neighbor))

        nx = cell.x
        ny = cell.y + 1
        if self.maze.is_inside(nx, ny):
            neighbor = self.maze.get_cell(nx, ny)

            if not neighbor.visited:
                neighbors.append(("S", neighbor))

        nx = cell.x - 1
        ny = cell.y
        if self.maze.is_inside(nx, ny):
            neighbor = self.maze.get_cell(nx, ny)

            if not neighbor.visited:
                neighbors.append(("W", neighbor))

        return neighbors

    def _remove_wall(self, current: Cell, neighbor: Cell, direction: str) -> None:

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
