"""CPU functionality."""

import sys

"""ALU ops"""
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100
INC = 0b01100101
DEC = 0b011001100
CMP = 0b10100111
AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101

"""PC Mutators"""
CALL = 0b01010000
RET = 0b00010001
INT = 0b01010010
IRET = 0b00010011
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
JGT = 0b01010111
JLT = 0b01011000
JLE = 0b01011001
JGE = 0b01011010

"""Other"""
NOP = 0b00000000
HLT = 0b00000001
LDI = 0b10000010
LD = 0b10000011
ST = 0b10000100
PUSH = 0b01000101
POP = 0b01000110
PRN = 0b01000111
PRA = 0b01001000

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #256 bytes of memory
        self.reg = [0] * 8 #8 general-purpose registers
        self.pc = 0 #Program Counter, the index into memory of the currently-executing instruction
        self.address = 0
        self.running = True
                
#    def handle_HLT(self):
#        self.pc += 1
#        sys.exit()
#
#    def handle_LDI(self):
#        reg_index = self.ram_read(self.pc + 1)
#        value = self.ram_read(self.pc + 2)
#        
#        self.reg[reg_index] = value
#        self.pc += 3
#
#    def handle_PRN(self):
#        reg_index = self.ram_read(self.pc + 1)
#        print(self.reg[reg_index])
#        self.pc += 2
#
#    def handle_ADD(self):
#        num_1 = self.reg[self.ram_read(self.pc + 1)]
#        num_2 = self.reg[self.ram_read(self.pc + 2)]
#
#        self.reg[self.ram_read(self.pc + 1)] = (num_1 + num_2)
#        self.pc += 3
#
#    def handle_SUB(self):
#        num_1 = self.reg[self.ram_read(self.pc + 1)]
#        num_2 = self.reg[self.ram_read(self.pc + 2)]
#
#        self.reg[self.ram_read(self.pc + 1)] = (num_1 - num_2)
#        self.pc += 3
#
#    def handle_MUL(self):
#        num_1 = self.reg[self.ram_read(self.pc + 1)]
#        num_2 = self.reg[self.ram_read(self.pc + 2)]
#
#        self.reg[self.ram_read(self.pc + 1)] = (num_1 * num_2)
#        self.pc += 3
#
#    def handle_DIV(self):
#        num_1 = self.reg[self.ram_read(self.pc + 1)]
#        num_2 = self.reg[self.ram_read(self.pc + 2)]
#
#        self.reg[self.ram_read(self.pc + 1)] = (num_1 / num_2)
#        self.pc += 3
    
    def ram_read(self, address): #accept the address to read and return the value stored there.
        return self.ram[address]
        
    def ram_write(self, value, address): #accept a value to write, and the address to write it to
        self.ram[address] = value
    
    def load(self):
        """Load a program into memory."""
        self.address = 0
        
        if len(sys.argv) < 2:
            print("Error: Insufficient arguments. Add a file from example folder into run command as arg[1]")
            sys.exit(0)
        
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
                    temp = line.split()
        
                    if len(temp) == 0:
                        continue
        
                    if temp[0][0] == '#':
                        continue
        
                    try:
                        self.ram[self.address] = int(temp[0], 2)
        
                    except ValueError:
                        print(f"Invalid number: {temp[0]}")
                        sys.exit(1)
        
                    self.address += 1
        
        except FileNotFoundError:
            print(f"Couldn't open {sys.argv[1]}")
            sys.exit(2)
        
        if self.address == 0:
            print("Program was empty!")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        a = self.reg[reg_a]
        b = self.reg[reg_b]

        if op == "ADD":
            a += b
        elif op == "SUB":
            a -= b
        elif op == "MUL":
            a *= b
        elif op == "DIV":
            a /= b
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
        while self.running:
            
            IR = self.ram_read(self.pc) #read memory address from register PC, store result in Instruction Register
            operand_a = self.ram_read(self.pc + 1) #read the bytes at pc+1 from ram
            operand_b = self.ram_read(self.pc + 2) #read the bytes at pc+2 from ram

            #depending on the value of the opcode, perform actions needed for the instruction
            if IR == HLT: #Halt the CPU (and exit the emulator).
                self.running = False
            elif IR == LDI: #Set the value of a register to an integer.
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif IR == PRN: #Print
                print(self.reg[operand_a])
                self.pc += 2
            elif IR == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
                self.pc += 3
            else:
                self.running = False
                print(f"Invalid Instruction: {IR}")

cpu = CPU()
cpu.load()
cpu.run()