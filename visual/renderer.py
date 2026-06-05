from maze import maze


def render(maze):
    # print("▗▄▄▄▖")
    # print("▐\033[31m█\033[0m\033[35m█\033[0m\033[32m█\033[0m▌")
    # print("▝▀▀▀▘")
    # print("                   ")
    # print("  ███████████████  ")
    # print("  █\033[31m███\033[0m██\033[35m███\033[0m██\033[32m███\033[0m█  ")
    # print("  █\033[31m███\033[0m██\033[35m███\033[0m██\033[32m███\033[0m█  ")
    # print("  ███████████████  ")
    # print("                   ")
    square = "█"
    color_empty = "\033[30m"  # black
    color_wall = "\033[37m"  # white
    color_cell = "\033[34m"  # blue
    color_esc = "\033[0m"

    for y in range(-1, maze.height + 1):
        if y == -1 or y == maze.height:
            print(f"{color_empty}{square}", end="")
            for i in range(maze.width):
                print(f"{square}{square}{square}{square}{square}", end="")
            print(f"{square}{color_esc}")
            continue
        for i in range(4):
            for x in range(-1, maze.width + 1):
                if x == -1 or x == maze.width:
                    print(f"{color_empty}{square}{color_esc}", end="")
                    continue
                c = maze.cells[y][x]
                if i == 0:
                    if c.east:
                        print(f"{color_wall}{square}{color_esc}", end="")
                    else:
                        print(f"{color_empty}{square}{color_esc}", end="")
                    if c.north:
                        print(
                            f"{color_wall}{square}{square}{square}{color_esc}", end=""
                        )
                    else:
                        print(
                            f"{color_empty}{square}{square}{square}{color_esc}", end=""
                        )
                    if c.west:
                        print(f"{color_wall}{square}{color_esc}", end="")
                    else:
                        print(f"{color_empty}{square}{color_esc}", end="")
                elif i == 1 or i == 2:
                    if c.east:
                        print(f"{color_wall}{square}{color_esc}", end="")
                    else:
                        print(f"{color_empty}{square}{color_esc}", end="")
                    if False:  # check if its unmuvable or no
                        print(
                            f"{color_cell}{square}{square}{square}{color_esc}", end=""
                        )
                    else:
                        print(
                            f"{color_empty}{square}{square}{square}{color_esc}", end=""
                        )
                    if c.west:
                        print(f"{color_wall}{square}{color_esc}", end="")
                    else:
                        print(f"{color_empty}{square}{color_esc}", end="")
                elif i == 3:
                    if c.east:
                        print(f"{color_wall}{square}{color_esc}", end="")
                    else:
                        print(f"{color_empty}{square}{color_esc}", end="")
                    if c.south:
                        print(
                            f"{color_wall}{square}{square}{square}{color_esc}", end=""
                        )
                    else:
                        print(
                            f"{color_empty}{square}{square}{square}{color_esc}", end=""
                        )
                    if c.west:
                        print(f"{color_wall}{square}{color_esc}", end="")
                    else:
                        print(f"{color_empty}{square}{color_esc}", end="")
            print("")
