"""CPU functionality."""

import sys

LDI = 0b10000010
HLT = 0b00000001
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # This will hold our 256 bytes of memory
        self.ram = [0] * 256
        
        # This will hold out 8 general purpose registers
        self.reg = [0] * 8

        # This is our program counter. It holds the address of the currently executing instruction
        self.pc = 0

        self.running = True

    def ram_read(self, MAR):
        # MAR = Memory Address Register
            # This will accept the address to read and return the value stored
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # MDR = Memory Data Register
            # This will accept the value to write, and the address to write it to
        self.ram[MAR] = MDR


    def load(self):
        """Load a program into memory."""

        filename = sys.argv[1]

        # We'll open the files
        with open(filename) as files:
            # using a key value pair, we'll enumerate through our files
            for address, line in enumerate(files):
                # We'll split the string into a list using "#" as the separator
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                except ValueError:
                    continue
                self.ram_write(address, v)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            # added the option for multiplication
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def LDI(self):
        # We'll read the bytes from RAM into variables in case the instructions need them
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        # Set the value of a register to an integer
        self.reg[operand_a] = operand_b

        # Increment the program counter by 3
        self.pc += 3

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)

        # This will print the numeric value stored in the given register
        print(self.reg[operand_a])

        # Increment the program counter by 2
        self.pc += 2

    def HLT(self):
        # We hault the CPU by setting it to false
        self.running = False
    
    def MUL(self):
        # We'll read the bytes from RAM into variables in case the instructions need them
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)

        # Use "MUL" to indicate multiplication, insert our two operands as the input
        self.alu("MUL", operand_a, operand_b)

        # Increment our program counter by 3
        self.pc += 3

    def call_function(self, n):
        # This is so our run method will know what to execute
        branch_table = {
            LDI : self.LDI,
            PRN : self.PRN,
            HLT : self.HLT,
            MUL : self.MUL,
        }

        files = branch_table[n]

        # As long as the method we're trying to get it not none, we can execute
        if branch_table.get(n) is not None:
            files()
        else:
            # Otherwise we print out that it's a bad instruction and we exit out
            print(f"Unknown instruction {n}")
            sys.exit(1)

    def run(self):
        """Run the CPU."""
        # While true
        while self.running:
            # Our instruction register is going to read the memory address that's stored in register PC
            IR = self.ram_read(self.pc)
            # Call the function
            self.call_function(IR)
