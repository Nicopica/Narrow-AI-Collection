from math import sqrt


class Location:
    def __init__(self, id_loc, x, y):
        self.id_loc = id_loc
        self.x = x
        self.y = y

    def distance_to(self, dest):
        a = (self.x - dest.x) ** 2
        b = (self.y - dest.y) ** 2
        c = int(sqrt(a + b) + 0.5)
        return c

    def __eq__(self, other):
        if isinstance(other, Location):
            return self.id_loc == other.id_loc
        return False

    def __hash__(self):
        return hash(self.id_loc)

    def __str__(self):
        return f"Id: {self.id_loc} at {self.x}, {self.y}"
