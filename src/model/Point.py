class Point:

    def __init__(self, x, y, tick):
        self.x = x
        self.y = y
        self.tick = tick

    def get_coords(self):
        return self.x, self.y

    def get_tick(self):
        return self.tick


    def __str__(self):
        return f"Point(x={self.x}, y={self.y} tick={self.tick})"
 