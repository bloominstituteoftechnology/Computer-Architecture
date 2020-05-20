"""CPU functionality."""

import sys




class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""   
        self.ram = [0] * 256
        self.reg = [0, 0, 0, 0, 0, 0, 0, 0xF4]
        self.pc = 0
        self.sp = 7
        self.branchtable = {}
        # self.branchtable["POP"] = self.pop
        self.branchtable["PUSH"] = self.push
        self.branchtable["LDI"] = self.ldi
        self.branchtable["MULT"] = self.mult
        self.branchtable["PRN"] = self.prn 

    def push(self):
        # Decrement the SP
        self.reg[self.sp] -= 1
        # Get register number
        index = self.ram[self.pc + 1]
        # Get value out of register
        val = self.reg[index]
        # Store value in memory at SP
        self.ram[self.reg[self.sp]] = val
        self.pc += 1

    def prn(self):
        self.pc += 1
        index = self.ram[self.pc]
        print(self.reg[index])
        self.pc += 1

    def mult(self):
        self.pc += 1
        operand1 = self.reg[self.ram[self.pc]]
        self.pc += 1
        operand2 = self.reg[self.ram[self.pc]]
        self.reg[self.ram[self.pc - 1]] = operand1 * operand2
        self.pc += 1

    def ldi(self):
        self.pc += 1
        index = self.ram[self.pc]
        self.reg[index] = self.ram[self.pc + 1]
        self.pc += 2

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
                self.branchtable["LDI"]()

            # push
            elif self.ram[self.pc] == 0b01000101:
                self.branchtable["PUSH"]()
                
            # multiply
            elif self.ram[self.pc] == 0b10100010:
                self.branchtable["MULT"]()

            # print
            elif self.ram[self.pc] == 0b01000111:
                self.branchtable["PRN"]()
                


