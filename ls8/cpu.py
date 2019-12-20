"""CPU functionality."""
import sys
from datetime import datetime

SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xF4 # 244 in hex
        self.pc = 0
        self.fl = 0
        self.stop = False

        def LDI(a, b):
            self.reg[a] = b
        def PRN(a, b):
            print(self.reg[a])
        def JMP(a, b):
            self.pc = self.reg[a]
        def JEQ(a, b):
            if (self.fl == 1): JMP(a, b)
            else: self.pc += 2
        def JNE(a, b):
            if (self.fl != 1): JMP(a, b)
            else: self.pc += 2
        def HLT(a, b):
            self.stop = True

        self.ops = {
            0b00000000: 'NOP',
            0b00000001: HLT,
            0b10000010: LDI,
            0b01000111: PRN,
            0b01010100: JMP,
            0b01010101: JEQ,
            0b01010110: JNE
        }
    
    def ram_read(self, mar):
        if mar > 255:
            raise Exception(f"RAM does not extend to {mar}")
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        if mar > 255:
            raise Exception(f"RAM does not extend to {mar}")
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""
        if len(sys.argv) < 2:
            raise Exception("Please specify the program to load")
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                if len(line) > 0 and line[0] in ['0', '1']:
                    self.ram_write(address, int(line[:8], 2))
                    address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        def ADD(a, b):
            self.reg[a] += self.reg[b]
        def INC(a, b):
            self.reg[a] += 1
        def DEC(a, b):
            self.reg[a] -= 1
        def MUL(a, b):
            self.reg[a] *= self.reg[b]
        def CMP(a, b):
            self.fl = 0
            val_a = self.reg[a]
            val_b = self.reg[b]
            if val_a < val_b: self.fl = 4
            elif val_a > val_b: self.fl = 2
            else: self.fl = 1

        alu_opcodes = {
            0b10100000: ADD,
            0b01100101: INC,
            0b01100110: DEC,
            0b10100010: MUL,
            0b10100111: CMP
        }

        if op in alu_opcodes:
            alu_opcodes[op](reg_a, reg_b)
        else:
            raise Exception(f"{hex(op)} is not a supported ALU operation")

    def opcodes(self, op):
        if op in self.ops: return self.ops[op]
        # If it's supposed to be an ALU op, send it there
        elif (op & 0b00100000) >> 5:
            return lambda a, b: self.alu(op, a, b)
        else:
            raise Exception(f"{hex(op)} is not a supported operation")

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

        while not self.stop:

            ir = self.ram[self.pc]
            op_fn = self.opcodes(ir)  

            num_args = ir >> 6 # Grab 7th/8th bits
            operand_a = self.ram[self.pc + 1] if num_args > 0 else None
            operand_b = self.ram[self.pc + 2] if num_args > 1 else None
            
            # Skip function call if no-op
            if op_fn != 'NOP':
                op_fn(operand_a, operand_b)
            # Check if op DOESN'T set PC
            if ((ir & 0b00010000) >> 4) ^ 1: # XOR against 1 flips the bit
                self.pc += (num_args + 1)