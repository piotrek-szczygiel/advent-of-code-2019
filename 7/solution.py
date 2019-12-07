import itertools
import threading


def get_digit(number, n):
    return number // 10 ** n % 10


class Pipe:
    def __init__(self, inp, inp_cond, out, out_cond):
        self.inp = inp
        self.inp_cond = inp_cond
        self.out = out
        self.out_cond = out_cond


class Cpu(threading.Thread):
    def __init__(self, id, ram, pipe):
        threading.Thread.__init__(self)

        self.id = id
        self.ram = ram
        self.pipe = pipe

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
        self.ram[dest] = a + b
        self.ip += 4

    def mul(self, mode):
        a = self.arg(0, mode[0])
        b = self.arg(1, mode[1])
        dest = self.arg(2, 1)
        self.ram[dest] = a * b
        self.ip += 4

    def inp(self, mode):
        dest = self.arg(0, 1)
        while not self.pipe.inp:
            with self.pipe.inp_cond:
                self.pipe.inp_cond.wait()
        value = self.pipe.inp.pop(0)
        self.ram[dest] = value
        self.ip += 2

    def out(self, mode):
        value = self.arg(0, mode[0])
        self.pipe.out.append(value)
        with self.pipe.out_cond:
            self.pipe.out_cond.notify()
        self.ip += 2

    def jnz(self, mode):
        test = self.arg(0, mode[0])
        dest = self.arg(1, mode[1])
        if test != 0:
            self.ip = dest
        else:
            self.ip += 3

    def jz(self, mode):
        test = self.arg(0, mode[0])
        dest = self.arg(1, mode[1])
        if test == 0:
            self.ip = dest
        else:
            self.ip += 3

    def lt(self, mode):
        a = self.arg(0, mode[0])
        b = self.arg(1, mode[1])
        dest = self.arg(2, 1)
        self.ram[dest] = 1 if a < b else 0
        self.ip += 4

    def eq(self, mode):
        a = self.arg(0, mode[0])
        b = self.arg(1, mode[1])
        dest = self.arg(2, 1)
        self.ram[dest] = 1 if a == b else 0
        self.ip += 4


def maximize_signal(ram, base_phases):
    max_result = 0
    for phases in list(itertools.permutations(base_phases)):
        queues = [[p] for p in phases]
        conds = [threading.Condition() for _ in phases]
        pipes = [
            Pipe(queues[i], conds[i], queues[(i + 1) % 5], conds[(i + 1) % 5])
            for i in range(5)
        ]
        pipes[0].inp.append(0)

        amps = []
        for i in range(5):
            amps.append(Cpu(i, ram[:], pipes[i]))
        for a in amps:
            a.start()
        for a in amps:
            a.join()

        max_result = max(pipes[4].out.pop(), max_result)

    return max_result


if __name__ == "__main__":
    ram = [int(x) for x in open("input.txt", "r").read().split(",")]

    result1 = maximize_signal(ram, [0, 1, 2, 3, 4])
    print(f"Part 1: {result1}")

    result2 = maximize_signal(ram, [5, 6, 7, 8, 9])
    print(f"Part 2: {result2}")
