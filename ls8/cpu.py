# cpu.py

"""CPU functionality."""

import sys
import os

class CPU:
    """Main CPU class."""

    def __init__(self):
        # Set RAM
        self.ram = [0] * 256
        # Create registers: R0 - R6 empty
        self.reg = [0] * 8
        # R7 set to 0xF4
        self.reg[7] = 0xF4

        # Set program counter to 0
        self.pc = 0
        # Set flags to 0
        self.fl = 0
        # Memory Address Register, holds the memory address we're reading or writing
        self.mar = 0
        # #Memory Data Register, holds the value to write or the value just read
        self.mdr = 0

    def load(self, file_name):
        """Load a program into memory."""

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

        program = []

        input_text = os.path.join(os.path.dirname(__file__), f"examples/{file_name}")

        try:
            with open(input_text) as my_file:
                for line in my_file:
                    comment_split = line.split('#')
                    possible_binary_number = comment_split[0]

                    try:
                        x = int(possible_binary_number, 2)
                        # print("{:08b}: {:d}".format(x, x))
                        program.append(x)
                    except:
                        print(f"Failed to cast {possible_binary_number} to an int")
                        continue
        except:
            print(f"File: {file_name} not found...")

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

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

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

        running = True
        ldi = 0b10000010
        prn = 0b01000111
        hlt = 0b00000001
        mul = 0b10100010

        while running:
            # print(self.pc)
            command_to_execute = self.ram_read(self.pc)
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)
            
            if command_to_execute == ldi:
                print("LDI executed")
                self.reg[op_a] = self.pc + 2
                self.pc += ((command_to_execute >> 6) & 0b11) + 1
            elif command_to_execute == prn:
                print("Print executed")
                print(self.reg[op_a])
                self.pc += ((command_to_execute >> 6) & 0b11) + 1
            elif command_to_execute == mul:
                print("Mult executed")
                print(op_a, op_b)
                self.reg[op_a] *= self.reg[op_b]
                self.pc += ((command_to_execute >> 6) & 0b11) + 1
            elif command_to_execute == hlt:
                print("Halt executed")
                running = False
            else:
                print(f"Unkown command: {command_to_execute}")
                self.pc += ((command_to_execute >> 6) & 0b11) + 1

        self.trace()
