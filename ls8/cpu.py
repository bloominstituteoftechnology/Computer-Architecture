"""CPU functionality."""

import sys

# opcodes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110

SP = 7

# Flags
LT = 0b00000100
GT = 0b00000010
EQ = 0b00000001


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.fl = 0
        self.bt = {
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            ADD: self.op_add,
            MUL: self.op_mul,
            POP: self.op_pop,
            PUSH: self.op_push,
            CALL: self.op_call,
            RET: self.op_ret,
            CMP: self.op_cmp,
            JMP: self.op_jmp,
            JEQ: self.op_jeq,
            JNE: self.op_jne
        }

    def op_ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b

    def op_prn(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def op_hlt(self, operand_a, operand_b):
        sys.exit(0)

    def op_add(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)

    def op_mul(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)

    def op_pop(self, operand_a, operand_b):
        self.reg[operand_a] = self.pop_val()

    def op_push(self, operand_a, operand_b):
        self.push_val(self.reg[operand_a])

    def op_call(self, operand_a, operand_b):
        # Pushing next instruction to stack
        self.push_val(self.pc + 2)
        # Setting pc to address of subroutine
        self.pc = self.reg[operand_a]

    def op_ret(self, operand_a, operand_b):
        # Poping next instruction off top of stack
        self.pc = self.pop_val()

    def op_cmp(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)

    def op_jmp(self, operand_a, operand_b):
        # Set the PC to the address stored in the given register
        self.pc = self.reg[operand_a]

    def op_jeq(self, operand_a, operand_b):
        # If equal flag is set (true), jump to the address stored in the given register
        if self.fl == EQ:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def op_jne(self, operand_a, operand_b):
        # If E flag is clear (false, 0), jump to the address stored in the given register
        if not self.fl == EQ:
            self.pc = self.reg[operand_a]
        else:
            self.pc += 2

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            # Open the file
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                    # Parse out the comments
                    comment_split = line.strip().split("#")
                    # Cast number strings to ints
                    value = comment_split[0].strip()
                    # Ignore blank lines
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # Populate a memory array
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def ram_read(self, mar):
        # Accept the address to read (mar) and return
        # address to write (mdr)
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mdr, mar):
        # Accept a value to write (mdr), and address
        # to write it to (mar)
        self.ram[mar] = mdr

    def push_val(self, val):
        self.reg[SP] -= 1
        self.ram_write(val, self.reg[SP])

    def pop_val(self):
        val = self.ram_read(self.reg[SP])
        self.reg[SP] += 1
        return val

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.fl = LT
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.fl = GT
            else:
                self.fl = EQ
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        while True:
            instruction = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            instruction_length = (instruction >> 6) + 1
            instruction_set_pc = ((instruction >> 4) & 0b1) == 1
            if instruction in self.bt:
                self.bt[instruction](operand_a, operand_b)
            # Check if opcode sets the pc
            # If not, increment pc by instruction_length
            if instruction_set_pc != 1:
                self.pc += instruction_length
