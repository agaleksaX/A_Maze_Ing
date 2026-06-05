import sys
from maze.maze import Maze
from maze.generator import MazeGenerator
from maze.solver import MazeSolver
from output.writer import MazeWriter
from config.parser import ConfigParser


def main() -> None:
    
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config_file = sys.argv[1]

    parser = ConfigParser(config_file)
    config = parser.parse()
    width = config["WIDTH"]
    height = config["HEIGHT"]
    seed = config["SEED"]
    entry = config["ENTRY"]
    exit_ = config["EXIT"]
    output_file = config["OUTPUT_FILE"]
    
    maze = Maze(width, height)
    gen = MazeGenerator(maze, seed)
    lab = gen.generate()
    solver = MazeSolver(lab, entry, exit_)
    path = solver.solve()
    writer = MazeWriter(lab, entry, exit_, path, output_file)
    writer.write()
    print("Maze written to", output_file)


if __name__ == "__main__":
    
    main()
