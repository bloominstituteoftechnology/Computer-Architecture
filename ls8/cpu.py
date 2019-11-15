"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


SP = 7  # register used for stack pointer


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0
        self.ram = [0] * 256
        self.branchtable = {
            HLT: self.handle_hlt,
            LDI: self.handle_ldi,
            PRN: self.handle_prn,
            MUL: self.handle_mul,
            ADD: self.handle_add,
            CMP: self.handle_cmp,
            POP: self.handle_pop,
            PUSH: self.handle_push,
            CALL: self.handle_call,
            RET: self.handle_ret,
            JMP: self.handle_jmp,
            JEQ: self.handle_jeq,
            JNE: self.handle_jne,
        }

        self.reg[SP] = 0xf4
        self.halted = False

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: comp.py [filename]")
            sys.exit(1)

        progname = sys.argv[1]

        address = 0

        # For now, we've just hardcoded a program:

        with open(progname) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == "":
                    continue

                val = int(line, 2)
                # print(val)

                self.ram[address] = val
                address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] > self.reg[reg_b]:
                self.fl = 0b00000010
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = 0b00000100
            if self.reg[reg_a] == self.reg[reg_b]:
                self.fl = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

        # print(self.reg[reg_a])

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def handle_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        # print(f'reg_num: {reg_num}')
        value = self.ram_read(self.pc + 2)

        self.reg[reg_num] = value

    def handle_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])

    def handle_pop(self):
        value = self.ram[self.reg[SP]]
        reg_num = self.ram_read(self.pc + 1)
        self.reg[reg_num] = value
        self.reg[SP] += 1

    def handle_push(self):
        self.reg[SP] -= 1
        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]
        self.ram[self.reg[SP]] = value

    def handle_call(self):
        ret_address = self.pc + 2
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = ret_address

        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]

    def handle_ret(self):
        self.pc = self.ram[self.reg[SP]]
        self.reg[SP] += 1

    def handle_add(self):
        num1 = self.ram_read(self.pc + 1)
        num2 = self.ram_read(self.pc + 2)
        self.alu("ADD", num1, num2)

    def handle_mul(self):
        num1 = self.ram_read(self.pc + 1)
        # print(f"num1: {num1}")
        num2 = self.ram_read(self.pc + 2)
        # print(f"num2: {num2}")
        self.alu("MUL", num1, num2)

    def handle_cmp(self):
        num1 = self.ram_read(self.pc + 1)
        num2 = self.ram_read(self.pc + 2)
        self.alu("CMP", num1, num2)

    def handle_jmp(self):
        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]

    def handle_jeq(self):
        reg_num = self.ram_read(self.pc + 1)
        # print(f"flag: {self.fl}")
        if self.fl == 0b00000001:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def handle_jne(self):
        reg_num = self.ram_read(self.pc + 1)
        if self.fl != 0b00000001:
            self.pc = self.reg[reg_num]
        else:
            self.pc += 2

    def handle_hlt(self):
        # print(f"halt activated")
        self.halted = True

    def run(self):
        """Run the CPU."""

        while self.halted != True:
            ir = self.ram[self.pc]
            val = ir
            op_count = val >> 6
            ir_length = op_count + 1
            # print(f"*ir out: {ir}")
            # print(f"ir_length: {ir_length}")
            # print(f"halted: {self.halted}")
            self.branchtable[ir]()

            if ir == 0 or None:
                # print(f"Unknown instructions at index {self.pc}")
                sys.exit(1)

            if ir != 80 and ir != 17 and ir != 84 and ir != 85 and ir != 86:
                # print(f'ir in: {ir}')
                self.pc += ir_length
