"""CPU functionality."""

import sys
# reserved ragisters
SP = 7

# opcodes
# `HLT` instruction handler
# HLT = 1
# # `LDI` instruction handler
# LDI = 130
# # `PRN` instruction handler
# PRN = 71
HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 0XF4
        self.E = 0
        self.L = 0
        self.G = 0

    def load(self):
        """Load a program into memory."""
        try:
            filename = sys.argv[1]
            address = 0
            with open(filename) as f:
                # Read in its contents line by line
                for line in f:
                    # Remove any comments
                    line = line.split("#")[0]
                    # Remove whitespace
                    line = line.strip()
                    # Skip empty lines
                    if line == "":
                        continue

                    value = int(line, 2)

                    # Set the instruction to memory
                    self.ram[address] = value
                    address += 1
        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

    def ram_read(self, address):
        # should accept the address to read and return the value stored there.
        return self.ram[address]

    def ram_write(self, value, address):
        # should accept a value to write, and the address to write it to
        self.ram[address] = value

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        # Add the `CMP` instruction This is an instruction handled by the ALU.
        elif op == "CMP":
            # If they are equal, set the Equal E flag to 1, otherwise set it to 0.
            if self.reg[reg_a] == self.reg[reg_b]:
                self.E = 1
            # If registerA is less than registerB, set the Less-than L flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] < self.reg[reg_b]:
                self.L = 1
            # If registerA is greater than registerB, set the Greater-than G flag to 1, otherwise set it to 0.
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.G = 1
        else:
            raise Exception("Unsupported ALU operation")

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

    def run(self):
        """Run the CPU."""
        # Implement the core of `CPU`'s `run()` method
        self.load()

        while True:
            # needs to read mem address stores in register PC and store in IR - local variable
            IR = self.ram_read(self.pc)
            # read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` and `operand_b` in case the instruction needs them
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # Then, depending on the value of the opcode, perform the actions needed for the instruction per the LS-8 spec. Maybe an `if-elif` cascade...? There are other options, too

            if IR == HLT:
                # In `run()` in your switch, exit the loop if a `HLT` instruction is encountered regardless of whether or not there are more lines of code in the LS-8 program you loaded
                print("Exit")
                break
            elif IR == PRN:
                # Add the `PRN` instruction
                data = operand_a
                print(self.reg[data])
                self.pc += 2
            elif IR == LDI:
                # Add the `LDI` instruction
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
            elif IR == PUSH:
                data = self.reg[operand_a]
                self.reg[SP] -= 1
                self.ram_write(data, self.reg[SP])
                self.pc += 2
            elif IR == POP:
                data = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                self.reg[operand_a] = data
                self.pc += 2
            elif IR == CALL:
                # reg = memory[pc + 1]
                # register[sp] -= 1
                self.reg[SP] -= 1
                # memory[register[sp]] = pc + 2
                self.ram[self.reg[SP]] = self.pc + 2
                # pc = register[reg]
                self.pc = self.reg[operand_a]
                # op_pc = True
            elif IR == RET:
                # pc = memory[register[sp]]
                self.pc = self.ram[self.reg[SP]]
                # register[sp] += 1
                self.reg[SP] += 1
                # op_pc = True
            elif IR == CMP:
                self.alu("CMP", operand_a, operand_b)
                self.pc += 3
            elif IR == JMP:
                # Jump to the address stored in the given register.
                # Set the PC to the address stored in the given register.
                self.pc = self.reg[operand_a]
            elif IR == JEQ:
                # If equal flag is set (true),
                if self.E is 1:
                    # jump to the address stored in the given register.
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            elif IR == JNE:
                # If E flag is clear (false, 0)
                if self.E is 0:
                    # jump to the address stored in the given register.
                    self.pc = self.reg[operand_a]
                else:
                    self.pc += 2
            else:
                print("Error")
