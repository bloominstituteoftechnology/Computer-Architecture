"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.sp = 7 #our stack pointer starts at the top of a 0-7 index
    
    def call_stack(self, func):
        branch_table = {
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100010: self.MULT,
            0b01100101: self.INC,
            0b01100110: self.DEC,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b00000001: self.HLT
        }
        if func in branch_table:
            branch_table[func]()
        else:
            print('invalid function')
            sys.exit(1)

    def LDI(self):
        reg_num = self.ram_read(self.pc+1)
        value = self.ram_read(self.pc+2)
        self.reg[reg_num] = value
        self.pc += 3

    def PRN(self):
        reg_num = self.ram_read(self.pc+1)
        print(self.reg[reg_num])
        self.pc += 2

    def HLT(self):
        self.running = False
        self.pc += 1

    def MULT(self):
        self.alu('MULT', self.pc+1, self.pc+2)
        self.pc += 3

    def DEC(self):
        self.alu('DEC', self.pc+1, None)

    def INC(self):
        self.alu('INC', self.pc+1, None)
    
    def PUSH(self):
        # print('push')
        #decrement SP
        self.sp -=1
        #get next value
        reg_num = self.ram[self.pc + 1]
        value = self.reg[reg_num]
        #store it
        self.ram[self.sp] = value
        self.pc += 2
    
    def POP(self):
        # print('pop')
        value = self.ram[self.sp]
        #go to next in ram
        self.reg[self.ram[self.pc + 1]] = value
        #increment sp
        self.sp +=1
        self.pc += 2

    def ram_read(self, index):
        return self.ram[index]

    def ram_write(self, index, value):
        self.ram[index] = value

    def load(self, f):
        """Load a program into memory."""
        file_path = f
        program = open(f"{file_path}", "r")
        address = 0
        for line in program:
            if line[0] == "0" or line[0] == "1":
                command = line.split("#", 1)[0]
                self.ram[address] = int(command, 2)
                address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[self.pc+1] += self.reg[self.pc+2]
        elif op == "MULT":
            self.reg[self.ram[reg_a]] *= self.reg[self.ram[reg_b]]
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
        self.running = True
        while self.running:
            ir = self.ram[self.pc]
            self.call_stack(ir)