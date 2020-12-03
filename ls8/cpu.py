"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0 
        self.fl = 0
        self.running = True
        self.reg = [0, 0, 0, 0 , 0, 0, 0, 0xF4]

        self.HLT = 0b00000001
        self.LDI = 0b10000010
        self.PRN = 0b01000111

    def ram_read(self, pc):
        return self.ram[pc]

    def ram_write(self, pc, val):
        self.ram[pc] = val

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

    def run(self):
        """Run the CPU."""
        while self.running == True:
            instruction = self.ram_read(self.pc)
            #print('instruction', "{0:b}".format(instruction))

             
            if instruction == self.PRN:
                val_to_print = self.ram[self.pc + 1]
                print(self.reg[val_to_print])
                self.pc += 2
                print('prn ran')
            elif instruction == self.LDI:
                reg_to_store = self.ram[self.pc + 1]
                val_to_store = self.ram[self.pc + 2]
                self.reg[reg_to_store] = val_to_store
                self.pc += 3
                print('ldi ran')
            elif instruction == self.HLT:
                print('hlt ran')
                self.running = False
            else:
                unknown_instruction = "{0:b}".format(instruction)
                print(f"Instruction Unknown {unknown_instruction}")
                sys.exit(1)
                
