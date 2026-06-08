*This project has been created as part of the 42 curriculum by agaleksa, msaribek.*

# A-Maze-Ing

## Description

A-Maze-Ing is a Python project developed as part of the 42 curriculum.

The goal of this project is to generate valid random mazes, solve them, export them into a hexadecimal format, and provide a visual representation of the generated result.

The project supports:

* Random maze generation
* Deterministic generation using a seed
* Perfect maze generation (single valid path)
* Shortest-path solving
* Hexadecimal export format
* Interactive terminal visualization
* Reusable maze generator package

The maze structure guarantees:

* Full connectivity
* Valid borders
* Consistent walls between neighbouring cells
* No isolated areas
* Optional visible “42” pattern inside the maze

---

# Project Structure

```text
A_Maze_Ing/
├── a_maze_ing.py
├── config.txt
├── README.md
├── requirements.txt
├── Makefile
├── config/
│   └── parser.py
├── maze/
│   ├── cell.py
│   ├── maze.py
│   ├── generator.py
│   └── solver.py
├── output/
│   └── writer.py
├── visual/
├── tests/
└── mazegen_amazeing/
    ├── pyproject.toml
    ├── src/
    └── dist/
```

---

# Instructions

## Installation

Clone repository:

```bash
git clone <repository_url>
cd A_Maze_Ing
```

Install dependencies:

```bash
make install
```

or

```bash
pip install -r requirements.txt
```

---

## Run

Generate maze:

```bash
python3 a_maze_ing.py config.txt
```

or

```bash
make run
```

---

## Debug

```bash
make debug
```

---

## Lint

```bash
make lint
```

Strict mode:

```bash
make lint-strict
```

---

# Configuration File

Example:

```txt
WIDTH=20
HEIGHT=15
SEED=42
ENTRY=0,0
EXIT=19,14
OUTPUT_FILE=maze.txt
PERFECT=True
```

## Parameters

| Key         | Description         |
| ----------- | ------------------- |
| WIDTH       | Maze width          |
| HEIGHT      | Maze height         |
| ENTRY       | Entry coordinates   |
| EXIT        | Exit coordinates    |
| OUTPUT_FILE | Output filename     |
| PERFECT     | Enable perfect maze |
| SEED        | Random seed         |

---

# Output Format

The maze is exported as hexadecimal values.

Wall encoding:

| Bit | Direction |
| --- | --------- |
| 0   | North     |
| 1   | East      |
| 2   | South     |
| 3   | West      |

Example:

```text
A43D
13F2
0AC4

0,0
19,14
SSEENNWW
```

---

# Maze Generation Algorithm

## Recursive Backtracking (Depth First Search)

We selected Recursive Backtracking because it provides:

* Fast generation
* Simple implementation
* Naturally generated corridors
* Easy reproducibility using seeds
* Efficient creation of perfect mazes

Generation process:

1. Select random start cell
2. Mark visited
3. Randomly choose neighbour
4. Remove wall
5. Continue recursively
6. Backtrack when blocked

---

# Visual Representation

The maze supports:

* Terminal rendering
* Path display
* Wall color changes
* Re-generation without restart

Controls:

```text
R → regenerate
P → show/hide path
C → change colors
Q → quit
```

---

# Reusable Module

Maze generation logic is separated into an installable package.

Package:

```text
mazegen_amazeing
```

Example:

```python
from mazegen.generator import MazeGenerator

generator = MazeGenerator(
    width=20,
    height=15,
    seed=42
)

maze = generator.generate()
```

The package exposes:

* Maze structure
* Generator
* Solver
* Solution access

---

# Team & Project Management

## Team Members

### agaleksa

* Core architecture
* Maze generation
* Configuration parser
* Validation

### msaribek

* Visualization
* Packaging
* Testing
* Documentation

---

## Planning

Initial plan:

* Generator
* Solver
* Export
* Visualizer

Final evolution:

* Improved package structure
* Added reusable module
* Added tests
* Added interactive rendering

---

## What Worked Well

* Clear module separation
* Independent testing
* Fast iteration

## What Could Be Improved

* Additional algorithms
* More rendering options
* Better UI customization

---

# Resources

Documentation:

* Python Documentation
* PEP8
* Flake8
* Mypy
* Packaging Guide

Algorithm references:

* Recursive Backtracking
* Graph Theory
* Maze Generation Techniques

AI usage:

AI was used only for:

* Documentation improvements
* Project structure review
* Edge-case discussion
* README refinement

All implementation decisions, debugging, testing, and final validation were completed manually by the team.

---

# Future Improvements

* Multiple algorithms
* Animation
* GUI support
* Export formats
* Real-time generation
