"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET  = 0b00010001

CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        # Set RAM
        self.ram = [0] * 256
        # Create registers
        self.reg = [0] * 8
        self.reg[7] = 0XF4 
        self.reg[6] = 0         
        # Set program counter to 0
        self.pc = 0
        self.running = True 
       
        self.branchtable = {
            HLT: self.hlt,
            LDI: self.ldi,
            PRN: self.prn,
            PUSH: self.push,
            POP: self.pop,
            CALL: self.call, 
            RET: self.ret,
            JEQ: self.jeq,
            JNE: self.jne,
            JMP: self.jmp,
        }
        

    def load(self):
        """Load a program into memory."""

        try: 
            with open(sys.argv[1]) as f:
                address = 0
                for line in f:
                    maybe_binary_number = line[:line.find('#')]
                    if maybe_binary_number == '':
                        continue
                    denary_int = int(maybe_binary_number, 2)
                    self.ram[address] = denary_int
                    address += 1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: {sys.argv[1]} not found ')
            sys.exit()

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == ADD:
            self.reg[reg_a] += self.reg[reg_b]
        elif op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == CMP: # compare 
            if self.reg[reg_a] < self.reg[reg_b]:
                self.reg[6] = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.reg[6] = 0b00000010
            else:
                self.reg[6] = 0b00000001
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value


    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
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
        IR = []
        self.running = True 
        while self.running:
            IR = self.ram[self.pc]
            num_args = IR >> 6
            is_alu_op = (IR >> 5) & 0b001
            operand_a = self.ram_read(self.pc+1) 
            operand_b = self.ram_read(self.pc+2)
            is_alu_op = (IR >> 5) & 0b001 == 1
            if is_alu_op:
                self.alu(IR, operand_a, operand_b)
            else:
                self.branchtable[IR](operand_a, operand_b)
            # check if command sets PC directly
            sets_pc = (IR >> 4) & 0b0001 == 1
            if not sets_pc:
                self.pc += 1 + num_args

    def hlt(self, operand_a, operand_b):
        self.running = False


    def ldi(self, operand_a, operand_b):
        self.reg[operand_a] = operand_b


    def prn(self, operand_a, operand_b):
        print(self.reg[operand_a])

    def jmp(self, operand_a, operand_b):
        reg_idx = self.reg[operand_a]
        self.pc = reg_idx

    
    def jeq(self, operand_a, operand_b):

        flags = self.reg[6]
        equal_is_flagged = (flags << 7) & 0b10000000 == 128
        if equal_is_flagged:
            # jump to address stored in reg
            given_reg_value = self.reg[operand_a]
            self.pc = given_reg_value
        else:
            self.pc += 2


    def jne(self, operand_a, operand_b):

        flags = self.reg[6]
        equal_is_flagged = flags == 1
        if equal_is_flagged:
            self.pc += 2
        else:
            # jump to address stored in reg
            given_reg_value = self.reg[operand_a]
            self.pc = given_reg_value


    def push(self, operand_a, operand_b):
        self.reg[7] -= 1
        # copy the value in the given register to the address pointed to by SP
        value = self.reg[operand_a]
        # copy to the address at stack pointer
        SP = self.reg[7]
        self.ram[SP] = value


    def pop(self, operand_a, operand_b):
        SP = self.reg[7]
        value = self.ram[SP]
        # Copy the value from the address pointed to by SP to the given register.
        self.reg[operand_a] = value
        self.reg[7] += 1


    def call(self, operand_a, operand_b):
        # PUSH
        return_address = self.pc + 2

        self.reg[7] -= 1

        SP = self.reg[7]
        self.ram[SP] = return_address
        reg_idx = self.ram[self.pc+1]
        subroutine_address = self.reg[reg_idx]

        self.pc = subroutine_address 


    def ret(self, operand_a, operand_b):
        # Return from subroutine.
        # Pop value from top of stack 
        SP = self.reg[7]
        return_address = self.ram[SP]
        # store it in pc
        self.pc = return_address
        self.reg[7] += 1