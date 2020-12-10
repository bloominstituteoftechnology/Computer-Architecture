"""CPU functionality."""

import sys

"""
 Inventory what is here
 Implement the CPU constructor
 Add RAM functions ram_read() and ram_write()
 Implement the core of run()
 Implement the HLT instruction handler
 Add the LDI instruction
 Add the PRN instruction
 """
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 15
        self.pc = 0
        self.registers = [0] * 8

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [ # LOOK IN THE SPECS
            # From print8.ls8
            0b10000010, # LDI R0,8 (--- one operand ---)
            0b00000000, # this indicates the register to be saved to '0'
            0b00001000, # ---- 8 ---- this indicates the value
            0b01000111, # PRN R0
            0b00000000, # index to print in register
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, pc):
        pass

    def ram_write(self, pc):
        pass

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     #elif op == "SUB": etc
    #     else:
    #         raise Exception("Unsupported ALU operation")

    # def trace(self):
    #     """
    #     Handy function to print out the CPU state. You might want to call this
    #     from run() if you need help debugging.
    #     """

    #     print(f"TRACE: %02X | %02X %02X %02X |" % (
    #         self.pc,
    #         #self.fl,
    #         #self.ie,
    #         self.ram_read(self.pc),
    #         self.ram_read(self.pc + 1),
    #         self.ram_read(self.pc + 2)
    #     ), end='')

    #     for i in range(8):
    #         print(" %02X" % self.reg[i], end='')

    #     print()

    def run(self):
        """Run the CPU."""
        running = True
        register_count = -1
        for register in self.registers:
            register_count += 1
            if register_count <= 6:
                self.registers[register_count] = 0
            else:
                self.registers[register_count] = '0xF4'

        self.ram = [0] * 15
        self.pc = 0
        self.load()

        while running:
            command_to_execute = self.ram[self.pc]

            # LDI instruction
            if command_to_execute == 130:
                spot_to_store = self.ram[self.pc + 1]
                value_to_store = self.ram[self.pc + 2]

                self.registers[spot_to_store] = value_to_store

                self.pc += 3

            # PRN instruction
            elif command_to_execute == 71:
                selected_register = self.ram[self.pc + 1]
                print(self.registers[selected_register])
                self.pc += 2

            # HLT instruction
            elif command_to_execute == 1:
                running = False

            # EXCEPTION
            else:
                print("ERROR INCORRECT COMMAND")

        
