"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0  # program counter
 
        self.ram = [0] * 256

        self.reg = [0] * 8
        self.reg[SP] = 0xf4

    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

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
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        def LDI(a, b): self.reg[a] = b
        def PRN(a, b): print(self.reg[a])
        opcodes = {
          0b00000000: 'NOP',
          0b00000001: 'HLT',
          0b10000010: LDI,
          0b01000111: PRN
        }
        while (op_fn := opcodes[(ir := self.ram_read(self.pc))]) != 'HLT':
            num_operands = ir >> 6 # Grab two highest bits
            operand_a = self.ram_read(self.pc + 0b1)
            operand_b = self.ram_read(self.pc + 0b10)
            if op_fn != 'NOP':
                op_fn(operand_a, operand_b)
            self.pc += (num_operands + 1)