class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

        self.north: bool = True
        self.east: bool = True
        self.south: bool = True
        self.west: bool = True

        self.visited: bool = False
