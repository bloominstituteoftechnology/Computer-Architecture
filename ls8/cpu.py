"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.halted = False

    def load(self):
        """Load a program into memory."""

        address = 0

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

        for instruction in self.ram:
            self.ram[address] = instruction
            # print(instruction)
            address += 1

        try:
            if len(sys.argv)<2:
                print(f'Error from {sys.argv[0]}: missing filename argument')
                print(f'Usage: python3 {sys.argv[0]} <somefilename>')
                sys.exit(1)

            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split('#')[0]
                    stripped_split_line =  split_line.strip()
                    if stripped_split_line != "":
                        command =  int(stripped_split_line, 2)
                        print(address)
                        self.ram[address]= command
                        address +=1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found')
            print("(Did you double check the file name?)")

    def hlt(self):        
        sys.exit(0)

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, value, pc):
        self.ram[pc] = value

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
        running = True
        while running:
            self.trace()
            self.ram_write(9,1)
            self.trace()
            self.hlt()
            running = False