import random
from maze.maze import Maze


class MazeRenderer:

    EMPTY = "  "

    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit_: tuple[int, int],
        path: str,
        show_path: bool = True,
        colors: dict[str, str] | None = None,
    ):
        self.maze = maze
        self.entry = entry
        self.exit = exit_
        self.path = path
        self.path_cells = self._build_path()
        self.show_path = show_path
        if colors is None:
            self.colors = self.generate_colors()
        else:
            self.colors = colors

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
                row.append(self._wall())

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
            return self._entry()

        if position == self.exit:
            return self._exit()

        if self.show_path and position in self.path_cells:
            return self._path()

        return self.EMPTY

    def _path_or_empty(
        self,
        current: tuple[int, int],
        neighbor: tuple[int, int],
    ) -> str:
        if (
            self.show_path
            and current in self.path_cells
            and neighbor in self.path_cells
        ):
            return self._path()

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

    @staticmethod
    def generate_colors() -> dict[str, str]:
        colors = [91, 92, 93, 94, 95, 96, 97]

        random.shuffle(colors)

        return {
            "wall": f"\033[{colors[0]}m██\033[0m",
            "entry": f"\033[{colors[1]}m██\033[0m",
            "exit": f"\033[{colors[2]}m██\033[0m",
            "path": f"\033[{colors[3]}m██\033[0m",
        }

    def _wall(self) -> str:
        return self.colors["wall"]

    def _entry(self) -> str:
        return self.colors["entry"]

    def _exit(self) -> str:
        return self.colors["exit"]

    def _path(self) -> str:
        return self.colors["path"]
