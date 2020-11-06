"""CPU functionality."""

import sys

#save a number
LDI = 0b10000010
#print a number
PRN = 0b01000111
#stop program
HLT = 0b00000001
#multiply
MUL = 0b10100010



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0]*8
        self.ram = [0]*256

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0
        program = []

        with open(sys.argv[1]) as file:
            for line in file:
                line_split = line.split("#")
                command = line_split[0].strip()
                if command == "":
                    continue
                command_num = int(command, 2)
                program.append(command_num)

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] = self.reg[reg_a]* self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
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
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if IR == HLT:
                self.trace()
                running = False
            elif IR == PRN:
                print(self.reg[operand_a])
                self.trace()
                self.pc +=2
            elif IR == LDI:
                self.reg[operand_a]=operand_b
                print(operand_a, operand_b)
                self.trace()
                self.pc += 3
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc +=3
            else:
                print(f"unrecognized command {IR}")
                self.trace()
                running = False