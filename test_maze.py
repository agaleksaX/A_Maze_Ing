from maze.maze import Maze


maze = Maze(4, 3)

print(maze.width)
print(maze.height)
print(maze.get_cell(2, 1).x)
print(maze.get_cell(2, 1).y)
print(maze.is_inside(3, 2))
print(maze.is_inside(4, 2))
