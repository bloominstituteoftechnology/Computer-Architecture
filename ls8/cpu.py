"""CPU functionality."""
import os
import sys

from examples import *

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
ADD = 0b10100000
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111 
JMP = 0b01010100 
JEQ = 0b01010101
JNE = 0b01010110
L_MASK = 0b00000100
G_MASK = 0b00000010 
E_MASK = 0b00000001 



class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.running = False
        self.registers = [0] * 8
        self.pc = 0
        self.sp = 7

        self.branchtable = {}
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[HLT] = self.hlt
        self.branchtable[ADD] = self.add
        self.branchtable[MUL] = self.mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call 
        self.branchtable[RET] = self.ret

        self.branchtable[CMP] = self.cmp 
        self.branchtable[JMP] = self.jmp 
        self.branchtable[JEQ] = self.jeq 
        self.branchtable[JNE] = self.jne 

        self.fl = 0






    def ram_read(self,val):
        print(self.ram[val])
    
    def ram_write(self, val, address):
        self.ram[address] = val

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]

        elif op == "CMP":
            self.fl = 0b00000000
            if self.registers[reg_a] == self.registers[reg_b]:
                self.fl = E_MASK 
            elif self.registers[reg_a] < self.registers[reg_b]:
                self.fl = L_MASK
            elif self.registers[reg_a] > self.registers[reg_b]:
                self.fl = G_MASK

        else:
            raise Exception("Unsupported ALU operation")


    def operation(self, op):
        op_a = self.ram[self.pc + 1]
        op_b = self.ram[self.pc + 2]
        self.alu(op, op_a, op_b)
        self.pc +=3

    def load_memory(self): 
        if len(sys.argv) != 2:
            print("Usage ls8.py filename.ls8")
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split('#')
                    cleaned = split_line[0].strip()

                    if cleaned == '':
                        continue
                    try:
                        cleaned = int(cleaned, 2)
                    except ValueError:
                        print(f'{cleaned} is not a valid value')
                        sys.exit(1) 

                    self.ram_write(cleaned, address)
                    address +=1

        except FileNotFoundError:
            print(f'{sys.argv[1]} does not exist')
            sys.exit(2)

        # print("Usage: enter in a filename....")

    # commands in branch table
    def ldi(self):
        # gets the address for registry
        operand_a = self.ram[self.pc + 1]
        # gets the value for the registry
        operand_b = self.ram[self.pc + 2]
        # Assign value to Reg Key
        self.registers[operand_a] = operand_b
        # Update PC
        self.pc += 3

    def prn(self):
        # get the address we want to print
        operand_a = self.ram[self.pc + 1]
        # Print Reg
        print(self.registers[operand_a])
        # Update PC
        self.pc += 2

    def hlt(self):
        # Exit Loop
        self.running = False
        # Update PC
        self.pc += 1

    def add(self):
        self.operation("ADD")

    def mul(self):
        self.operation("MUL")

    def push(self):
        given_register = self.ram[self.pc + 1]
        value_in_register = self.registers[given_register]
        # Decrement the stack pointer
        self.registers[self.sp] -= 1
        # Write the value of the given register to memory at SP location
        self.ram[self.registers[self.sp]] = value_in_register
        self.pc += 2

    def pop(self):
        given_register = self.ram[self.pc + 1]
        # write the value in memory at the top of stack to the given register
        value_from_memory = self.ram[self.registers[self.sp]]
        self.registers[given_register] = value_from_memory
        # increment the stack pointer
        self.registers[self.sp] += 1
        self.pc += 2

    def call(self):
        # Get the given register in the operand
        given_register = self.ram[self.pc + 1]
        # Store the return address (PC + 2) onto the stack
        # decrement the stack pointer
        self.registers[self.sp] -= 1
        # write the return address
        self.ram[self.registers[self.sp]] = self.pc + 2
        # set pc to the value inside the given_register
        self.pc = self.registers[given_register]

    def ret(self):
        # set the pc to the value at the top of the stack
        self.pc = self.ram[self.registers[self.sp]]
        # pop from stack
        self.registers[self.sp] += 1

    
    def cmp(self):
        op_a = self.ram[self.pc + 1]
        op_b = self.ram[self.pc + 2]
        self.alu("CMP", op_a, op_b)
        self.pc += 3

    def jmp(self):
        self.pc += 1
        given_register = self.ram[self.pc]
        self.pc = self.registers[given_register]

    def jeq(self):
        given_register = self.ram[self.pc + 1]
        if self.fl == E_MASK:
            self.pc = self.registers[given_register]
        else:
            self.pc += 2

    def jne(self):
        given_register = self.ram[self.pc + 1]
        if self.fl != E_MASK:
            self.pc = self.registers[given_register]
        else:
            self.pc += 2

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
            IR = self.pc
            
            instance = self.ram[IR]

            try:
                self.branchtable[instance]()

            except KeyError:
                print(f'KeyError at {self.registers[self.ram[instance]]}')
                sys.exit(1)


# c = CPU()
# c.load_memory(sys.argv[1])
