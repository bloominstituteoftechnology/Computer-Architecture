"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.sp = 0xF4
        self.halt = False
        self.fl = 0b00000000
        self.jump_table = {}
        self.jump_table[f'{0b10000010}'] = self.LDI
        self.jump_table[f'{0b01000111}'] = self.PRN
        self.jump_table[f'{0b00000001}'] = self.HLT
        self.jump_table[f'{0b10100000}'] = self.ADD
        self.jump_table[f'{0b10100010}'] = self.MUL
        self.jump_table[f'{0b01000101}']= self.PUSH
        self.jump_table[f'{0b01000110}'] = self.POP
        self.jump_table[f'{0b01010000}'] = self.CALL
        self.jump_table[f'{0b00010001}'] = self.RET
        self.jump_table[f'{0b10100111}'] = self.CMP
        self.jump_table[f'{0b01010110}'] = self.JNE
        self.jump_table[f'{0b01010101}'] = self.JEQ
        self.jump_table[f'{0b01010100}'] = self.JEQ

       

    def load(self, filename):
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
        try:
            with open(filename) as f:
                for line in f:
                    comment_split = line.split('#')
                    num = comment_split[0].strip()
                    if num == '':
                        continue
                    instruction = int(num, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print('file not found')
            sys.exit(2)

        


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] *= self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    def ram_read(self, index):
        print(self.ram[index])
    def ram_write(self, index, value):
        self.ram[index] = value

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

    def LDI(self):
        register = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.reg[register] = value
        self.pc += 3
    
    def PRN(self):
        register = self.ram[self.pc + 1]
        print(self.reg[register])
        self.pc += 2

    def HLT(self):
        self.halt = True
        
    def ADD(self):
        value_1 = self.ram[self.pc + 1]
        value_2 = self.ram[self.pc + 2]
        self.alu('ADD', value_1, value_2)
        self.pc += 3
    def MUL(self):
        value_1 = self.ram[self.pc + 1]
        value_2 = self.ram[self.pc + 2]
        self.alu('MUL', value_1, value_2)
        self.pc += 3
    
    def PUSH(self):
        register = self.ram[self.pc + 1]
        val = self.reg[register]
        self.sp -= 1
        self.ram[self.sp] = val
        self.pc += 2
    
    def POP(self):
        register = self.ram[self.pc + 1]
        self.reg[register] = self.ram[self.sp]
        self.sp += 1
        self.pc += 2

    def CALL(self):
        return_address = self.pc + 2
        self.sp -= 1
        register = self.ram[self.pc + 1]
        self.ram[self.sp] = return_address
        self.pc = self.reg[register]

    def RET(self):
        self.pc = self.ram[self.sp]
        self.sp += 1
    
    def CMP(self):
        register_1 = self.ram[self.pc + 1]
        value_1 = self.reg[register_1]
        register_2 = self.ram[self.pc + 2]
        value_2 = self.reg[register_2]
        if value_1 == value_2:
            self.fl = 0b00000001
        elif value_1 > value_2:
            self.fl = 0b00000010
        elif value_1 < value_2:
            self.fl = 0b00000100
        self.pc += 3

    def JEQ(self):
        if self.fl == 0b00000001:
            register = self.ram[self.pc + 1]
            self.pc = self.reg[register]
        else:
            self.pc += 2
    
    def JNE(self):
        if self.fl != 0b00000001:
            register = self.ram[self.pc + 1]
            self.pc = self.reg[register]
        else:
            self.pc += 2
    
    def JMP(self):
        register = self.ram[self.pc + 1]
        self.pc = self.reg[register]
    def run(self):
        """Run the CPU."""
       
        

        while self.halt is False:
            instruction = self.ram[self.pc]
        
            if f'{instruction}' in self.jump_table:
                self.jump_table[f'{instruction}']()
            else:
                print('instruction not found', instruction)
                self.halt = True
     


