"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0 # Program Counter (PC), the index into memory of the currently-executing instruction
        

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR): # Memory Address Register (MAR) / Memory Data Register (MDR)
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

    def run(self, args=None):
        """Run the CPU."""
        
        if not args or args[0] == '' or not args[0]: print("Error: Could not find file to run.")
        
        with open(args[0]) as file:
            lines = file.readlines()
            print(lines)
            for line in lines:
                line = line.split(' # ')[0].strip()
                print(f'> {line}')

        running = True

        ir = {
             0b10000010: 'LDI',
             0b01000111: 'PRN',
             0b00000001: 'HLT'
        }

        while running:
            i = self.ram[self.pc]
            ins = ir[i]

            if ins == 'LDI':
                # Preform LDI Action.
                reg_num = self.ram_read(self.pc + 1)
                value = self.ram_read(self.pc + 2)
                self.reg[reg_num] = [value]
                self.pc += 3
            elif ins == 'PRN':
                # Preform PRN Action.
                reg_num = self.ram_read(self.pc + 1)
                print(self.reg[reg_num])
                self.pc += 2
            elif ins == 'HLT':
                # Preform HLT.
                running = False
            else: print(f'Unknown Instruction Code: {i}')