"""CPU functionality."""

import sys

ADD = 0b10100000
AND = 0b10101000
CALL = 0b01010000
CMP = 0b10100111
DEC = 0b01100110
DIV = 0b10100011
HLT = 0b00000001
INC = 0b01100101
LDI = 0b10000010
MOD = 0b10100100
MUL = 0b10100010
NOT = 0b01101001
OR = 0b10101010
POP = 0b01000110
PRA = 0b01001000
PRN = 0b01000111
PUSH = 0b01000101
RET = 0b00010001
ST = 0b10000100
SUB = 0b10100001
SHL = 0b10101100
SHR = 0b10101101
XOR = 0b10101011

SP = 7 # register number for stack pointer

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.branch = {ADD: self.add,
                       AND: self.aand,
                       CALL: self.call,
                       CMP: self.cmp,
                       DEC: self.dec,
                       DIV: self.div,
                       INC: self.inc,
                       LDI: self.ldi,
                       MOD: self.mod,
                       MUL: self.mul,
                       NOT: self.nnot,
                       OR: self.oor,
                       POP: self.pop,
                       PRA: self.pra,
                       PRN: self.prn,
                       PUSH: self.push,
                       RET: self.ret,
                       ST: self.st,
                       SUB: self.sub,
                       SHL: self.shl,
                       SHR: self.shr,
                       XOR: self.xor,
                       }

        self.reg = bytearray(8)
        self.ram = bytearray(256)

        self.reg[SP] = 0xF4

        self.PC = 0
        self.IR = 0
        self.MAR = 0
        self.MDR = 0
        self.FL = 0

    def aand(self, reg_a, reg_b):
        """
        Bitwise-AND the values in registerA and registerB, then store the
        result in registerA.
        """
        self.alu('AND', reg_a, reg_b)

    def add(self, reg_a, reg_b):
        """
        Add the value in two registers and store the result in registerA.
        """
        self.alu('ADD', reg_a, reg_b)

    def call(self, reg_num):
        """
        Calls a subroutine (function) at the address stored in the register.

        The address of the instruction directly after CALL is pushed onto the
        stack. This allows us to return to where we left off when the
        subroutine finishes executing.

        The PC is set to the address stored in the given register. We jump to
        that location in RAM and execute the first instruction in the
        subroutine. The PC can move forward or backwards from its current
        location.
        """
        self.ldi(4, self.PC + 2)
        self.push(4)
        self.PC = self.reg[reg_num]

    def cmp(self, reg_a, reg_b):
        """
        Compare the values in two registers.

        - If they are equal, set the Equal E flag to 1, otherwise set it to 0.

        - If registerA is less than registerB, set the Less-than L flag to 1,
        otherwise set it to 0.

        - If registerA is greater than registerB, set the Greater-than G flag
        to 1, otherwise set it to 0.
        """
        self.alu('CMP', reg_a, reg_b)

    def dec(self, reg_num):
        """
        Decrement (subtract 1 from) the value in the given register.
        """
        self.alu('DEC', reg_num)

    def div(self, reg_a, reg_b):
        """
        Divide the value in the first register by the value in the second,
        storing the result in registerA.

        If the value in the second register is 0, the system should print an
        error message and halt.
        """
        self.alu('DIV', reg_a, reg_b)

    def inc(self, reg_num):
        """
        Increment (add 1 to) the value in the given register.
        """
        self.alu('INC', reg_num)

    def ldi(self, reg_num, value):
        """
        Set the value of a register to an integer.
        """
        self.reg[reg_num] = value

    def mod(self, reg_a, reg_b):
        """
        Divide the value in the first register by the value in the second,
        storing the remainder of the result in registerA.

        If the value in the second register is 0, the system should print an
        error message and halt.
        """
        self.alu('MOD', reg_a, reg_b)

    def mul(self, reg_a, reg_b):
        """
        Multiply the values in two registers together and store the result in
        registerA.
        """
        self.alu('MUL', reg_a, reg_b)

    def nnot(self, reg_num):
        """
        Perform a bitwise-NOT on the value in a register, storing the result
        in the register.
        """
        self.alu('NOT', reg_num)

    def oor(self, reg_a, reg_b):
        """
        Perform a bitwise-OR between the values in registerA and registerB,
        storing the result in registerA.
        """
        self.alu('OR', reg_a, reg_b)

    def pop(self, reg_num):
        """
        Pop the value at the top of the stack into the given register.

        1. Copy the value from the address pointed to by SP to the given
        register.

        2. Increment SP.
        """
        self.reg[reg_num] = self.ram_read(self.reg[SP])
        self.reg[SP] += 1

    def pra(self, reg_num):
        """
        Print alpha character value stored in the given register.

        Print to the console the ASCII character corresponding to the value in
        the register.
        """
        print(chr(self.reg[reg_num]))

    def prn(self, reg_num):
        """
        Print numeric value stored in the given register.

        Print to the console the decimal integer value that is stored in the
        given register.
        """
        print(self.reg[reg_num])

    def push(self, reg_num):
        """Push the value in the given register on the stack.

        1. Decrement the SP.
        2. Copy the value in the given register to the address pointed to by
        SP.
        """
        self.reg[SP] -= 1
        self.ram_write(self.reg[reg_num], self.reg[SP])

    def ret(self):
        """
        Return from subroutine.

        Pop the value from the top of the stack and store it in the PC.
        """
        self.pop(4)
        self.PC = self.reg[4]

    def shl(self, reg_a, reg_b):
        """
        Shift the value in registerA left by the number of bits specified in
        registerB, filling the low bits with 0.
        """
        self.alu('SHL', reg_a, reg_b)

    def shr(self, reg_a, reg_b):
        """
        Shift the value in registerA right by the number of bits specified in
        registerB, filling the high bits with 0.
        """
        self.alu('SHR', reg_a, reg_b)

    def st(self, reg_a, reg_b):
        """
        Store value in registerB in the address stored in registerA.
        """
        self.ram[self.reg[reg_a]] = self.reg[reg_b]

    def sub(self, reg_a, reg_b):
        """
        Subtract the value in the second register from the first, storing the
        result in registerA.
        """
        self.alu('SUB', reg_a, reg_b)

    def xor(self, reg_a, reg_b):
        """
        Perform a bitwise-XOR between the values in registerA and registerB,
        storing the result in registerA.
        """
        self.alu('XOR', reg_a, reg_b)

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

        if len(sys.argv) != 2:
            print("Usage: ls8.py <filename>")
            sys.exit()

        with open(sys.argv[1]) as file:
            program = [int(line[:line.find('#')].strip(), 2)
                       for line in file
                       if line != '\n' and line[0] != '#']

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b=None):
        """ALU operations."""

        if op == 'ADD':
            self.reg[reg_a] += self.reg[reg_b]
        elif op == 'AND':
            self.reg[reg_a] = self.reg[reg_a] & self.reg[reg_b]
        elif op == 'CMP':
            if self.reg[reg_a] < self.reg[reg_b]:
                self.FL = 0b00000100
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.FL = 0b00000010
            else:
                self.FL = 0b00000001
        elif op == 'DEC':
            self.reg[reg_a] -= 1
        elif op == 'DIV':
            self.reg[reg_a] = self.reg[reg_a] // self.reg[reg_b]
        elif op == 'INC':
            self.reg[reg_a] += 1
        elif op == 'MOD':
            self.reg[reg_a] = self.reg[reg_a] % self.reg[reg_b]
        elif op == 'MUL':
            self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]
        elif op == 'NOT':
            self.reg[reg_a] = 0b11111111 - self.reg[reg_a]
        elif op == 'OR':
            self.reg[reg_a] = self.reg[reg_a] | self.reg[reg_b]
        elif op == 'SUB':
            self.reg[reg_a] = self.reg[reg_a] - self.reg[reg_b]
        elif op == 'SHL':
            self.reg[reg_a] = self.reg[reg_a] << self.reg[reg_b]
        elif op == 'SHR':
            self.reg[reg_a] = self.reg[reg_a] >> self.reg[reg_b]
        elif op == 'XOR':
            self.reg[reg_a] = self.reg[reg_a] ^ self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.PC,
            #self.fl,
            #self.ie,
            self.ram_read(self.PC),
            self.ram_read(self.PC + 1),
            self.ram_read(self.PC + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')
        print()

    def run(self):
        """Run the CPU."""
        self.IR = self.ram_read(self.PC)
        operand_a = self.ram_read(self.PC + 1)
        operand_b = self.ram_read(self.PC + 2)

        while self.IR != HLT:
            num_args = (self.IR & 0b11000000) >> 6
            pc_set = (self.IR & 0b00010000) >> 4
            try:
                if num_args == 0:
                    self.branch[self.IR]()
                elif num_args == 1:
                    self.branch[self.IR](operand_a)
                else:
                    self.branch[self.IR](operand_a, operand_b)
            except KeyError:
                raise Exception("Unsupported operation.")

            if pc_set == 0:
                self.PC += num_args + 1

            self.IR = self.ram_read(self.PC)
            operand_a = self.ram_read(self.PC + 1)
            operand_b = self.ram_read(self.PC + 2)
