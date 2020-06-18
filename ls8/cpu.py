"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0] * 8 # 8 registers
        self.ram = [0] * 256 # memory of 256 bit
        self.program_counter = 0
        self.running = False 
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

    # load instruction from first
    # value
    # 
    def LDI(self):
        reg_num = reg[program_counter]
        pass 
    def PRN(self):
        reg_num = reg[program_counter] 
        pass 
    def HLT(self):
        reg_num = reg[program_counter]
        pass 

# MAR contains the address that is being read or written to. 
# he MDR contains> the data that was read or the data to write.
    
    # return address in RAM
    def ram_read(self, MAR) -> str:
        return self.ram[MAR]

    # write to RAM, return nothing
    def ram_write(self, MAR, MDR) -> None:
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MULT":
            self.reg[reg_a] *= self.reg[reg_b]    
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            #self.fl,
            #self.ie,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # execute the instructions stored in self.ram 
    def run(self):
        self.running = True

        while self.running:

            IR = self.ram_read(self.program_counter)

            if IR == 0b10000010:
                operand_a = self.ram_read(self.program_counter + 1)
                operand_b = self.ram_read(self.program_counter + 2)
                self.ram_write(operand_b, operand_a)
                self.program_counter += 3
            elif IR == 0b01000111:
                operand_a = self.ram_read(self.program_counter + 1)
                self.ram_write(operand_b, operand_a)
                print(f'printing... {self.ram[operand_a]}')           
                self.program_counter += 2

            elif IR == 0b00000001:
                self.running = False
                print("Program Halted")
            else:
                print("Unknown Instruction")
                self.running = False