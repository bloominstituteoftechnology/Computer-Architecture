"""CPU functionality."""

import sys




class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.pc = 0

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) < 2:
            print("No program specified. Please specify a program.")
            sys.exit(1)

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                self.ram[address] = v
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
        halted = False
        while not halted:
            
            # halt
            if self.ram[self.pc] == 0b00000001:
                halted = True

            # load into reg
            elif self.ram[self.pc] == 0b10000010:
                self.pc += 1
                index = self.ram[self.pc]
                self.reg[index] = self.ram[self.pc + 1]
                self.pc += 2

            # multiply
            elif self.ram[self.pc] == 0b10100010:
                self.pc += 1
                operand1 = self.reg[self.ram[self.pc]]
                self.pc += 1
                operand2 = self.reg[self.ram[self.pc]]
                self.reg[self.ram[self.pc - 1]] = operand1 * operand2
                self.pc += 1

            # print
            elif self.ram[self.pc] == 0b01000111:
                self.pc += 1
                index = self.ram[self.pc]
                print(self.reg[index])
                self.pc += 1




