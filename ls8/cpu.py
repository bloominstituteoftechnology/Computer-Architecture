"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.registers = {
            0: 0,
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
            7: 0
        }
        self.registers_internal = {
            "PC": 0,
            "IR": 0,
            "MAR": 0,
            "MDR": 0,
            "FL": 0
        }
        self.running = True

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

    def ram_read(self, loc):
        """Return the value that passed memory location"""
        self.registers_internal["MAR"] = loc            # the memory address being read
        self.registers_internal["MDR"] = self.ram[loc]  # the value just read
        return self.ram[loc]

    def ram_write(self, val, loc):
        self.registers_internal["MAR"] = loc    # the memory address being written to
        self.registers_internal["MDR"] = val    # the value to be written
        self.ram[loc] = val
        return 

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

        # Execute while the CPU is deemed running
        while self.running:
            # Read the data at the program counter ('') memory location
            #   PC: program counter
            #   IR: instruction register
            self.registers_internal["IR"] = self.ram[self.registers_internal["PC"]]

            # Read the next two memory locations (in case they happen to be operands)
            loc_operand_a = self.registers_internal["PC"] + 1
            loc_operand_b = self.registers_internal["PC"] + 2
            operand_a     = self.ram_read(loc_operand_a)
            operand_b     = self.ram_read(loc_operand_b)
            instr         = self.registers_internal["IR"]

            #* Execute the current instruction
            # LDI Instruction: load into register - Decimal = 130
            if instr == 0b10000010:
                # Operand A: register in which to load data
                # Operand B: data to be loaded
                self.registers[operand_a] = operand_b

                # Advance the program counter 3 memory locations
                self.registers_internal["PC"] = self.registers_internal["PC"] + 3 

            # PRN Instruction: print register - Decimal = 71
            elif instr == 0b1000111:
                # Operand: register containing the data to print
                print(f'Register: {operand_a} => {self.registers[operand_a]}')

                # Advance the program counter 2 memory locations
                self.registers_internal["PC"] = self.registers_internal["PC"] + 2 

            # HLT Instruction: halt execution - Decimal = 71
            elif instr == 0b0000001:
                self.running = False
                return

            # Invalid Instruction
            else:
                print("ERR: invalid instruction encountered. Terminating")
                self.running = False
             