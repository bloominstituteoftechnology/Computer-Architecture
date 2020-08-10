"""CPU functionality."""

import sys

"""Instruction Opcodes"""
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Initialize ram to hold 256 bytes of memory
        byte = [0] * 8
        self.ram = [byte] * 256

        # Eight general purpose registers
        self.reg = [byte] * 8

        ## Internal Registers

        # Program Counter - address of the currently executing instruction
        self.pc = 0

        # Instruction Register - contains a copy of the currently executing
        # instruction
        self.ir = None

        # Memory Address Register - holds the memory address we're reading or
        # writing
        self.mar = 0

        # Memory Data Register - holds the value to write or the value just read
        self.mdr = None

        # Flags Register - holds the current flags status
        self.fl = None

        # Set up a branch table
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn

    def load(self):
        """Load a program into memory."""

        # Print an error if user did not provide a program to load
        # and exit the program
        if len(sys.argv) < 2:
            print("Please provide a file to open\n")
            print("Usage: filename file_to_open\n")
            sys.exit()

        try:
            # Open the file provided as the 2nd arg
            with open(sys.argv[1]) as file:
                for line in file:
                    # Split the line into an array, with '#' as the delimiter
                    comment_split = line.split("#")

                    # The first string is a possible instruction
                    possible_instruction = comment_split[0]

                    # If it's an empty string, this line is a comment
                    if possible_instruction == "":
                        continue

                    # If the string starts with a 1 or 0, it's an instruction
                    if possible_instruction[0] == "1" or possible_instruction[0] == "0":
                        # Get the first 8 values (remove trailing whitespace and
                        # chars)
                        instruction = possible_instruction[:8]

                        # Convert the instruction into an integer and store it
                        # in memory
                        self.ram[self.mar] = int(instruction, 2)

                        # Increment the memory address register value
                        self.mar += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == SUB:
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == DIV:
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        """
        Should accept the address to read and return the value stored there
        """
        self.mar = address
        self.mdr = self.ram[self.mar]

        return self.mdr

    def ram_write(self, address, value):
        """
        Should accept a value to write, and the address to write to
        """
        self.mar = address
        self.mdr = value

        self.ram[self.mar] = self.mdr

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def handle_hlt(self):
        sys.exit()

    def handle_ldi(self):
        register = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[register] = value

    def handle_prn(self):
        register = self.ram_read(self.pc + 1)
        print(self.reg[register])

    def run(self):
        """Run the CPU."""
        running = True

        while running:
            # Get the current instruction
            instruction = self.ram_read(self.pc)

            # Store a copy of the current instruction in IR register
            self.ir = instruction

            # Get the number of operands
            num_operands = instruction >> 6

            # Store the bytes at PC+1 and PC+2
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # Check if it's an ALU instruction
            is_alu_operation = (instruction >> 5) & 0b1

            if is_alu_operation:
                self.alu(self.ir, operand_a, operand_b)
            else:
                self.branchtable[self.ir]()

            # Point the PC to the next instruction in memory
            self.pc += num_operands + 1
