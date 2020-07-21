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
OPERANDS_MASK = 0b11000000
ALU_MASK      = 0b00100000
PC_MASK       = 0b00010000
ID_MASK       = 0b00001111

# Offsets

OPERANDS_OFFSET = 6
ALU_OFFSET = 5

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

        self.configure_dispatch_table()

    def configure_dispatch_table(self):
        self.dispatch_table = {}

        self.dispatch_table[HLT] = self.hlt
        self.dispatch_table[LDI] = self.ldi
        self.dispatch_table[PRN] = self.prn

    @property
    def stack_pointer(self):
        return self.reg[7]

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
            pass # TODO: requires setting flags
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

    def hlt(self):
        sys.exit()

    def ldi(self, reg_num, value):
        self.reg[reg_num] = value
        
    def prn(self, reg_num):
        print(self.reg[reg_num])

    def run(self):
        """Run the CPU."""

        # Read initial instruction
        instruction_reg = self.ram_read(self.pc)

        while True:
            # Determine how many bytes in this instruction
            num_operands = instruction_reg >> OPERANDS_OFFSET
            print(f"instruction_reg: {bin(instruction_reg)}")
            print(f"num_operands: {num_operands}")

            # Determine if it is an ALU operation
            is_alu_operation = (instruction_reg & ALU_MASK) >> ALU_OFFSET

            print(f"Is alu operation: {is_alu_operation}")

            if is_alu_operation:
                if num_operands == 1:
                    self.alu(instruction_reg, self.ram_read(self.pc + 1))
                    self.pc += 2
                elif num_operands == 2:
                    self.alu(instruction_reg, self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                    self.pc += 3
                else:
                    print("Bad instruction")
                
            # If not, call appropriate function from dispatch table with proper number of operands
            elif num_operands == 0:
                self.dispatch_table[instruction_reg]()
                self.pc += 1
            elif num_operands == 1:
                self.dispatch_table[instruction_reg](self.ram_read(self.pc + 1))
                self.pc += 2
            elif num_operands == 2:
                self.dispatch_table[instruction_reg](self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3
            else:
                print("Bad instruction")

            # Read next instruction
            instruction_reg = self.ram_read(self.pc)

            


