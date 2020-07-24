"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
    
    def hlt(self):
        self.running = False
        self.pc += 1
    
    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        self.pc += 3

    def prn(self, reg_num):
        print(self.reg[reg_num])
        self.pc += 2
    
    def load(self):
        """Load a program into memory."""
        # # hardcoded:
        # address = 0
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

        # load an .ls8 file given the filename passed in as an argument
        file_name = sys.argv[1]
        try:
            address = 0
            with open(file_name) as file:
                for line in file:
                    split_line = line.split('#')[0]
                    command = split_line.strip()

                    if command == '':
                        continue

                    instruction = int(command, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        
        elif op == "CMP":
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag = 0b00000001
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = 0b10000010
            else:
                self.flag = 0b00000100
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
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        ADD = 0b10100000
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        CMP = 0b10100111
        JMP = 0b01010100
        JEQ = 0b01010101
        JNE = 0b01010110

        # load the instructions file
        self.load()
        while self.running:
            instruction_register = self.ram[self.pc]
            reg_a = self.ram[self.pc+1]
            reg_b = self.ram[self.pc+2]

            if instruction_register == HLT:
                self.hlt()
            
            elif instruction_register == LDI:
                self.ldi(reg_a, reg_b)
            
            elif instruction_register == PRN:
                self.prn(reg_a)
            
            elif instruction_register == MUL:
                self.alu("MUL", reg_a, reg_b)
                self.pc += 3
            
            elif instruction_register == PUSH:
                self.reg[7] -= 1

                reg_a = self.ram[self.pc+1]
                value = self.reg[reg_a]

                sp = self.reg[7]
                self.ram[sp] = value

                self.pc += 2

            elif instruction_register == POP:
                sp = self.reg[7]

                reg_a = self.ram[self.pc+1]

                value = self.ram[sp]
                self.reg[reg_a] = value

                self.reg[7] += 1
                self.pc += 2
            elif instruction_register == CALL:
                address = self.reg[reg_a]
                return_address = self.pc + 2
                self.reg[7] -= 1
                sp = self.reg[7]
                self.ram[sp] = return_address
                self.pc = address
            elif instruction_register == RET:
                sp = self.reg[7]
                return_address = self.ram[sp]
                self.reg[7] += 1
                self.pc = return_address
            elif instruction_register == CMP:
                self.alu('CMP', reg_a, reg_b)
                self.pc += 3

            elif instruction_register== JMP:
                break
                self.pc == self.reg[reg_a]
            
            elif instruction_register == JEQ:
                if (self.flag & HLT) == 1:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2

            elif instruction_register == JNE:
                if (self.flag & HLT) == 0:
                    self.pc = self.reg[reg_a]
                else:
                    self.pc += 2
            else:
                print(f"Instruction number {self.pc} not recognized!")
                self.pc += 1