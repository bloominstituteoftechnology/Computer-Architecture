"""CPU functionality."""

import sys

# OP code

HALT = 0b01 # 1
PRN = 0b01000111 # 71
LDI = 0b10000010 #130
MUL = 0b10100010 #162
ADD = 0b10100000 #160
PUSH = 0b01000101 # 69
POP = 0b01000110 # 70
CMP = 0b10100111 # 167
JMP = 0b01010100 # 84

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0 # program counter
        self.reg = [0] * 8 # example R0 - R7
        self.ram = [0] * 256 # list # 8 bits
        self.running = True
        self.flag = 0b00

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0

            with open(filename) as file: # reading the passed in filename
                for line in file: # for every line in the file
                    split_line = line.split('#') # we want to skip anything starting with a '#'
                    cmd = split_line[0].strip() # we also want to 

                    if cmd == '': # remove/skip any white space
                        continue

                    instruction = int(cmd, 2) # turning the string into binary with int function passing (2 args)

                    # print(f'instructions: ', instruction)
                    
                    self.ram[address] = instruction
                    address += 1
    
        except FileNotFoundError: # if an error or file not found, print this 
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found!')
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP:
            if self.reg[reg_a] == self.reg[reg_b]:
                self.flag += bin(1)
            else:
                self.flag += bin(0)
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

        self.reg[7] = 0xF4 #stack pointer

        while self.running: 
            cmd = self.ram[self.pc]

            if cmd == LDI:
                reg_location = self.ram_read(self.pc + 1)
                reg_value = self.ram_read(self.pc + 2)
                self.reg[reg_location] = reg_value
                print(self.reg[reg_location])
                self.pc += 3
            elif cmd == PRN:
                curr_val = self.ram[self.pc + 1]
                print(self.reg[curr_val])
                self.pc += 2
            elif cmd == HALT:
                self.running = False
                self.pc += 1
            elif cmd == MUL:
                reg_location = self.ram_read(self.pc + 1)
                reg_value = self.ram_read(self.pc + 2)
                self.reg[reg_location] *= self.reg[reg_value]
                self.pc += 3
            elif cmd == PUSH:
                # decrement stack pointer
                self.reg[7] -= 1
                # get the val from the register
                reg_location = self.ram[self.pc + 1]
                val = self.reg[reg_location]
                # put val at the stack pointer address in memory
                sp = self.reg[7]
                self.ram[sp] = val

                # increment program counter to put program back on track
                self.pc += 2
            elif cmd == POP:
                # get stack pointer 
                sp = self.reg[7]
                # get register num to put val in
                reg_location = self.ram[self.pc + 1]
                # use stack pointer to get the val
                val = self.ram[sp]
                # put val into given register
                self.reg[reg_location] = val
                #increment stack pointer
                self.reg[7] += 1

                # increment program counter to put program back on track
                self.pc += 2
            elif cmd == JMP:
                reg_location = self.ram_read(self.pc + 1)
                reg_value = self.ram_read(self.pc + 1)
                self.reg[reg_location] = reg_value

                self.pc += 2
            else:
                print(f'No such {cmd} exists')
                sys.exit(1)
        

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

