class Wire:
    def __init__(self, definition):
        self.movements = [(chunk[0], int(chunk[1:])) for chunk in definition.split(",")]

    def get_path(self):
        path = {}
        x, y, cost = 0, 0, 0
        for (movement, length) in self.movements:
            for _ in range(length):
                if movement == "U":
                    y += 1
                elif movement == "D":
                    y -= 1
                elif movement == "L":
                    x -= 1
                elif movement == "R":
                    x += 1

                cost += 1
                path[(x, y)] = cost

        return path


def part1(wire_a, wire_b):
    path_a = wire_a.get_path()
    path_b = wire_b.get_path()
    intersections = set(path_a.keys()) & set(path_b.keys())
    return min([abs(x) + abs(y) for (x, y) in intersections])


def part2(wire_a, wire_b):
    path_a = wire_a.get_path()
    path_b = wire_b.get_path()
    intersections = set(path_a.keys()) & set(path_b.keys())
    return min(path_a[i] + path_b[i] for i in intersections)


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        contents = file.readlines()

    wire_a = Wire(contents[0])
    wire_b = Wire(contents[1])

    result1 = part1(wire_a, wire_b)
    print(f"Part 1: {result1}")

    result2 = part2(wire_a, wire_b)
    print(f"Part 2: {result2}")
