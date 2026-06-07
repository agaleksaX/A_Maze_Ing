import random
import sys
import time
from typing import cast
from config.parser import ConfigParser
from maze.generator import MazeGenerator
from maze.maze import Maze
from maze.solver import MazeSolver
from output.writer import MazeWriter
from visual.renderer import MazeRenderer


def generate_maze(
    width: int,
    height: int,
    seed: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    perfect: bool,
) -> tuple[Maze, str]:
    """Generate a maze and return its shortest solution path."""
    maze = Maze(width, height)

    gen = MazeGenerator(
        maze,
        seed,
        perfect,
    )
    lab = gen.generate()

    solver = MazeSolver(lab, entry, exit_)
    path = solver.solve()

    if not path and entry != exit_:
        raise ValueError("No valid path found from entry to exit")

    return lab, path


def get_random_position(width: int, height: int) -> tuple[int, int]:
    """Return random coordinates inside maze bounds."""
    return (
        random.randint(0, width - 1),
        random.randint(0, height - 1),
    )


def is_forbidden_position(position: tuple[int, int], maze: Maze) -> bool:
    """Check whether position belongs to the closed 42 pattern."""
    return position in maze.pattern_cells


def regenerate_maze(
    width: int,
    height: int,
    seed: int,
    perfect: bool,
) -> tuple[Maze, str, tuple[int, int], tuple[int, int]]:
    """Generate maze with random entry and exit outside 42 pattern."""
    while True:
        entry = get_random_position(width, height)
        exit_ = get_random_position(width, height)

        if entry == exit_:
            continue

        try:
            lab, path = generate_maze(
                width,
                height,
                seed,
                entry,
                exit_,
                perfect,
            )

        except ValueError:
            continue

        if not is_forbidden_position(entry, lab) and not is_forbidden_position(
            exit_,
            lab,
        ):
            return lab, path, entry, exit_


def animate_path(
    lab: Maze,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: str,
    colors: dict[str, str],
    show_pattern: bool,
) -> None:
    """Animate shortest path rendering step by step."""
    partial_path = ""

    for direction in path:
        partial_path += direction
        print("\033c", end="")

        renderer = MazeRenderer(
            lab,
            entry,
            exit_,
            partial_path,
            True,
            colors,
            show_pattern,
        )
        renderer.render()

        time.sleep(0.05)


def animate_generation_and_path(
    width: int,
    height: int,
    seed: int,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    perfect: bool,
    colors: dict[str, str],
    show_pattern: bool,
) -> tuple[Maze, str]:
    """Animate maze generation from scratch and then animate its path."""

    def render_step(current_maze: Maze) -> None:
        print("\033c", end="")

        renderer = MazeRenderer(
            current_maze,
            entry,
            exit_,
            "",
            False,
            colors,
            show_pattern,
        )
        renderer.render()

        time.sleep(0.02)

    maze = Maze(width, height)

    generator = MazeGenerator(
        maze,
        seed,
        perfect,
        render_step,
    )
    lab = generator.generate()

    solver = MazeSolver(lab, entry, exit_)
    path = solver.solve()

    animate_path(
        lab,
        entry,
        exit_,
        path,
        colors,
        show_pattern,
    )

    return lab, path


def write_maze(
    lab: Maze,
    entry: tuple[int, int],
    exit_: tuple[int, int],
    path: str,
    output_file: str,
) -> bool:
    """Write maze to file and report write errors."""
    writer = MazeWriter(lab, entry, exit_, path, output_file)

    try:
        writer.write()

    except OSError as error:
        print(f"Error: cannot write output file: {error}")
        return False

    return True


def load_config(config_file: str) -> dict[str, object] | None:
    """Load configuration and handle parsing errors."""
    try:
        parser = ConfigParser(config_file)
        return parser.parse()

    except (
        FileNotFoundError,
        ValueError,
        OSError,
    ) as error:
        print(f"Error: {error}")
        return None


def main() -> None:
    """Run maze generation and interactive visualization."""
    if len(sys.argv) != 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        return

    config = load_config(sys.argv[1])

    if config is None:
        return

    width = cast(int, config["WIDTH"])
    height = cast(int, config["HEIGHT"])
    seed = cast(int, config["SEED"])
    perfect = cast(bool, config["PERFECT"])
    entry = cast(tuple[int, int], config["ENTRY"])
    exit_ = cast(tuple[int, int], config["EXIT"])
    output_file = cast(str, config["OUTPUT_FILE"])

    show_path = True
    show_pattern = True
    colors = MazeRenderer.generate_colors()

    try:
        lab, path = generate_maze(
            width,
            height,
            seed,
            entry,
            exit_,
            perfect,
        )

    except ValueError as error:
        print(f"Error: {error}")
        return

    if not write_maze(lab, entry, exit_, path, output_file):
        return

    print()
    print("Maze written to", output_file)

    while True:
        renderer = MazeRenderer(
            lab,
            entry,
            exit_,
            path,
            show_path,
            colors,
            show_pattern,
        )
        renderer.render()

        print()
        print("=== A-Maze-ing ===")

        if perfect:
            print("Mode: PERFECT=True")
        else:
            print("Mode: PERFECT=False")

        print("1: Re-generate a new maze")
        print("2: Show/Hide path from entry to exit")
        print("3: Rotate maze colors")
        print("4: Toggle PERFECT mode")
        print("5: Toggle 42 highlight")
        print("6: Animate generation and path")
        print("7: Quit")

        try:
            choice = input("Choice? (1-7): ")

        except EOFError:
            print("\nQuit")
            break

        except KeyboardInterrupt:
            print("\nInterrupted")
            return

        if choice == "1":
            seed += 1
            lab, path, entry, exit_ = regenerate_maze(
                width,
                height,
                seed,
                perfect,
            )

            if not write_maze(lab, entry, exit_, path, output_file):
                continue

            print("New maze generated")

        elif choice == "2":
            show_path = not show_path

        elif choice == "3":
            colors = MazeRenderer.generate_colors()

        elif choice == "4":
            perfect = not perfect
            seed += 1

            lab, path, entry, exit_ = regenerate_maze(
                width,
                height,
                seed,
                perfect,
            )

            if not write_maze(
                lab,
                entry,
                exit_,
                path,
                output_file,
            ):
                continue

            if perfect:
                print("Mode changed: PERFECT=True")
            else:
                print("Mode changed: PERFECT=False")

        elif choice == "5":
            show_pattern = not show_pattern

            if show_pattern:
                print("42 highlight enabled")
            else:
                print("42 highlight disabled")

        elif choice == "6":
            seed += 1

            lab, path = animate_generation_and_path(
                width,
                height,
                seed,
                entry,
                exit_,
                perfect,
                colors,
                show_pattern,
            )

            if not write_maze(
                lab,
                entry,
                exit_,
                path,
                output_file,
            ):
                continue

            print("Generation and path animation completed")

        elif choice == "7":
            print("Quit")
            break

        else:
            print("Invalid choice. " "Please enter 1, 2, 3, 4, 5, 6, or 7.")


if __name__ == "__main__":
    main()
