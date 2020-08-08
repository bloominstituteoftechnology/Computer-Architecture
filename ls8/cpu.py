"""CPU functionality."""

import sys
import re

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8 # 8 general-purpose registers.
        self.ram = [0] * 256 # to hold 256 bytes of memory

    def load(self, file):
        """Load a program into memory."""

        address = 0

        # # For now, we've just hardcoded a program:
        with open(file, 'r') as commands:
            for command in commands:
                is_command = re.match("^(0|1)\w+", command)

                if is_command == None:
                    continue

                print(is_command.group(0))
                self.ram[address] = int(is_command.group(0), 2)
                address += 1



    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

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

        ir = None

        pc = 0 #counter
        ir = None # copy of currently execution instruction
        mar = None # holds the address we're reading from
        mdr = None # holds the value to write or just read
        fl = None # flags, ?? what the heck is this for?

        # It needs to read the memory address that's stored in register PC
        # and store that result in IR

        is_running = True

        # Meanings of the bits in the first byte of each instruction: AABCDDDD

        # AA Number of operands for this opcode, 0-2
        # B 1 if this is an ALU operation
        # C 1 if this instruction sets the PC
        # DDDD Instruction identifier

        while is_running:

            # 01000111
            ir = self.ram[pc] & 0b0001111
            print(f"instruction: {ir}")
            # PRN
            # PRN register pseudo-instruction

            # Print numeric value stored in the given register.

            # Print to the console the decimal integer value that is stored in the given register.
            if (ir == 0b0111):
                mdr = self.reg
                mar = self.ram[pc + 1]
                pc += 1
                print(f"Register {mar}: {mdr[mar]}")
            elif (ir == 0b0010):
                mdr = self.ram[pc + 2]
                # print(f"Writing to {self.ram[pc + 1]}: value - {mdr}")
                self.reg[self.ram[pc + 1]] = mdr
                pc += 2
            elif (ir == 0b01):
                # print("HLT instruction")
                is_running = False
                break

            pc += 1