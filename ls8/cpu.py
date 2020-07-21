"""CPU functionality."""

# Instructions
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

OPERANDS_OFFSET = 6

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = True
        self.configure_dispatch_table()

    def configure_dispatch_table(self):
        self.dispatch_table = {}
        self.dispatch_table[LDI] = self.ldi
        self.dispatch_table[PRN] = self.prn

    def ram_read(self, address) -> int:
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value
    
    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def ldi(self, reg_num, value):
        self.reg[reg_num] = value

    def prn(self, reg_num):
        print(self.reg[reg_num])

    def run(self):
        """Run the CPU."""
        instruction_reg = self.ram_read(self.pc)
        while instruction_reg != HLT:
            num_operands = instruction_reg >> OPERANDS_OFFSET
            if num_operands == 0:
                self.dispatch_table[instruction_reg]()
                self.pc += 1
            elif num_operands == 1:
                self.dispatch_table[instruction_reg](self.ram_read(self.pc + 1))
                self.pc += 2
            elif num_operands == 2:
                self.dispatch_table[instruction_reg](self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
                self.pc += 3
            else:
                print("I don't understant the command")
            instruction_reg = self.ram_read(self.pc)
