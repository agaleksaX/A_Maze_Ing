from maze.generator import MazeGenerator
from maze.maze import Maze


maze = Maze(4, 4)
gen = MazeGenerator(maze, seed=42)
gen.generate()

visited_count = 0
opened_walls = 0
for row in maze.cells:
    for cell in row:
        if cell.visited:
            visited_count += 1
        if not cell.north:
            opened_walls += 1
        if not cell.west:
            opened_walls += 1
        if not cell.south:
            opened_walls += 1
        if not cell.east:
            opened_walls += 1
            
print(visited_count)
print(opened_walls)