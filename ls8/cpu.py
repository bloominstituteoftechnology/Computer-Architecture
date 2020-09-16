"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = [0] * 8 # registers 0 - 7
        self.pc = 0 # Program Counter, address of the currently executing 
        # the registers are "variables" and there are
        # a fixed number of them (8)
        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.LDI = 0b10000010 
        self.MUL = 0b10100010
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # args = sys.argv[0]
        # print(args, 'the first argument in sys.argv')
        args2 = sys.argv[1]
        # print(args2, 'second argument in sys.argv')


        with open(f"{args2}", 'r') as pro_file:

            for line in pro_file:
                # print(line)

                # we will check each line, take out the notes and save those program numbers in
                # our programs array. 
                split_line = line.split('#')
                # print(split_line) # returns ['binary number', 'comments from #']
                bit = split_line[0].strip() #takes care of white space from first line 


                if bit == "":
                    continue

                try:
                    instruction = int(bit,2) # this turns our string of bit code, into an actual 
                    # binary digit, which is what we want

                except ValueError:
                    print(f"Invalid value: {bit}")
                
                self.ram[address] = instruction
                address += 1
        # print(args2[0], 'second argument in second spot')
        # program = [
            # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        # ]

        # print(program)

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        #overwrite in the ram position, or place this value at that position
        self.ram[address] = value

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


        operating = True
        while operating:
            ir = self.ram_read(self.pc) # Instruction register reading the current item in the PC

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.HLT:
                operating = False
                self.pc += 1

            if ir == self.PRN:
                print(self.registers[operand_a])
                self.pc += 2

            if ir == self.LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3

            if ir == self.MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
                self.pc += 3
