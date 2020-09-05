"""CPU functionality."""

import sys

HALT = 0b00000001
PRNT = 0b01000111
LDI = 0b10000010

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0 # program counter
        self.registers = [0] * 8 # example R0 - R7
        self.ram = [0] * 256 # list
        self.running = True


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        HALT = 0b00000001
        PRNT = 0b01000111
        LDI = 0b10000010

        program = [
            # From print8.ls8
            LDI, # LDI R0,8
            0b00000000, # register 0
            0b00001000, # print 8
            PRNT, # PRN R0
            0b00000000,
            HALT,
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

        while self.running: 
            instruction = self.ram[self.pc]

            if instruction == LDI:
                reg_location = self.ram_read(self.pc + 1)
                reg_value = self.ram_read(self.pc + 2)
                self.ram_write(reg_location, reg_value)
                print(self.registers[reg_location])
                self.pc += 2
            elif instruction == PRNT:
                curr_val = self.ram[self.pc + 1]
                print(curr_val)
                self.pc += 1
            elif instruction == HALT:
                self.running = False
            else:
                print(f'No such {instruction} exists')
                sys.exit(1)
        
        self.pc += 1
        

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
