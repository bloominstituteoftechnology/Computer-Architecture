"""CPU functionality."""

import sys
# import re


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Create 256 bytes of Ram, 8 registers, assign memory for the stack, a counter, and continuous variable
        # memory
        self.ram = [0] * 256
        # registers
        self.registers = [0] * 8
        #assign memory
        self.registers[7] = 240 # hex 0XF0
        # continuous variable
        self.running = True
        # counter
        self.pc = 0

    def ram_read(self, address):
        # Accepts the address and returns the value from ram
        return(self.ram[address])
    

    def ram_write(self, address, value):
        # Accepts the address and value and assigns to ram
        self.ram[address] = value



    def load(self):
        """Load a program into memory."""
        if len(sys.argv) < 2:
            print("Insufficient arguments, re-evaluate and try again")
            print("Usage: filename file_to_open")

        address = 0

        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    potential_num = comment_split[0]

                    if potential_num == "":
                        continue

                    if potential_num[0] == "1" or potential_num[0] == "0":
                        num = potential_num[:8]
                        
                        self.ram[address] = int(num, 2)
                        address += 1
                    
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} not found")
            

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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        
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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110

        while self.running:
            # the HLT instruction

            if self.ram[self.pc] == HLT:
                self.running == False

            # the LDI instruction
            if self.ram[self.pc] == LDI:
                num_to_load = self.ram[self.pc + 2]
                reg_index = self.ram[self.pc + 1]
                self.registers[reg_index] = num_to_load
                self.pc += 3

            # the PRN instruction
            if self.ram[self.pc] == PRN:
                reg_to_print = self.ram[self.pc +1]
                print(self.registers[reg_to_print])
                self.pc += 2

            # the MUL instruction
            if self.ram[self.pc] == MUL:
                first_reg = self.ram[self.pc + 1]
                sec_reg = self.ram[self.pc + 2]
                first_factor = self.registers[first_reg]
                sec_factor = self.registers[sec_reg]
                product = first_factor * sec_factor
                print(product)
                self.pc += 3

            # the PUSH instruction
            if self.ram[self.pc] == PUSH:
                # when pushing, first decrement the stack pointer
                self.registers[7] -= 1
                # next find the register for pushing and it's value
                reg_to_push = self.ram[self.pc + 1]
                num_to_push = self.registers[reg_to_push]
                # copy the number to memory
                SP = self.registers[7]
                self.ram[SP] = num_to_push
                self.pc += 2

            # the POP instruction
            if self.ram[self.pc] == POP:
                # when popping, don't decrement the stack pointer
                SP = self.registers[7]
                # the value should be at the most recent position of the stack pointer
                num_to_pop = self.ram[SP]
                # find the register for popping and copy the number into that register
                reg_to_pop = self.ram[self.pc + 1]
                self.registers[reg_to_pop] = num_to_pop
                # after POP increment the stack pointer to the new 'most recent' position
                self.registers[7] += 1
                self.pc += 2


    
            



