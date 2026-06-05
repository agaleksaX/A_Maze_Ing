from maze.maze import Maze
from maze.cell import Cell


class MazeWriter:

    def __init__(
        self,
        maze: Maze,
        entry: tuple[int, int],
        exit: tuple[int, int],
        path: str,
        output_file: str,
    ) -> None:
        self.maze = maze
        self.entry = entry
        self.exit = exit
        self.path = path
        self.output_file = output_file

    def write(self) -> None:

        lines = self._maze_to_lines()
        with open(self.output_file, "w", encoding="utf-8") as file:
            for line in lines:
                file.write(line + "\n")

            file.write("\n")

            x, y = self.entry
            file.write(f"{x},{y}\n")

            x, y = self.exit
            file.write(f"{x},{y}\n")

            file.write(self.path + "\n")

    def _cell_to_hex(self, cell: Cell) -> str:

        value = 0
        digits = "0123456789ABCDEF"

        if cell.north:
            value += 1

        if cell.east:
            value += 2

        if cell.south:
            value += 4

        if cell.west:
            value += 8

        return digits[value]

    def _maze_to_lines(self) -> list[str]:

        lines = []
        for row in self.maze.cells:
            line = ""
            for cell in row:
                hex_digit = self._cell_to_hex(cell)
                line += hex_digit

            lines.append(line)
        return lines
