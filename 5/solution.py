def get_digit(number, n):
    return number // 10 ** n % 10


class Cpu:
    def __init__(self, ram):
        self.ram = ram
        self.ip = 0
        self.running = True

        self.opcodes = {
            1: self.add,
            2: self.mul,
            3: self.inp,
            4: self.out,
            5: self.jnz,
            6: self.jz,
            7: self.lt,
            8: self.eq,
            99: self.hlt,
        }

    def run(self):
        while self.running:
            ins = self.ram[self.ip]
            opcode = get_digit(ins, 1) * 10 + get_digit(ins, 0)
            mode = [get_digit(ins, x) for x in range(2, 5)]
            self.opcodes[opcode](mode)

    def hlt(self, mode):
        print("HLT")
        self.running = False

    def arg(self, position, mode):
        if mode == 0:
            return self.ram[self.ram[self.ip + position + 1]]
        elif mode == 1:
            return self.ram[self.ip + position + 1]

    def add(self, mode):
        a = self.arg(0, mode[0])
        b = self.arg(1, mode[1])
        dest = self.arg(2, 1)
        print(f"ADD\t{dest} = {a} + {b}")
        self.ram[dest] = a + b
        self.ip += 4

    def mul(self, mode):
        a = self.arg(0, mode[0])
        b = self.arg(1, mode[1])
        dest = self.arg(2, 1)
        print(f"MUL\t{dest} = {a} * {b}")
        self.ram[dest] = a * b
        self.ip += 4

    def inp(self, mode):
        dest = self.arg(0, 1)
        self.ram[dest] = int(input(f"INP\t{dest} = "))
        self.ip += 2

    def out(self, mode):
        a = self.arg(0, mode[0])
        print(f"OUT\t{a}")
        self.ip += 2

    def jnz(self, mode):
        test = self.arg(0, mode[0])
        dest = self.arg(1, mode[1])
        print(f"JNZ\t{test} != 0 => {dest}")
        if test != 0:
            self.ip = dest
        else:
            self.ip += 3

    def jz(self, mode):
        test = self.arg(0, mode[0])
        dest = self.arg(1, mode[1])
        print(f"JZ\t{test} == 0 => {dest}")
        if test == 0:
            self.ip = dest
        else:
            self.ip += 3

    def lt(self, mode):
        a = self.arg(0, mode[0])
        b = self.arg(1, mode[1])
        dest = self.arg(2, 1)
        print(f"LT\t{a} < {b} => {dest}")
        if a < b:
            self.ram[dest] = 1
        else:
            self.ram[dest] = 0
        self.ip += 4

    def eq(self, mode):
        a = self.arg(0, mode[0])
        b = self.arg(1, mode[1])
        dest = self.arg(2, 1)
        print(f"EQ\t{a} == {b} => {dest}")
        if a == b:
            self.ram[dest] = 1
        else:
            self.ram[dest] = 0
        self.ip += 4


if __name__ == "__main__":
    ram = [int(x) for x in open("input.txt", "r").read().split(",")]
    cpu = Cpu(ram)

    print("Enter '1' for Part 1")
    print("Enter '5' for Part 2")
    cpu.run()
