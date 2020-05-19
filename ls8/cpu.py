"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        pass

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8 Set the value of a register to an integer.
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0 Print numeric value stored in the given register. Print to the console the decimal integer value that is stored in the given register.
            0b00000000,
            0b00000001, # HLT - Halt the CPU
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
        """Run the CPU.
        read the memory address that's stored in register `PC`, and store
        that result in `IR`, the _Instruction Register_
        
        read the bytes at `PC+1` and `PC+2` from RAM into variables `operand_a` 
        and `operand_b` in case the instruction needs them.
        
        the `PC` needs to be updated to point to the next instruction 
        for the next iteration of the loop in `run()`"""
        IR = 0 # _Instruction Register_ contains a copy of the currently executing instruction
        self.ram_read(self.pc)
        self.ram_read(self.pc + 1)

    def ram_read(self):
        """accept the address to read and return the value stored
there."""
        int(self)
        return self

    def ram_write(self):
        """accept a value to write, and the address to write it to."""

        return address
