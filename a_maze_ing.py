import sys
import random
from maze.maze import Maze
from maze.generator import MazeGenerator
from maze.solver import MazeSolver
from output.writer import MazeWriter
from config.parser import ConfigParser
from visual.renderer import MazeRenderer


def generate_maze(
    width: int,
    height: int,
    seed: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
) -> tuple[Maze, str]:
    maze = Maze(width, height)

    gen = MazeGenerator(maze, seed)
    lab = gen.generate()

    solver = MazeSolver(lab, entry, exit_)
    path = solver.solve()

    return lab, path


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
    show_path = True
    colors = MazeRenderer.generate_colors()

    lab, path = generate_maze(
        width,
        height,
        seed,
        entry,
        exit_,
    )
    writer = MazeWriter(lab, entry, exit_, path, output_file)
    writer.write()

    print()
    print("Maze written to", output_file)

    while True:
        renderer = MazeRenderer(lab, entry, exit_, path, show_path, colors)
        renderer.render()

        print()
        print("=== A-Maze-ing ===")
        print("1: Re-generate a new maze")
        print("2: Show/Hide path from entry to exit")
        print("3: Rotate maze colors")
        print("4: Quit")

        choice = input("Choice? (1-4): ")

        if choice == "1":
            seed += 1

            entry = (
                random.randint(0, width - 1),
                random.randint(0, height - 1),
            )

            exit_ = (
                random.randint(0, width - 1),
                random.randint(0, height - 1),
            )

            while entry == exit_:
                exit_ = (
                    random.randint(0, width - 1),
                    random.randint(0, height - 1),
                )

            lab, path = generate_maze(width, height, seed, entry, exit_)
            writer = MazeWriter(lab, entry, exit_, path, output_file)
            writer.write()
            print("New maze generated")

        elif choice == "2":
            show_path = not show_path
        elif choice == "3":
            colors = MazeRenderer.generate_colors()
        elif choice == "4":
            print("Quit")
            break
        else:
            print("Invalid choice. Please enter 1, 2, 3, or 4.")


if __name__ == "__main__":

    main()
