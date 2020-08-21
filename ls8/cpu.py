"""CPU functionality."""

import sys
from operations import *

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #256 bytes of memory
        self.reg = [0] * 8 #8 general-purpose registers
        self.pc = 0 #Program Counter, the index into memory of the currently-executing instruction
        self.address = 0
        self.sp = len(self.reg) - 1 #stack pointer (7)
        self.flag = None
        self.running = True
    
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
        elif op == "CMP":
            if a < b:
                self.flag = LT
            elif a > b:
                self.flag = GT
            elif a == b:
                self.flag = EQ
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
                self.advance(3)
            elif IR == PRN: #Print
                print(self.reg[operand_a])
                self.advance(2)
            elif IR == MUL:
                self.reg[operand_a] *= self.reg[operand_b]
#                self.alu("MUL", operand_a, operand_b)
                self.advance(3)
            elif IR == PUSH:
                self.sp -= 1
                self.reg[self.sp] = self.reg[self.ram[self.pc + 1]] #Write value in ram at pc to the stack, then save value to stack
                self.advance(2)
            elif IR == POP:
                self.reg[self.ram[self.pc + 1]] = self.reg[self.sp] #take from stack, add to reg
                self.sp += 1
                self.advance(2)
            elif IR == RET:
                #pop off stack
                SP = self.ram[self.reg[6]]
                #set stack pointer to pointer
                self.pc = SP
                #increment the pointer
                self.reg[6] += 1
            elif IR == CALL:
                # remember where to return to and get address of next instruction
                next_inst_address = self.pc + 2
                # Decrement the pointer
                self.reg[6] -= 1
                # push onto stack
                self.ram[self.reg[6]] = next_inst_address
                self.pc = self.reg[operand_a]
            elif IR == CMP: #compare values
                self.alu("CMP", operand_a, operand_b)
                self.advance(3)
            elif IR == JMP:
                self.jump(operand_a)
            elif IR == JEQ: #JMP if equal
                if self.flag == EQ:
                    self.jump(operand_a)
                else:
                    self.advance(2)
            elif IR == JNE: #JMP if not equal
                if not self.flag == EQ:
                    self.jump(operand_a)
                else:
                    self.advance(2)
            else:
                self.running = False
                print(f"Invalid Instruction: {IR}")
    
    #Helper methods
    def jump(self, operand_a): #Jump to the address stored in the given register.
        jump = self.reg[operand_a]
        self.pc = jump #set pc to jump to that address
        
    def advance(self, amount):
        self.pc += amount

# Uncomment to test in file
#cpu = CPU()
#cpu.load()
#cpu.run()