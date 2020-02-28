"""CPU functionality."""

import sys

# Operation codes
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
AND = 0b10101000
OR = 0b10101010
XOR = 0b10101011
NOT = 0b01101001
SHR = 0b10101101
SHL = 0b10101100
MOD = 0b10100100
ADDI = 0b11111111

# Flags
E = 0
L = 0
G = 0

# Pointer
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256   
        self.pc = 0

        self.branchtable = {}
        self.branchtable[LDI] = self.LDI
        self.branchtable[PRN] = self.PRN
        self.branchtable[HLT] = self.HLT
        self.branchtable[MUL] = self.alu
        self.branchtable[ADD] = self.alu
        self.branchtable[PUSH] = self.PUSH
        self.branchtable[POP] = self.POP
        self.branchtable[CALL] = self.CALL
        self.branchtable[RET] = self.RET
        self.branchtable[CMP] = self.CMP
        self.branchtable[JMP] = self.JMP
        self.branchtable[JEQ] = self.JEQ
        self.branchtable[JNE] = self.JNE
        self.branchtable[AND] = self.alu
        self.branchtable[OR] = self.alu
        self.branchtable[XOR] = self.alu
        self.branchtable[NOT] = self.alu
        self.branchtable[SHL] = self.alu
        self.branchtable[SHR] = self.alu
        self.branchtable[MOD] = self.alu
        self.branchtable[ADDI] = self.ADDI
        self.lines = 0

    def ram_read(self, mar):
        mdr = self.ram[mar]
        return mdr

    def ram_write(self, mar, value):
        self.ram[mar] = value

    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0
            # open the file
            with open(sys.argv[1]) as f:
                # Read all the lines
                for line in f:
                    # Parse out the comments
                    comment_split = line.strip().split("#")
                    # cast the numbers from strings to ints
                    value = comment_split[0].strip()
                    # ignore blank lines
                    if value == "":
                        continue
                    self.lines += 1
                    instruction = int(value, 2)
                    # populate a memory array
                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print("File not found")
            sys.exit(2)

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
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += 3        
    
    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += 2

    def HLT(self):
        sys.exit(0)

    def alu(self, op):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)

        if op == ADD:
            self.reg[op_a] += self.reg[op_b]
            self.pc += 3
        elif op == MUL:
            self.reg[op_a] *= self.reg[op_b]
            self.pc += 3
        elif op == AND:
            self.reg[op_a] &= self.reg[op_b]
            self.pc += 3
        elif op == OR:
            self.reg[op_a] |= self.reg[op_b]
            self.pc += 3
        elif op == XOR:
            self.reg[op_a] ^= self.reg[op_b]
            self.pc += 3
        elif op == NOT:
            self.reg[op_a] = ~(self.reg[op_a])
            self.pc += 2
        elif op == SHL:
            self.reg[op_a] << self.reg[op_b]
            self.pc += 3
        elif op == SHR:
            self.reg[op_a] >> self.reg[op_b]
            self.pc += 3
        elif op == MOD:
            if (self.reg[op_b] == 0):
                print("Error! Can't divide by 0.")
                sys.exit(0)
            self.reg[op_a] %= self.reg[op_b]
        else:
            raise Exception("Unsupported ALU operation.")

    def PUSH(self):
        # Grab the register argument
        reg = self.ram_read(self.pc + 1)
        val = self.reg[reg]
        # Decrement the SP
        self.reg[SP] -= 1
        # Copy the value in the given register
        self.ram_write(self.reg[SP], val)
        self.pc += 2

    def POP(self):
        # Grab the value from the top of the stack
        reg = self.ram_read(self.pc + 1)
        val = self.ram_read(self.reg[SP])
        # Copy the value from the address pointed to by SP to the given register.
        self.reg[reg] = val
        # increment SP
        self.reg[SP] += 1
        self.pc += 2

    def CALL(self):
        # push return addr on stack
        return_address = self.pc + 2
        self.reg[SP] -= 1 # decrement sp
        self.ram_write(self.reg[SP], return_address)
        # set the pc to the value in the register
        reg_num = self.ram_read(self.pc + 1)
        self.pc = self.reg[reg_num]

    def RET(self):
        # Pop the value from the top of the stack
        # store it in the PC.
        self.pc = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def CMP(self):
        E = 0
        L = 0
        G = 0
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        reg_a = self.reg[op_a]
        reg_b = self.reg[op_b]
        if (reg_a == reg_b):
            E = 1
        if (reg_a < reg_b):
            L = 1
        if (reg_a > reg_b):
            G = 1
        print("E, L, and G", (E, L, G))
        self.pc += 3    

    def JMP(self):
        # Jump to the address stored in the given register.
        # Set the PC to the address stored in the given register.
        op = self.ram_read(self.pc + 1)
        self.pc = self.reg[op]

    def JEQ(self):
        # If equal flag is set (true), jump to the address stored in the given register.
        if E == 1:
            op = self.ram_read(self.pc + 1)
            self.pc = self.reg[op]
        else:
            self.pc += 2

    def JNE(self):
        if E == 0:
            op = self.ram_read(self.pc + 1)
            self.pc = self.reg[op]
        else:
            self.pc += 2

    def ADDI(self):
        op_a = self.ram_read(self.pc + 1)
        op_b = self.ram_read(self.pc + 2)
        self.reg[op_a] += op_b
        self.pc += 3

    def run(self):
        """Run the CPU."""
        alu = [0b10100010, 0b10100000, 0b10101000, 0b10101010, 0b10101011, 0b01101001, 0b10101101, 0b10101100, 0b10100100]
        for _ in range(self.lines):
            ir = self.ram_read(self.pc)
            if (ir in alu):
                self.branchtable[ir](ir)
            else:
                self.branchtable[ir]()

