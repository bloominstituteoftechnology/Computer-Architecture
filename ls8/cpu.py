"""CPU functionality."""

#Instructions for today
"""
Day 1: Get print8.ls8 running
 Inventory what is here

 Implement the CPU constructor
 
 Add RAM functions ram_read() and ram_write()
 
 Implement the core of run()
 
 Implement the HLT instruction handler
 
 Add the LDI instruction
 
 Add the PRN instruction
"""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0

    def ram_read(self, location): 
        # print(location, self.ram[location])
        return self.ram[location]


    def ram_write(self, address, value):
        self.ram[address] = value

        
    def load(self, file_name):
        """Load a program into memory."""
        address = 0

        # LDI = 0b10000010
        # EIGHT = 0b00001000
        # PRINT_NUM = 0b01000111
        # HALT = 0b00000001

        with open(file_name) as f: 
            lines = f.readlines()
            lines = [line for line in lines if line.startswith('0') or line.startswith('1')]
            program = [int(line[:8], 2) for line in lines]

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        for instruction in program:
            self.ram[address] = instruction
            # print('program statements',self.ram[address])
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
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
         
        
        running = True 
        IR = self.pc

        ldi = 0b10000010
        prn = 0b01000111
        hlt = 0b00000001

        while running: 
            # print(instruction, IR)
            instruction = self.ram_read(IR)
            op_a = self.ram_read(IR + 1)
            op_b = self.ram_read(IR + 2)
            if instruction == ldi: 
                # print("op_a: ",op_a)
                # self.ram_read(IR + 2)
                self.register[op_a] = op_b
                # print("hello")
                IR += 3
            elif instruction == prn: 
                print(self.register[op_a])
                IR += 2
            elif instruction == hlt: 
                sys.exit(0)
            else:
                print(f"Unknown instruction at pc point: {IR}")
                # print("has exited")
                sys.exit(1)

