 # Inventory what is here ^
 # Implement the CPU constructor ^
 # Add RAM functions ram_read() and ram_write()
 # Implement the core of run()
 # Implement the HLT instruction handler
 # Add the LDI instruction
 # Add the PRN instruction
 #
"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0    # program counter: address of the currently executing instruction
        self.fl = 0     # flags


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

    def ram_read(self, MAR):
        """Accepts the address to read and return the value stored there"""
        return self.ram[MAR]
        # MAR contains the address that is being read or written to.
        # MDR contains the data that was read

    def ram_write(self, MAR, MDR):
        """Should accept a value to write and the address to write it to"""
        self.ram[MAR]=MDR
        # so we will move the stuff from MAR TO MDR

    def run(self):
        """Run the CPU."""

        Running=True

        LDI=0b10000010
        HLT=0b00000001
        PRN=0b01000111

        while Running:
            # read the memory address sotred in pc and store it in Instruction Register
            Command=self.ram_read(self.pc)
            if Command == LDI:
                operand_a = self.ram_read(self.pc+1)
                operand_b = self.ram_read(self.pc+2)
                # registers
                # sets a specific register to a specified value
                self.reg[operand_a]=operand_b
                self.pc+=3

            elif Command==HLT:
                Running=False
                self.pc+=1

            elif Command==PRN:
                # PRN: adding
                reg = self.ram[self.pc+1]
                print(self.reg[reg])  # prints 8 to the console.
                self.pc+=2
