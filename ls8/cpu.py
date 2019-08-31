"""CPU functionality."""

import sys

#global operations
#ALU ops
ADD = 0b10100000 # 00000aaa 00000bbb
SUB = 0b10100001 # 00000aaa 00000bbb
MUL = 0b10100010 # 00000aaa 00000bbb
DIV = 0b10100011 # 00000aaa 00000bbb
MOD = 0b10100100 # 00000aaa 00000bbb
INC = 0b01100101 # 00000rrr
DEC = 0b01100110 # 00000rrr
CMP = 0b10100111 # 00000aaa 00000bbb
AND = 0b10101000 # 00000aaa 00000bbb
NOT = 0b01101001 # 00000rrr
OR  = 0b10101010 # 00000aaa 00000bbb
XOR = 0b10101011 # 00000aaa 00000bbb
SHL = 0b10101100 # 00000aaa 00000bbb
SHR = 0b10101101 # 00000aaa 00000bbb
ALU_OP = [ADD, SUB, MUL, DIV, MOD, INC, DEC, CMP, AND, NOT, OR, XOR, SHL, SHR]

## PC mutators
CALL = 0b01010000 # 00000rrr
RET  = 0b00010001 #
INT  = 0b01010010 # 00000rrr
IRET = 0b00010011 #
JMP  = 0b01010100 # 00000rrr
JEQ  = 0b01010101 # 00000rrr
JNE  = 0b01010110 # 00000rrr
JGT  = 0b01010111 # 00000rrr
JLT  = 0b01011000 # 00000rrr
JLE  = 0b01011001 # 00000rrr
JGE  = 0b01011010 # 00000rrr

## Other
NOP = 0b00000000
HLT = 0b00000001 
LDI  = 0b10000010 # 00000rrr iiiiiiii
LD   = 0b10000011 # 00000aaa 00000bbb
ST   = 0b10000100 # 00000aaa 00000bbb
PUSH = 0b01000101 # 00000rrr
POP  = 0b01000110 # 00000rrr
PRN  = 0b01000111 # 00000rrr
PRA  = 0b01001000 # 00000rrr

# SP = reg[7] = F3  # stack pointer (SP) is always register 7
F3 = 0b11110011

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.halt = False
        self.SP = F3

        #branch/dispatch table
        self.ops = {
            HLT: self.hlt,
            LDI: self.reg_add,
            PRN: self.print_num,
            MUL: self.mul,
            ADD: self.add,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call,
            RET: self.ret,
            JMP: self.jump,
        }
    
    def print_num(self, mar, mdr):
        #Print numeric value stored in the given register
        self.reg[mar]
    
    def reg_add(self, mar, mdr):
        #set value of a register to an integer
        self.reg[mar] = mdr
    
    def hlt(self, mar, mdr):
        self.halt = not self.halt

    def mul(self, op_a, op_b):
        self.alu("MUL", op_a, op_b)

    def add(self, op_a, op_b):
        self.alu("ADD", op_a, op_b)
    
    def push(self, mar, mdr):
        #Decrement the SP
        self.reg[7] = (self.reg[7] - 1) % 255
        # pointer is the new value in reg[7]
        self.SP = self.reg[7]
        #copy the value in the given register to the address pointed to by SP
        # value in ram = reg[PC + 1]
        self.ram[self.SP] = self.reg[mar]

    def pop(self, mar, mdr):
        #copy value from the address pointed to by SP to the given register
        self.SP = self.reg[7]
        #reg[PC + 1] = ram[pointer value]
        self.reg[mar] = self.ram[self.SP]
        #Increment SP
        self.reg[7] = (self.reg[7] + 1) % 255
    
    def call(self, op_a, op_b):
        #push reg_address to jump to: reg[op_a]
        self.push(op_a, op_b)
        # save location of next instruction to ram via SP
        self.ram[self.SP] = self.pc + 2
        #set PC address to jump to
        self.pc = self.reg[op_a]

    def ret(self, mar, mdr):
        # return to skipped instruction
        # set pc to return address
        self.pc = self.ram[self.SP]
    
    def jump(self, mar, mdr):
        self.pc = self.reg[mar]

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        address = 0
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    #get hashes from input file
                    hashes = line.split("#")
                    instruction = hashes[0]
                    #skip empty lines
                    if instruction == "":
                        continue
                    #if the instruction begins with 1 or 0 add to ram
                    first_bit = instruction[0]
                    if first_bit == "1" or first_bit == "0":
                        self.ram_write(address, int(instruction[0:8], 2))
                        address += 1
        except FileNotFoundError:
            print(f"Error: File {sys.argv[1]} not found!")
            sys.exit(2)
        except IsADirectoryError:
            print(f"Error: {sys.argv[1]} is a directory! Please choose a file")
            sys.exit(3)

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            print(self.reg[reg_a] + self.reg[reg_b])
        elif op == "MUL":
            print(self.reg[reg_a] * self.reg[reg_b])
        #elif op == "SUB": etc
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

    def run(self):
        """Run the CPU."""
        self.reg[7] = F3
        self.SP = self.reg[7]

        while not self.halt:
            #read instruction given
            ir = self.ram_read(self.pc)
         
            #save next instructions
            #values AA
            op_a = self.ram_read(self.pc + 1)
            op_b = self.ram_read(self.pc + 2)

            #track how many operands are in instruction
            #value B
            op_size = ir >> 6

            #check if op auto sets PC value
            #value C
            inst_set = ((ir >> 4) & 0b1) == 1

            #if instruction is in the dispatch table run instruction with op a and b
            if ir in self.ops:
                self.ops[ir](op_a, op_b)
            else:
                print(f"Error: Instruction {ir} not found")
                exit()
            if inst_set == False:
                self.pc += op_size + 1