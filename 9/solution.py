def get_digit(number, n):
    return number // 10 ** n % 10


def dummy_print(*values, end="\n"):
    pass


class Cpu:
    RAM_SIZE = 2048  # Minimum 2KB of RAM

    def __init__(self, ram, debug=False):
        self.ram = ram
        self.ram.extend([0 for _ in range(Cpu.RAM_SIZE - len(ram))])

        self.debug = debug
        self.log = print if debug else dummy_print
        self.output = None

        self.ip = 0
        self.bp = 0
        self.running = True

        self.opcodes = {
            1: (self.add, 4),
            2: (self.mul, 4),
            3: (self.inp, 2),
            4: (self.out, 2),
            5: (self.jnz, 3),
            6: (self.jz, 3),
            7: (self.lt, 4),
            8: (self.eq, 4),
            9: (self.abp, 2),
            99: (self.hlt, 1),
        }

    def run(self):
        while self.running:
            ins = self.ram[self.ip]
            opcode = self.opcodes[get_digit(ins, 1) * 10 + get_digit(ins, 0)]
            mode = [get_digit(ins, x) for x in range(2, 5)]
            bytes = self.ram[self.ip : self.ip + opcode[1]]
            self.log(f"{self.ip: <4} {str(bytes): <32}\t{opcode[0].__name__}\t", end="")
            opcode[0](mode)
        return self.output

    def arg(self, position, all_modes, dest=False):
        mode = all_modes[position]
        value = self.ram[self.ip + position + 1]
        if mode == 0:
            if dest:
                return value
            else:
                return self.ram[value]
        elif mode == 1:
            return value
        elif mode == 2:
            if dest:
                return self.bp + value
            else:
                return self.ram[self.bp + value]

    def hlt(self, mode):
        self.running = False
        self.log()

    def add(self, mode):
        a = self.arg(0, mode)
        b = self.arg(1, mode)
        dest = self.arg(2, mode, dest=True)
        self.log(f"{dest} <- {a} + {b} ({a + b})")
        self.ram[dest] = a + b
        self.ip += 4

    def mul(self, mode):
        a = self.arg(0, mode)
        b = self.arg(1, mode)
        dest = self.arg(2, mode, dest=True)
        self.log(f"{dest} <- {a} * {b} ({a * b})")
        self.ram[dest] = a * b
        self.ip += 4

    def inp(self, mode):
        dest = self.arg(0, mode, dest=True)
        if self.debug:
            value = input(f"{dest} <- ")
        else:
            value = input("inp> ")
        self.ram[dest] = int(value)
        self.ip += 2

    def out(self, mode):
        value = self.arg(0, mode)
        if self.debug:
            print(f"-> {value}")
        else:
            print(f"out> {value}")
        self.output = value
        self.ip += 2

    def jnz(self, mode):
        test = self.arg(0, mode)
        jump = self.arg(1, mode)
        self.log(f"{test} != 0 -> {jump}")
        if test != 0:
            self.ip = jump
        else:
            self.ip += 3

    def jz(self, mode):
        test = self.arg(0, mode)
        jump = self.arg(1, mode)
        self.log(f"{test} == 0 -> {jump}")
        if test == 0:
            self.ip = jump
        else:
            self.ip += 3

    def lt(self, mode):
        a = self.arg(0, mode)
        b = self.arg(1, mode)
        dest = self.arg(2, mode, dest=True)
        self.log(f"{dest} <- {a} < {b}")
        if a < b:
            self.ram[dest] = 1
        else:
            self.ram[dest] = 0
        self.ip += 4

    def eq(self, mode):
        a = self.arg(0, mode)
        b = self.arg(1, mode)
        dest = self.arg(2, mode, dest=True)
        self.log(f"{dest} <- {a} == {b}")
        if a == b:
            self.ram[dest] = 1
        else:
            self.ram[dest] = 0
        self.ip += 4

    def abp(self, mode):
        offset = self.arg(0, mode)
        self.log(f"{offset} -> {self.bp + offset}")
        self.bp += offset
        self.ip += 2


if __name__ == "__main__":
    print("Enter '1' for first part or '2' for second part")
    print()
    ram = [int(x) for x in open("input.txt").read().split(",")]
    Cpu(ram).run()
