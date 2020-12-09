"""CPU functionality."""

import sys
import time
import traceback

IM = 5
IS = 6
SP = 7

HLT = 0b0001
LDI = 0b0010
ST = 0b0100
PUSH = 0b0101
POP = 0b0110
PRN = 0b0111
PRA = 0b1000

CALL = 0b0000
RET = 0b0001
INT = 0b0010
IRET = 0b0011
JMP = 0b0100

ALU_ADD = 0b0000
ALU_SUB = 0b0001
ALU_MUL = 0b0010
ALU_DIV = 0b0011
ALU_MOD = 0b0100
ALU_INC = 0b0101
ALU_DEC = 0b0110
ALU_CMP = 0b0111
ALU_AND = 0b1000
ALU_NOT = 0b1001
ALU_OR = 0b1010
ALU_XOR = 0b1011
ALU_SHL = 0b1100
ALU_SHR = 0b1101

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[SP] = 0xf4
        self.pc = 0
        self.fl = 0
        # these aren't mentioned in the spec
        # but there didn't seem to be a suitable place to put them
        self.start_time = 0
        self.time = 0

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] += val
    
    def push(self, val):
        self.reg[SP] -= 1
        self.ram[self.reg[SP]] = val

    def pop(self):
        val = self.ram[self.reg[SP]]
        self.reg[SP] += 1
        return val

    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram[address] = instruction
            address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        def add(): self.reg[reg_a] += self.reg[reg_b]
        def sub(): self.reg[reg_a] -= self.reg[reg_b]
        def mul(): self.reg[reg_a] *= self.reg[reg_b]
        def div():
            if reg_b == 0:
                raise "Can't divide by 0"
            self.reg[reg_a] //= self.reg[reg_b]
        # def mod(a, b): self.reg[a] %= self.reg[b]
            

        ALU_INSTRUCTIONS = {
            ALU_ADD: add,
            ALU_SUB: sub,
            ALU_MUL: mul,
            ALU_DIV: div,
            # ALU_MOD: lambda a, b: self.reg[a] % self.reg[b],
            # ALU_INC: lambda a: self.reg[a] + 1,
            # ALU_DEC: lambda a: self.reg[a] - 1,
            # ALU_CMP: lambda a, b: self.reg[a] == self.reg[b],
            # ALU_AND: lambda _: ,
            # ALU_NOT: lambda _: ,
            # ALU_OR: lambda _: ,
            # ALU_XOR: lambda _: ,
            # ALU_SHL: lambda _: ,
            # ALU_SHR: lambda _: ,
        }

        if op in ALU_INSTRUCTIONS:
            ALU_INSTRUCTIONS[op]()
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
        try:
            self.start_time = time.time()
            while True:
                self.reg[IS] = 0
                # timer interrupt status
                self.time = time.time()
                if self.time >= self.start_time + 1:
                    self.start_time += ((self.time - self.start_time) // 1)
                    self.reg[IS] |= 1 # timer interrupt bit
                
                # keyboard interrupt status
                # TODO

                # check interrupts
                maskedInterrupts = self.reg[IS] & self.reg[IM]
                for bit in range(8):
                    if (maskedInterrupts >> bit) & 1:
                        self.reg[IS] & ~(1 << bit)
                        self.push(self.pc)
                        self.push(self.fl)
                        for reg in range(7):
                            self.push(self.reg[reg])
                        # go to interrupt handler from interrupt address table
                        self.pc = self.ram[0xf8 + bit]
                        # disable further interrupts
                        self.reg[IM] = 0
                        break

                ir = self.ram_read(self.pc)
                
                self.pc += 1
                
                instruction = ir & 0b1111
                is_alu = (ir >> 5) & 1
                sets_pc = (ir >> 4) & 1
                operand_count = ir >> 6

                op_position = self.pc
                operands = (self.ram_read(op_position + i) for i in range(operand_count))
                self.pc += operand_count
                
                if is_alu:
                    self.alu(instruction, next(operands), next(operands))
                elif sets_pc:
                    def call():
                        self.push(self.pc)
                        self.pc = self.reg[next(operands)]
                    def ret(): self.pc = self.pop()
                    def jmp(): self.pc = self.reg[next(operands)]
                    def int_(): self.reg[IS] |= 1 << self.reg[next(operands)]
                    def iret():
                        for reg in reversed(range(7)):
                            self.reg[reg] = self.pop()
                        self.fl = self.pop()
                        self.pc = self.pop()
                        self.reg[IM] = ~0

                    INSTRUCTIONS = {
                        CALL: call,
                        RET: ret,
                        JMP: jmp,
                        INT: int_,
                        IRET: iret
                    }

                    if instruction in INSTRUCTIONS:
                        INSTRUCTIONS[instruction]()
                    else:
                        raise Exception(f"UNRECOGNIZED INSTRUCTION: {instruction:b}")
                elif instruction == HLT:
                    break
                else:
                    def ldi():
                        a = next(operands)
                        b = next(operands)
                        self.reg[a] = b
                    def prn(): print(self.reg[next(operands)])
                    def pra(): print(chr(self.reg[next(operands)]))
                    def push(): self.push(self.reg[next(operands)])
                    def pop(): self.reg[next(operands)] = self.pop()
                    def st():
                        a = next(operands)
                        b = next(operands)
                        self.ram[self.reg[a]] = self.reg[b]
                    
                    INSTRUCTIONS = {
                        LDI: ldi,
                        PRN: prn,
                        PRA: pra,
                        PUSH: push,
                        POP: pop,
                        ST: st,
                    }

                    if instruction in INSTRUCTIONS:
                        INSTRUCTIONS[instruction]()
                    else:
                        raise Exception(f"UNRECOGNIZED INSTRUCTION: {instruction:b}")
        except Exception as e:
            print(f"ERROR OCCURED: {e}")
            traceback.print_exc()
            self.trace()
