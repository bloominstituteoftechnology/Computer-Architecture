"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.memory = [0]*256
        self.register = [0]*8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.memory[address] = instruction
            address += 1


    def alu(self, op, register_a, register_b):
        """ALU operations."""

        if op == "ADD":
            self.register[register_a] += self.register[register_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.memory_read(self.pc),
            self.memory_read(self.pc + 1),
            self.memory_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.register[i], end='')

        print()

    def memory_read(self, MAR):
        return self.memory[MAR]

    def memory_write(self, MDR, MAR):
        self.memory[MAR] = MDR
        return

    def run(self):
        """Run the CPU."""
        logic = True

        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        while logic:
            IR = self.memory_read(self.pc)
            operand_a = self.memory_read(self.pc + 1)
            operand_b = self.memory_read(self.pc + 2)
            if IR == LDI:
                self.register[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN:
                print(self.register[operand_a])
                self.pc += 2
            elif IR == HLT:
                self.pc += 1
                break
            else:
                self.pc += 1
                print(f"{IR} - command is not available")
                sys.exit()
                
