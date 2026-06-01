from maze.generator import MazeGenerator
from maze.maze import Maze
from maze.solver import MazeSolver

maze = Maze(4, 4)
gen = MazeGenerator(maze, seed=42)
lab = gen.generate()
solver = MazeSolver(lab, (0, 0), (3, 3))

path = solver.solve()
print(path)
print(len(path))
