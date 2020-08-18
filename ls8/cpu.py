"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #R0 - R7
        #R0 is for flags
        #R7 is for stack pointer
        self.reg = [0]*8
        #Initial tracker for commands
        self.pc = self.reg[7]
        #emulated memory
        self.ram = [None]*256
        self.running = True
    
    def load(self):
        address = 0
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    comment_split = line.split('#')
                    possible_num = comment_split[0]
                    if possible_num == '':
                        continue
                    if possible_num[0] == '1' or possible_num[0] == '0':
                        num = possible_num[:8]
                        #print(num)
                        self.ram[address] = int(num,2)
                        address+=1
        except FileNotFoundError:
            print(f'{sys.argv[0]}: {sys.argv[1]} not found!')

    def ram_write(self, MAR, MDR):
        self.reg[MAR] = MDR

    def ram_read(self, MAR):
        MDR = self.reg[MAR]
        return MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc+=3
        #elif op == "SUB": etc
        elif op == "MUL":
            print(self.reg[reg_a]*self.reg[reg_b])
            self.pc+=3
        elif op == "CMP":
            if reg_a == reg_b:
                self.reg[0] = 0b00000001
            elif reg_a < reg_b:
                self.reg[0] = 0b00000100
            elif reg_a > reg_b:
                self.reg[0] = 0b00000010
            self.pc+=3
        
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

    def ldi(self):
        address = self.ram[self.pc+1]
        value = self.ram[self.pc+2]
        self.reg[address] = value
        self.pc+=3
        

    def prn(self):
        address = self.ram[self.pc+1]
        print(self.reg[address])
        self.pc+=2

    def run(self):
        """Run the CPU."""
        self.load()
        LDI = 0b10000010
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        CMP = 0b10100111
        JMP = 0b01010100
        JNE = 0b01010110
        JEQ = 0b01010101
        while self.running:
            command = self.ram[self.pc]
            if command == LDI:
                print("LDI")
                self.ldi()
                
            if command == PRN:
                print("PRN")
                self.prn()
                
            if command == MUL:
                print("MUL")
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]
                self.alu("MUL", reg_a, reg_b)
                
            if command == CMP:
                print("CMP")
                reg_a = self.reg[self.ram[self.pc+1]]
                reg_b = self.reg[self.ram[self.pc+2]]
                self.alu("CMP", reg_a, reg_b)
                
            if command == JMP:
                print("JMP")
                jmp_address = self.ram[self.pc+1]
                self.pc = self.reg[jmp_address]
                
            if command == JNE:
                print("JNE")
                jmp_address = self.ram[self.pc+1]
                if self.reg[0] is not 0b00000001:
                    self.pc = self.reg[jmp_address]
                else:
                    self.pc+=2

            if command == JEQ:
                print("JEQ")
                jmp_address = self.ram[self.pc+1]
                if self.reg[0] == 0b00000001:
                    self.pc = self.reg[jmp_address]
                else:
                    self.pc+=2

            if command == HLT:
                print("HLT")
                self.running = False



