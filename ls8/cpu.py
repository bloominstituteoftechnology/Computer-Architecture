import sys

class CPU:
    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.isRunning = True
        self.instruction_set = {
            0b00000001: self.hlt,
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b10100010: self.mul,
            0b01000110: self.pop,
            0b01000101: self.push,
            0b01010000: self.call,
            0b00010001: self.ret,
            0b10100000: self.add

        }

    def ram_write(self, val, addy):
        self.ram[addy] = val

    def ram_read(self, addy):
        return self.ram[addy]


    def load(self, program):
        address = 0
        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        if op == "ADD":
            self.reg[reg_a] = 255 & (self.reg[reg_a] + self.reg[reg_b])
        elif op == "MUL":
            self.reg[reg_a] = 255 & (self.reg[reg_a] * self.reg[reg_b])
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        while self.isRunning:
            if self.ram_read(self.pc) not in self.instruction_set:
                print("We found something out of the ordinary!")
                print("{0:b}".format(self.ram_read(self.pc)))
                print(self.ram_read(self.pc))
                return 1
            self.instruction_set[self.ram_read(self.pc)]()

    def ldi(self):
        reg_a = self.ram_read(self.pc + 1)
        int = self.ram_read(self.pc + 2)
        self.reg[reg_a] = 255 & int
        self.pc += 3

    def add(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def mul(self):
        reg_a = self.ram_read(self.pc + 1)
        reg_b = self.ram_read(self.pc + 2)
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3

    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2

    def hlt(self):
        self.isRunning = False

    def pop(self):
        self.reg[self.ram_read(self.pc + 1)] = self.ram_read(self.reg[7])
        self.reg[7] += 1
        self.pc += 2

    def push(self):
        self.reg[7] -= 1
        self.ram[self.reg[7]] = self.reg[self.ram_read(self.pc + 1)]
        self.pc += 2

    def call(self):
        sub_add = self.reg[self.ram_read(self.pc + 1)]
        ret_add = self.pc + 2
        while self.ram_read(ret_add) not in self.instruction_set:
            ret_add += 1
        self.reg[7] -= 1
        self.ram[self.reg[7]] = ret_add
        self.pc = sub_add

    def ret(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1