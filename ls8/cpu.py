"""CPU functionality."""

import sys



class CPU:
    """Main CPU class."""

    def __init__(self, register, ram):
        """Construct a new CPU."""
        self.reg = [0] * register
        self.pc = 0
        self.ram = [0] * ram

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
        # Loads program into RAM
        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
    def ram_write(self, regLocation, value):
        self.reg[regLocation] = value
        #self.pc += 3

    def ram_read(self, regLocation):
        return self.reg[regLocation]
        # Can advance self.pc here or in run, but not both!
        #self.pc += 2
    
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
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001 
        MUL = 0b10100010
        """Run the CPU."""
        # Load the program
        self.load()
        # From ram, read instructions
        print("instructions given: ")
        halted = True
        while halted is True:
            # Go thru RAM and read instructions
            instructions = self.ram[self.pc]
            if instructions == LDI:
                # At this reg location, insert this value
                self.ram_write(self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3
            elif instructions == PRN:
                # At this reg location, read the value
                print(self.ram_read(self.ram[self.pc + 1]))
                self.pc += 2
            elif instructions == MUL:
                # At these 2 reg locations, read the values and multiply
                a = self.ram_read(self.ram[self.pc + 1])
                b = self.ram_read(self.ram[self.pc + 2])
                c = a * b
                self.ram_write(a, c)
            elif instructions == HLT:
                halted = False
                self.pc += 1
            else: 
                print(f"Unknown command at {self.pc}", "Command give: ", self.reg[self.pc])

CPU(8, 8).run()

