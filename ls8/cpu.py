"""CPU functionality."""

import sys

# Instruction Set

ADD  = 0b10100000
AND  = 0b10101000
CALL = 0b01010000
CMP  = 0b10100111
DEC  = 0b01100110
DIV  = 0b10100011
HLT  = 0b00000001
INC  = 0b01100101
INT  = 0b01010010
IRET = 0b00010011
JEQ  = 0b01010101
JGE  = 0b01011010
JGT  = 0b01010111
JLE  = 0b01011001
JLT  = 0b01011000
JMP  = 0b01010100
JNE  = 0b01010110
LD   = 0b10000011
LDI  = 0b10000010
MOD  = 0b10100100
MUL  = 0b10100010
NOP  = 0b00000000
NOT  = 0b01101001
OR   = 0b10101010
POP  = 0b01000110
PRA  = 0b01001000
PRN  = 0b01000111
PUSH = 0b01000101
RET  = 0b00010001
SHL  = 0b10101100
SHR  = 0b10101101
ST   = 0b10000100
SUB  = 0b10100001
XOR  = 0b10101011

# Bit Masks

ALU_MASK = 0b00100000
PC_MASK  = 0b00010000

L_MASK   = 0b00000100
G_MASK   = 0b00000010
E_MASK   = 0b00000001

# Offsets

OPERANDS_OFFSET = 6
ALU_OFFSET = 5
PC_OFFSET = 4

L_OFFSET = 2
G_OFFSET = 1

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.fl = 0
        self.stack_pointer = 0xF7
        self.configure_dispatch_table()

    def configure_dispatch_table(self):
        self.dispatch_table = {}

        self.dispatch_table[CALL] = self.call
        self.dispatch_table[HLT] = self.hlt
        self.dispatch_table[JEQ] = self.jeq
        self.dispatch_table[JMP] = self.jmp
        self.dispatch_table[JNE] = self.jne
        self.dispatch_table[LD] = self.ld
        self.dispatch_table[LDI] = self.ldi
        self.dispatch_table[POP] = self.pop
        self.dispatch_table[PRA] = self.pra
        self.dispatch_table[PRN] = self.prn
        self.dispatch_table[PUSH] = self.push
        self.dispatch_table[RET] = self.ret
        self.dispatch_table[ST] = self.st

    @property
    def stack_pointer(self):
        return self.reg[7]
    
    @stack_pointer.setter
    def stack_pointer(self, value):
        value &= 0xff
        self.reg[7] = value

    @property
    def interrupt_status(self):
        return self.reg[6]

    @interrupt_status.setter
    def interrupt_status(self, value):
        self.reg[6] = value

    @property
    def interrupt_mask(self):
        return self.reg[5]

    @interrupt_mask.setter
    def interrupt_mask(self, value):
        self.reg[5] = value
        
    def ram_read(self, address) -> int:
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
    
    def load(self, path):
        """Load a program into memory."""

        address = 0

        with open(path) as program:
            for line in program:
                line = line.split('#',1)[0]

                try:
                    instruction = int(line, 2)
                    self.ram[address] = instruction
                    address += 1
                except ValueError:
                    pass

    def alu(self, op, a, b = None):
        """ALU operations."""
        if op == ADD:
            self.reg[a] = self.reg[a] + self.reg[b]
        elif op == AND:
            self.reg[a] = self.reg[a] & self.reg[b]
        elif op == CMP:
            if self.reg[a] < self.reg[b]:
                self.fl = L_MASK
            elif self.reg[a] > self.reg[b]:
                self.fl = G_MASK
            else:
                self.fl = E_MASK
        elif op == DEC:
            self.reg[a] -= 1
        elif op == DIV:
            if self.reg[b] == 0:
                raise ValueError("Cannot divide by 0")
            self.reg[a] = self.reg[a] // self.reg[b] # is this correct, using the floor division?
        elif op == INC:
            self.reg[a] += 1
        elif op == MOD:
            self.reg[a] = self.reg[a] % self.reg[b]
        elif op == MUL:
            self.reg[a] = self.reg[a] * self.reg[b]
        elif op == NOT:
            self.reg[a] = ~self.reg[a]
        elif op == OR:
            self.reg[a] = self.reg[a] | self.reg[b]
        elif op == SHL:
            self.reg[a] = self.reg[a] << self.reg[b]
        elif op == SHR:
            self.reg[a] = self.reg[a] >> self.reg[b]
        elif op == SUB:
            self.reg[a] = self.reg[a] - self.reg[b]
        elif op == XOR:
            self.reg[a] = self.reg[a] ^ self.reg[b]
        else:
            raise Exception("Unsupported ALU operation")

        self.reg[a] &= 0xff # Make sure we are staying within the 8 bit limit of our registers

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

    def call(self, a):
        # push address of instruction at pc + 2 to the stack
        self.stack_pointer -= 1
        self.ram_write(self.stack_pointer, self.pc + 2)
        # set pc to address in reg a
        self.pc = self.reg[a]

    def hlt(self):
        sys.exit()

    def jeq(self, a):
        if self.fl & E_MASK:
            self.pc = self.reg[a]
        else:
            self.pc += 2

    def jmp(self, a):
        self.pc = self.reg[a]

    def jne(self, a):
        if not self.fl & E_MASK:
            self.pc = self.reg[a]
        else:
            self.pc += 2

    def ld(self, a, b):
        self.reg[a] = self.ram_read(self.reg[b])

    def ldi(self, a, value):
        self.reg[a] = value

    def pop(self, a):
        self.reg[a] = self.ram_read(self.stack_pointer)
        self.stack_pointer += 1

    def pra(self, a):
        print(chr(self.reg[a]))

    def prn(self, a):
        print(self.reg[a])

    def push(self, a):
        self.stack_pointer -= 1
        self.ram_write(self.stack_pointer, self.reg[a])
    
    def ret(self):
        # Pop address from stack and set pc to that address
        self.pc = self.ram_read(self.stack_pointer)
        self.stack_pointer += 1

    def st(self, a, b):
        self.ram_write(self.reg[a], self.reg[b])

    def run(self):
        """Run the CPU."""

        # Read initial instruction
        instruction_reg = self.ram_read(self.pc)

        while True:
            # Determine how many bytes in this instruction
            num_operands = instruction_reg >> OPERANDS_OFFSET
            
            # print(f"instruction_reg: {bin(instruction_reg)}")
            # print(f"num_operands: {num_operands}")

            # Determine if it is an ALU operation
            is_alu_operation = (instruction_reg & ALU_MASK) >> ALU_OFFSET

            # print(f"Is alu operation: {is_alu_operation}")

            if is_alu_operation:
                if num_operands == 1:
                    self.alu(instruction_reg, self.ram_read(self.pc + 1))
                elif num_operands == 2:
                    self.alu(instruction_reg, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                else:
                    print("Bad instruction")
                
            # If not, call appropriate function from dispatch table with proper number of operands
            elif num_operands == 0:
                self.dispatch_table[instruction_reg]()
            elif num_operands == 1:
                self.dispatch_table[instruction_reg](self.ram_read(self.pc + 1))
            elif num_operands == 2:
                self.dispatch_table[instruction_reg](self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            else:
                print("Bad instruction")

            # Detrmine if the instruction set the PC
            sets_pc = (instruction_reg & PC_MASK) >> PC_OFFSET

            # Increment the PC accordingly
            if not sets_pc:
                self.pc += num_operands + 1

            # Read next instruction
            instruction_reg = self.ram_read(self.pc)

            


