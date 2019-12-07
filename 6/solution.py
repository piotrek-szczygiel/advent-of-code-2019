import sys


class Planet:
    def __init__(self, name, parent, children):
        self.name = name
        self.parent = parent
        self.children = children

    def get_orbits(self, planets):
        count = 0
        parent = self.parent

        while True:
            if parent is None:
                break
            count += 1
            if parent == "COM":
                break
            parent = planets[parent].parent

        return count

    def find(self, planets, caller):
        if self.name == "SAN":
            return 0

        children_cost = sys.maxsize
        children = list(filter(lambda c: c != caller, self.children))
        if len(children) > 0:
            children_cost = 1 + min(
                planets[x].find(planets, self.name) for x in children
            )

        parent_cost = sys.maxsize
        if self.parent is not None and self.parent != caller:
            parent_cost = 1 + planets[self.parent].find(planets, self.name)

        return min(children_cost, parent_cost)


if __name__ == "__main__":
    planets = {}

    for line in open("input.txt", "r").readlines():
        parent, child = line.split(")")
        parent, child = parent.strip(), child.strip()

        if child in planets:
            planets[child].parent = parent
        else:
            planets[child] = Planet(child, parent, [])

        if parent in planets:
            planets[parent].children.append(child)
        else:
            planets[parent] = Planet(parent, None, [child])

    count = 0
    for planet in planets.values():
        count += planet.get_orbits(planets)

    print(f"Part 1: {count}")

    result = planets["YOU"].find(planets, "YOU") - 2
    print(f"Part 2: {result}")
