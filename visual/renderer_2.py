from maze.maze import Maze


class MazeRender:
    WALL = "\033[37m█\033[0m"
    EMPTY = " "
    ENTRY = "\033[35mE\033[0m"
    EXIT = "\033[31mX\033[0m"
    PATH = "\033[90m░\033[0m"

    def __init__(self, maze: Maze, entry, exit_, path):
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

        canvas = []
        for _ in range(height):
            row = []
            for _ in range(width):
                row.append(self.WALL)
            canvas.append(row)

        for y in range(self.maze.height):
            for x in range(self.maze.width):
                cell = self.maze.get_cell(x, y)

                cx = x * 2 + 1
                cy = y * 2 + 1

                if (x, y) == self.entry:
                    canvas[cy][cx] = self.ENTRY
                elif (x, y) == self.exit:
                    canvas[cy][cx] = self.EXIT
                elif (x, y) in self.path_cells:
                    canvas[cy][cx] = self.PATH
                else:
                    canvas[cy][cx] = self.EMPTY

                if not cell.north:
                    if (x, y) in self.path_cells and (x, y - 1) in self.path_cells:
                        canvas[cy - 1][cx] = self.PATH
                    else:
                        canvas[cy - 1][cx] = self.EMPTY

                if not cell.south:
                    if (x, y) in self.path_cells and (x, y + 1) in self.path_cells:
                        canvas[cy + 1][cx] = self.PATH
                    else:
                        canvas[cy + 1][cx] = self.EMPTY

                if not cell.east:
                    if (x, y) in self.path_cells and (x + 1, y) in self.path_cells:
                        canvas[cy][cx + 1] = self.PATH
                    else:
                        canvas[cy][cx + 1] = self.EMPTY

                if not cell.west:
                    if (x, y) in self.path_cells and (x - 1, y) in self.path_cells:
                        canvas[cy][cx - 1] = self.PATH
                    else:
                        canvas[cy][cx - 1] = self.EMPTY

        return canvas

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
