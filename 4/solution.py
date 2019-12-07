with open("input.txt", "r") as file:
    content = file.read().split("-")

start = int(content[0])
end = int(content[1])


def part1():
    counter = 0
    for pin in range(start, end + 1):
        pin = str(pin)
        invalid = False
        double = False

        for i in range(len(pin) - 1):
            if pin[i] > pin[i + 1]:
                invalid = True
                break
            if pin[i] == pin[i + 1]:
                double = True

        if double and not invalid:
            counter += 1

    return counter


def part2():
    counter = 0
    for pin in range(start, end + 1):
        pin = str(pin)
        invalid = False
        double = False
        count = [0 for _ in range(10)]

        for i in range(len(pin) - 1):
            if pin[i] > pin[i + 1]:
                invalid = True
                break

        for c in pin:
            count[int(c)] += 1

        for c in count:
            if c == 2:
                double = True
                break

        if double and not invalid:
            counter += 1

    return counter


print(f"Part 1: {part1()}")
print(f"Part 2: {part2()}")
