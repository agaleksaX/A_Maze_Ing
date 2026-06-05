from maze.maze import Maze


class MazeRenderer:
    WALL = "\033[96m██\033[0m"   # bright cyan
    EMPTY = "  "
    ENTRY = "\033[92m██\033[0m"  # bright green
    EXIT = "\033[91m██\033[0m"   # bright red
    PATH = "\033[93m██\033[0m"   # bright yellow

    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        path: str,
    ):
        self.maze = maze
        self.entry = entry
        self.exit = exit_
        self.path = path
        self.path_cells = self._build_path()

    def render(self) -> None:
        canvas = self._build_canvas()

        for row in canvas:
            print("".join(row))

    def _build_canvas(self) -> list[list[str]]:
        height = self.maze.height * 2 + 1
        width = self.maze.width * 2 + 1

        canvas = self._create_canvas(height, width)

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                self._draw_cell(canvas, x, y)

        return canvas

    def _create_canvas(self, height: int, width: int) -> list[list[str]]:
        canvas = []

        for _ in range(height):
            row = []

            for _ in range(width):
                row.append(self.WALL)

            canvas.append(row)

        return canvas

    def _draw_cell(self, canvas: list[list[str]], x: int, y: int) -> None:
        cell = self.maze.get_cell(x, y)

        cx = x * 2 + 1
        cy = y * 2 + 1
        current = (x, y)

        canvas[cy][cx] = self._cell_symbol(current)

        if not cell.north:
            neighbor = (x, y - 1)
            canvas[cy - 1][cx] = self._path_or_empty(current, neighbor)

        if not cell.south:
            neighbor = (x, y + 1)
            canvas[cy + 1][cx] = self._path_or_empty(current, neighbor)

        if not cell.east:
            neighbor = (x + 1, y)
            canvas[cy][cx + 1] = self._path_or_empty(current, neighbor)

        if not cell.west:
            neighbor = (x - 1, y)
            canvas[cy][cx - 1] = self._path_or_empty(current, neighbor)

    def _cell_symbol(self, position: tuple[int, int]) -> str:
        if position == self.entry:
            return self.ENTRY

        if position == self.exit:
            return self.EXIT

        if position in self.path_cells:
            return self.PATH

        return self.EMPTY

    def _path_or_empty(
        self,
        current: tuple[int, int],
        neighbor: tuple[int, int],
    ) -> str:
        if current in self.path_cells and neighbor in self.path_cells:
            return self.PATH

        return self.EMPTY

    def _build_path(self) -> set[tuple[int, int]]:
        x, y = self.entry
        path_cells = {(x, y)}

        for direction in self.path:
            if direction == "N":
                y -= 1
            elif direction == "S":
                y += 1
            elif direction == "E":
                x += 1
            elif direction == "W":
                x -= 1

            path_cells.add((x, y))

        return path_cells
