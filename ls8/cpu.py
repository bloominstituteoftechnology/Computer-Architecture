"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = {}
        self.reg = [None] * 8
        self.sp = len(self.reg)
        self.pc = 0
        self.ir = self.pc
        # self.ie = 0
        self.running = 0

    def load(self, program):
        """Load a program into memory."""

        address = 0
        file1 = open(program, 'r')
        program = file1.readlines()
        # For now, we've just hardcoded a program:
        # program = [
            # # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        # ]

        for instruction in program:
            if instruction[0].isdigit():
                self.ram[address] = instruction[:8]
                address += 1


    def ram_read(self, r):
        return int(self.ram[r],2)

    def ram_write(self, operand_a, operand_b):
        operand_a = self.ram_read(operand_a)
        operand_b = self.ram_read(operand_b)
        self.reg[operand_a]=operand_b

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL": 
            self.reg[reg_a] = f'{self.reg[reg_a] * self.reg[reg_b]}'
        elif op == "DIV": 
            self.reg[reg_a] /= self.reg[reg_b]
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
        self.running = 1
        while self.running and self.pc < len(self.ram):
            num_operands = 1
            command = self.ram[self.pc]
            if command[0:2] == '01':  #Has 1 operands, increment by 2 after iteration of fx
                num_operands += 1
            if command[0:2] == '10':  #Has 2 operands, increment by 3 after iteration of fx
                num_operands += 2
            if command[2:3] == '1':  #ALU, runs arithmetic
                if command[3:] == '00010': 
                    self.alu('MUL', self.ram_read(self.pc+1), self.ram_read(self.pc+2))
                elif command[3:] == '00000': 
                    self.alu('ADD', self.ram_read(self.pc+1), self.ram_read(self.pc+2))
            elif command[3:] == '00001': #HLT, exits program
                self.running = 0
                exit()
            elif command[3:] == '00111': #PRN, returns value at index
                index = self.ram_read(self.pc+1)
                number_to_print = self.reg[index]
                print(number_to_print)
            elif command[3:] == '00010': #LDI, store value
                self.ram_write(self.pc+1, self.pc+2)
            elif command[3:] == '00101': #PUSH, adds value at index to stack
                self.sp -=1
                index = self.ram_read(self.pc+1)
                self.reg[self.sp] = self.reg[index]
            elif command[3:] == '00110': #POP, removes value from index of stack
                index = self.ram_read(self.pc+1)
                popper = self.reg[self.sp]
                self.sp +=1
                self.reg[index] = popper
            if command[3:4] == '1':  #Maual PC setting
                if command[4:] == '0000': 
                    index = self.ram_read(self.pc+1)
                    self.ir = self.pc+2
                    self.pc=self.reg[index]
                if command[4:] == '0001': 
                    self.pc = self.ir
            else:
                self.pc+=num_operands
            