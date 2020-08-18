"""CPU functionality."""

import sys

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

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
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

    def ldi(self, operand_a, operand_b):
        # Set the value of a register to an integer
        self.reg[operand_a] = operand_b

    def prn(self, operand_a):
        # This will print the numeric value stored in the given register
        print(self.reg[operand_a])

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001

        running = True
        
        while running:
            # Instruction register is going to read the the memory address thats stored in register PC
            IR = self.ram_read(self.pc)
            
            # We'll read the bytes from RAM into variables in case the instructions need them
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # If our instruction register is equal to HLT (Hault the CPU)
            if IR == HLT:
                # We stop running
                running = False
                # We increment the program counter by 1
                self.pc += 1
            
            elif IR == LDI:
                # Execute our LDI function using our two operands as input parameters
                self.ldi(operand_a, operand_b)
                # Increment the program counter by 3
                self.pc += 3

            elif IR == PRN:
                # Execute our PRN function using operand_a
                self.prn(operand_a)
                # Increment the program counter by 2
                self.pc += 2
            
            else:
                # If everything fails, we'll terminate and print out that it's a bad input
                print(f"Bad input: {bin(IR)}")
                running = False
