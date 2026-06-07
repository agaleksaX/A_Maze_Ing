import os
import tempfile
import unittest

from config.parser import ConfigParser
from maze.generator import MazeGenerator
from maze.maze import Maze
from maze.solver import MazeSolver
from output.writer import MazeWriter


class TestMazeProject(unittest.TestCase):
    def test_maze_size_and_cells(self) -> None:
        maze = Maze(15, 15)

        self.assertEqual(maze.width, 15)
        self.assertEqual(maze.height, 15)
        self.assertTrue(maze.is_inside(14, 14))
        self.assertFalse(maze.is_inside(15, 14))

    def test_generator_creates_pattern(self) -> None:
        maze = Maze(15, 15)
        generator = MazeGenerator(maze, seed=42)

        generator.generate()

        self.assertGreater(len(maze.pattern_cells), 0)

        for x, y in maze.pattern_cells:
            cell = maze.get_cell(x, y)
            self.assertTrue(cell.north)
            self.assertTrue(cell.east)
            self.assertTrue(cell.south)
            self.assertTrue(cell.west)

    def test_solver_finds_path(self) -> None:
        maze = Maze(15, 15)
        generator = MazeGenerator(maze, seed=42)
        generated = generator.generate()

        solver = MazeSolver(generated, (0, 0), (14, 14))
        path = solver.solve()

        self.assertNotEqual(path, "")
        self.assertTrue(set(path).issubset({"N", "E", "S", "W"}))

    def test_writer_creates_output_file(self) -> None:
        maze = Maze(15, 15)
        generator = MazeGenerator(maze, seed=42)
        generated = generator.generate()

        solver = MazeSolver(generated, (0, 0), (14, 14))
        path = solver.solve()

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            output_file = temp_file.name

        try:
            writer = MazeWriter(
                generated,
                (0, 0),
                (14, 14),
                path,
                output_file,
            )
            writer.write()

            with open(output_file, "r", encoding="utf-8") as file:
                content = file.read()

            self.assertIn("0,0", content)
            self.assertIn("14,14", content)
            self.assertIn(path, content)

        finally:
            os.remove(output_file)

    def test_parser_reads_valid_config(self) -> None:
        config_text = (
            "WIDTH=15\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=14,14\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
            "SEED=42\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
        ) as temp_file:
            temp_file.write(config_text)
            config_file = temp_file.name

        try:
            parser = ConfigParser(config_file)
            config = parser.parse()

            self.assertEqual(config["WIDTH"], 15)
            self.assertEqual(config["HEIGHT"], 15)
            self.assertEqual(config["ENTRY"], (0, 0))
            self.assertEqual(config["EXIT"], (14, 14))
            self.assertEqual(config["OUTPUT_FILE"], "maze.txt")
            self.assertEqual(config["PERFECT"], True)
            self.assertEqual(config["SEED"], 42)

        finally:
            os.remove(config_file)

    def test_parser_rejects_invalid_config(self) -> None:
        config_text = (
            "WIDTH=15\n"
            "HEIGHT=15\n"
            "ENTRY=0,0\n"
            "EXIT=0,0\n"
            "OUTPUT_FILE=maze.txt\n"
            "PERFECT=True\n"
        )

        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            delete=False,
        ) as temp_file:
            temp_file.write(config_text)
            config_file = temp_file.name

        try:
            parser = ConfigParser(config_file)

            with self.assertRaises(ValueError):
                parser.parse()

        finally:
            os.remove(config_file)


if __name__ == "__main__":
    unittest.main()
