"""CPU functionality."""
# py ls8.py examples/sctest.ls8
import sys
import time

LDI =  0b10000010
PRN =  0b01000111
HLT =  0b00000001
MUL =  0b10100010
PUSH = 0b01000101
POP =  0b01000110
CMP =  0b10100111
JMP =  0b01010100
JEQ =  0b01010101
JNE =  0b01010110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.reg[7] = 255 # R7 is reserved as the stack pointer (SP)
        self.ram = [0] * 256
        self.fla = [0] * 8 # `FL` bits: `00000LGE`
        self.hlt = False


        self.ops = {
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            MUL: self.op_mul,
            PUSH: self.op_push,
            POP: self.op_pop,
            CMP: self.op_cmp,
            JMP: self.op_jmp,
            JEQ: self.op_jeq,
            JNE: self.op_jne
        }

    # op functions
    def op_ldi(self, address, value):
        self.reg[address] = value

    def op_prn(self, address, op_b): # op a/b
        print(self.reg[address]) # op_a acts as address

    def op_hlt(self, op_a, op_b):
        self.hlt = True
    
    def op_mul(self, operand_a, operand_b):
        self.alu('MUL', operand_a, operand_b)

    def op_push (self, operand_a, operand_b):
        self.reg[7] -= 1 # decrement stack pointer
        sp = self.reg[7] # sp variable
        self.ram[sp] = self.reg[operand_a]

    def op_pop (self, operand_a, operand_b):
        sp = self.reg[7] # sp variable        
        operand_b = self.ram[sp]
        self.reg[operand_a] = operand_b

    def op_jmp(self, address, operand_b):
        self.pc = self.reg[address]

    def op_cmp(self, operand_a, operand_b):
        value1 = self.reg[operand_a]
        value2 = self.reg[operand_b]
        if value1 < value2:
            self.fla[5] = 1
        elif value1 > value2:
            self.fla[6] = 1
        elif value1 == value2:
            self.fla[7] = 1
        else: print('Non-comparable values')
        # `FL` bits: `00000LGE`

    def op_jeq(self, operand_a, operand_b):
        if self.fla[7] == 1:
            self.op_jmp(operand_a, operand_b)
        else:
            self.pc += 2

    def op_jne(self, operand_a, operand_b):
        if self.fla[7] == 0:
            self.op_jmp(operand_a, operand_b)
        else:
            self.pc += 2

    # ram functions 

    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self, filename):
        """Load a program into memory."""

        address = 0
        with open(filename) as file:
            for line in file:
                comment_split = line.split('#') # used to ignore comments
                instruction = comment_split[0]
                if instruction == '':
                    continue
                elif (instruction[0] == '0') or (instruction[0] == '1'):
                    self.ram[address] = int(instruction[:8], 2)
                    address += 1

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
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

        print()

    def run(self):
        """Run the CPU."""
        while self.hlt == False:
            #self.trace()
            #time.sleep(1)
            ir = self.ram[self.pc]
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            op_size = ir >> 6
            ins_set = ((ir >> 4) & 0b1) == 1
            if ir in self.ops:
                self.ops[ir](operand_a, operand_b)
            if not ins_set:
                self.pc += op_size + 1