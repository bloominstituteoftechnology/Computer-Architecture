"""CPU functionality."""
 
import sys
LDI = 0b10000010 
PRN = 0b01000111 
HLT = 0b00000001
MUL = 0b10100010

PUSH = 0b01000101   
POP = 0b01000110    
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # construct RAM + REG + PC 
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0       # program counter is the address of currently executing instructions 
        self.fl = 0
        self.bt = {        
            LDI: self.op_ldi,
            PRN: self.op_prn,
            HLT: self.op_hlt,
            ADD: self.op_add,
            MUL: self.op_mul,
            POP: self.op_pop,
            PUSH: self.op_push,
            CALL: self.op_call,
            RET: self.op_ret,
            
        }

    def ram_read(self, mar):
        #mar = memory address register // mdr = memory data register 
        #read the address and write out the number (data) 
        mdr = self.ram[mar]
        return mdr
    
    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

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
        pass
