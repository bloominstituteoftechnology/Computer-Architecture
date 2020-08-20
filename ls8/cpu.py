"""CPU functionality."""

import sys
import time


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        # self.ir = 0b00000000
        # self.mar = 0
        # self.mdr = 0b00000000
        self.fl = 0b000
        self.reg[7] = 0xF4

    def load(self):
        """Load a program into memory."""

        program = []
        if len(sys.argv) == 2:
            try:
                with open(sys.argv[1]) as f:
                    for line in f:
                        line = line.partition('#')[0]
                        line = line.rstrip()

                        if line != '':
                            program.append(int(line, 2))

            except FileNotFoundError as e:
                print('\n', e, '\n')

            for address, instruction in enumerate(program):
                self.ram[address] = instruction
                address += 1
        else:
            return print('\nPlease include a file to load!\n')

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""

        def add():
            self.reg[reg_a] += self.reg[reg_b]

        def sub():
            self.reg[reg_a] -= self.reg[reg_b]

        def mul():
            self.reg[reg_a] *= self.reg[reg_b]

        def div():
            if self.reg[reg_b] == 0:
                self.ram_write(self.ram_read(self.pc+3), 0b00000001)
                return print('Cannot divide by zero!')
            self.reg[reg_a] /= self.reg[reg_b]

        def mod():
            if self.reg[reg_b] == 0:
                self.ram_write(self.ram_read(self.pc+3), 0b00000001)
                return print('Cannot modulo by zero!')
            self.reg[reg_a] %= self.reg[reg_b]

        def inc():
            self.reg[reg_a] += 1

        def dec():
            self.reg[reg_a] -= 1

        def bcmp():
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000001

        def band():
            self.reg[reg_a] &= self.reg[reg_b]

        def bnot():
            self.reg[reg_a] = 0b11111111 - self.reg[reg_a]

        def bor():
            self.reg[reg_a] |= self.reg[reg_b]

        def bxor():
            self.reg[reg_a] ^= self.reg[reg_b]

        def shl():
            self.reg[reg_a] <<= self.reg[reg_b]

        def shr():
            self.reg[reg_a] >>= self.reg[reg_b]

        operations = {
            0b10100000: add,
            0b10100001: sub,
            0b10100010: mul,
            0b10100011: div,
            0b10100100: mod,
            0b01100101: inc,
            0b01100110: dec,
            0b10100111: bcmp,
            0b10101000: band,
            0b01101001: bnot,
            0b10101010: bor,
            0b10101011: bxor,
            0b10101100: shl,
            0b10101101: shr,
        }

        try:
            operations[op]()
        except KeyError:
            print('\nUnsupported ALU operation\n')

    def ldi(self):
        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)

    def ld(self):
        self.reg[self.ram_read(
            self.pc+1)] = self.ram_read(self.reg[self.ram_read(self.pc+2)])

    def st(self):
        self.ram_write(self.reg[self.ram_read(self.pc+1)],
                       self.ram_read(self.pc+2))

    def prn(self):
        print(self.reg[self.ram_read(self.pc+1)])

    def pra(self):
        print(chr(self.reg[self.ram_read(self.pc+1)]), end="")

    def nop(self):
        pass

    def push(self, address=None):
        if address is None:
            self.reg[7] -= 1
            self.ram_write(self.reg[7], self.reg[self.ram_read(self.pc+1)])
        else:
            self.reg[7] -= 1
            self.ram_write(self.reg[7], address)

    def pop(self, ret=False):
        if self.reg[7] == 0xF4:
            return print('Stack is Empty!')

        if ret:
            pc = self.ram_read(self.reg[7])
            self.reg[7] += 1
            return pc

        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def call(self):
        self.push(self.pc+2)
        self.pc = self.reg[self.ram_read(self.pc+1)]

    def jmp(self):
        self.pc = self.reg[self.ram_read(self.pc+1)]

    def jeq(self):
        if self.fl == 0b1:
            self.jmp()
            return True

    def jge(self):
        if self.fl == 0b10 or self.fl == 0b1:
            self.jmp()
            return True

    def jgt(self):
        if self.fl == 0b10:
            self.jmp()
            return True

    def jle(self):
        if self.fl == 0b100 or self.fl == 0b1:
            self.jmp()
            return True

    def jlt(self):
        if self.fl == 0b100:
            self.jmp()
            return True

    def jne(self):
        if self.fl > 0b1 or self.fl == 0b0:
            self.jmp()
            return True

    def ret(self):
        self.pc = self.pop(True)

    def checkAlu(self, instruction):
        if (instruction & 0b00100000) >> 5 == 1:
            val1 = self.ram_read(self.pc+1)
            val2 = self.ram_read(self.pc+2)
            self.alu(instruction, val1, val2)
            return 0b00000000

        return instruction

    def pc_inc_calc(self, instruction):
        if (instruction & 0b00010000) >> 4 != 1:
            return (instruction >> 6) + 1

        return 0

    def run(self):
        """Run the CPU."""

        commands = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000000: self.nop,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b10000011: self.ld,
            0b10000100: self.st,
            0b01001000: self.pra,
            0b01010000: self.call,
            0b00010001: self.ret,
            0b01010010: 'INT',
            0b00010011: 'IRET',
            0b01010100: self.jmp,
            'HALT': 0b00000001,
        }

        conditionals = {
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b01010111: self.jgt,
            0b01011000: self.jlt,
            0b01011001: self.jle,
            0b01011010: self.jge,
        }

        # start = time.time()

        while self.ram_read(self.pc) != commands['HALT'] and self.pc < 255:
            instruction = self.ram_read(self.pc)
            pc_increase = self.pc_inc_calc(instruction)
            instruction = self.checkAlu(instruction)

            # if time.time() - start >= 1:
            #     print("ONE SECOND")
            #     start = time.time()

            if instruction in conditionals:
                if not conditionals[instruction]():
                    self.pc += (instruction >> 6) + 1

            else:
                try:
                    commands[instruction]()
                    self.pc += pc_increase

                except KeyError:
                    return print(f'\nInstruction {instruction} not found at {self.pc}\n')
