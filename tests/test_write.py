from maze.generator import MazeGenerator
from maze.maze import Maze
from maze.solver import MazeSolver
from output.writer import MazeWriter

maze = Maze(10, 10)
gen = MazeGenerator(maze, seed=42)
lab = gen.generate()
solver = MazeSolver(lab, (0, 0), (9, 9))

path = solver.solve()

write = MazeWriter(lab, (0, 0), (9, 9), path, "output_file.txt")

write.write()

with open("output_file.txt", "r", encoding="utf-8") as file:
    print(file.read())
    