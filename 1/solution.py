def fuel1(mass):
    return mass // 3 - 2


def fuel2(mass, acc=0):
    result = mass // 3 - 2
    if result <= 0:
        return acc

    return fuel2(result, acc + result)


def part1(masses):
    return sum([fuel1(mass) for mass in masses])


def part2(masses):
    return sum([fuel2(mass) for mass in masses])


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        content = file.read()

    masses = [int(mass) for mass in content.splitlines()]

    result1 = part1(masses)
    print(f"Part 1: {result1}")

    result2 = part2(masses)
    print(f"Part 2: {result2}")
