def machine(noun, verb, memory):
    pc = 0

    memory[1] = noun
    memory[2] = verb

    while True:
        intcode = memory[pc]

        a = memory[pc + 1]
        b = memory[pc + 2]
        dest = memory[pc + 3]

        if intcode == 1:
            memory[dest] = memory[a] + memory[b]
        elif intcode == 2:
            memory[dest] = memory[a] * memory[b]
        elif intcode == 99:
            return memory[0]
        else:
            print(f"Invalid intcode: {intcode}")
            return -1

        pc += 4


def part1(memory):
    return machine(12, 2, memory)


def part2(memory):
    for noun in range(100):
        for verb in range(100):
            result = machine(noun, verb, memory[:])
            if result == 19690720:
                return noun * 100 + verb


if __name__ == "__main__":
    with open("input.txt", "r") as file:
        content = file.read()

    memory = [int(intcode) for intcode in content.split(",")]

    result1 = part1(memory[:])
    print(f"Part 1: {result1}")

    result2 = part2(memory[:])
    print(f"Part 2: {result2}")
