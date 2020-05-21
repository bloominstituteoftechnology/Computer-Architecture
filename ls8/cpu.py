import sys
import os

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        pass
        self.pc = 0
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.SP = 0xf3

    def load(self, filename):
        """Load a program into memory."""
        # print("Loading CPU...")
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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        try:
            address = 0
            #open the file
            with open(sys.argv[1]) as f:
                #read every line
                for line in f:
                    # Use strip to make sure no errors occur in spacing
                    comment_split = line.strip().split("#")
                    # Cast number string to int
                    value = comment_split[0].strip()
                    # Leave Strings empty
                    if value == "":
                        continue
                    instruction = int(value, 2)
                    # Populate memory array
                    self.ram[address] = instruction
                    address += 1

        except:
            print("cant find file")
            sys.exit(2)


    def ram_read(self, address):
        # Memory Address Register
        # The MAR contains the address that is being read or written to.
        return self.ram[address]

    def ram_write(self, address, value):
        # Memory Data Register
        # The MDR contains the data that was read or the data to write. 
        self.ram[address] = value


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
        while True:
            # IR = self.ram_read(self.PC)
            # op = self.getOperation(IR)
            opcode = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            if opcode == LDI:
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif opcode == PRN:
                print(self.reg[operand_a])
                self.pc += 2
            elif opcode == MUL:
                self.alu(opcode, operand_a, operand_b)
                self.pc += 3
            elif opcode == PUSH:
                operand_a = self.ram_read(self.pc + 1) #Register whose value is to be pushed on stack
                self.ram_write(self.SP, self.reg[operand_a])
                self.pc += 2
                self.SP -= 1
            elif opcode == POP:
                operand_a = self.ram_read(self.pc + 1)  # Register in which stack value is to be popped
                self.reg[operand_a] = self.ram_read(self.SP+1)
                self.SP += 1
                self.pc += 2

            elif opcode == HLT:
                sys.exit(0)
            else:
                print(f"Did not work")
                sys.exit(1)