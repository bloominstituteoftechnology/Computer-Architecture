"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 256
        self.reg = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8, 130 in decimal
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0, 71 in decimal
        #     0b00000000,
        #     0b00000001, # HLT, 1 in decimal
        # ]

        program = []

        if len(sys.argv) != 2:  
            print("usage invalid")
            sys.exit(1)

        try:
            with open(f'examples/{sys.argv[1]}') as f:
                for line in f:
                    try:
                        line = line.split('#', 1)[0]
                        line = int(line, 2)          
                        program.append(line)
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]

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
            ir = self.ram[self.pc] # Instruction Register - internal part of CPU that holds a value.  Special purpose part of CPU.

            if ir == 130: # LDI instruction
                reg_num = self.ram[self.pc+1]
                value = self.ram[self.pc+2]
                self.reg[reg_num] = value
                self.pc += (ir >> 6) + 1 # using bit shifting to determine length of instruction set.
            
            elif ir == 71: # PRN instruction
                reg_num = self.ram[self.pc+1]
                print(self.reg[reg_num])
                self.pc += (ir >> 6) + 1

            elif ir == 1: # HLT instruction
                running = False

            elif ir == 162:
                num1 = self.ram[self.pc+1]
                num2 = self.ram[self.pc+2]
                print(self.alu("MUL", num1, num2))
                self.pc += (ir >> 6) + 1

            else:
                self.pc += (ir >> 6) + 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDA):
        self.ram[MAR] = MDA
        return self.ram[MAR]


    # x >> 6 is right shift by 6
    # x << 6 is left shift by 6


    

