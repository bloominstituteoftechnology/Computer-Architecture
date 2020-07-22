"""CPU functionality."""

import sys
# print(sys.argv)
# sys.exit(0)

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.HLT = 0b00000001
        self.MUL = 0b10100010
        self.address = 0

    def load(self):
        """Load a program into memory."""

        with open(sys.argv[1]) as f:
            for line in f:
                try:
                    line = line.strip().split("#",1)[0]
                    # if line == '':
                    #     continue
                    line = int(line, 2)
                    self.ram[self.address] = line
                    self.address += 1
                    # print(line)
                except ValueError:
                    pass

        # address = 0

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
            self.reg[reg_a] += self.reg[reg_b]
        elif op == self.MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")



    def ram_read(self, address=None):
        v = self.ram[address]
        return v

    def ram_write(self, value=None, address=None):
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
        self.trace()
        running = True
        while running:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if IR ==  0b10000010:  # LDI instruction
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == 0b01000111:  # PRN instruction
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == self.HLT:
                running = False
            elif IR == self.MUL:
                # self.reg[operand_a] *= self.reg[operand_b]
                self.alu(IR, operand_a, operand_b)
                self.pc += 3
            else:
                print(f"Unknown instruction {IR}")
                running = False       