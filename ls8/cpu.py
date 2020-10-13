"""CPU functionality."""

import sys

HLT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.register = [0] * 8
        self.pc = 0
    
    def ram_read(self, address):
        return self.ram[address]
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        try:
            with open(sys.argv[1]) as f:
                #can be interpreted as "for instruction in program"
                for line in f:
                    line = line.strip()

                    #accounting for any comments or blank lines
                    if line == '' or line[0] == '#'
                    continue

                    try:
                        str_value = line.split("#")[0]
                        value = int(str_value, 10)

                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit()
                    
                    ram[address] = value
                    address += 1
        except FileNotFoundError:
            print(f"File not found!: {sys.argv[1]}")
            sys.exit(0)

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
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
            print(" %02X" % self.register[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        
        running = True

        while running is True:
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == HLT:
                #HLT
                self.pc += 1
                running = False
            elif ir == LDI:
                #LDI
                reg_num = operand_a
                value = operand_b
                self.register[reg_num] = value
                self.pc += 3
            elif ir == PRN:
                #PRN
                reg_num = operand_a
                print(self.register[reg_num])
                self.pc += 2
            else:
                print("Unknown instruction")
                sys.exit(0)

