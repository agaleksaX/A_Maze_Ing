from config.parser import ConfigParser
from maze.generator import MazeGenerator
from maze.maze import Maze
from maze.solver import MazeSolver
from output.writer import MazeWriter

parser = ConfigParser("config.txt")
config = parser.parse()

maze = Maze(config["WIDTH"], config["HEIGHT"])

gen = MazeGenerator(maze, seed=config["SEED"])
lab = gen.generate()

solver = MazeSolver(lab, config["ENTRY"], config["EXIT"])
path = solver.solve()

writer = MazeWriter(
    lab,
    config["ENTRY"],
    config["EXIT"],
    path,
    config["OUTPUT_FILE"],
)

writer.write()

with open(config["OUTPUT_FILE"], "r", encoding="utf-8") as file:
    print(file.read())
