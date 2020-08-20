"""CPU functionality."""

import sys

program_filename = sys.argv[1]
# print(sys.argv[1])

"""ALU ops"""
ADD = 0b10100000
SUB = 0b10100001
MUL = 0b10100010
DIV = 0b10100011
MOD = 0b10100100

INC = 0b01100101
DEC = 0b011001100

CMP = 0b10100111


AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101

"""PC Mutators"""
CALL = 0b01010000
RET = 0b00010001

INT = 0b01010010
IRET = 0b00010011

JMP = 0b01010100
JEQ = 0b01010101
JNE = 0b01010110
JGT = 0b01010111
JLT = 0b01011000
JLE = 0b01011001

JGE = 0b01011010

"""Other"""
NOP = 0b00000000

HLT = 0b00000001

LDI = 0b10000010

LD = 0b10000011
ST = 0b10000100

PUSH = 0b01000101
POP = 0b01000110

PRN = 0b01000111
PRA = 0b01001000


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.fl = 0
        self.address = 0
        self.op_size = 0
        # The stack pointer (SP) is stored at R7 which when intialized points to address 0xF4 in RAM
        self.reg[6] = 0xF4
        self.running = True
        self.branch_table = {
            0b00000001: self.HLT,
            0b10000010: self.LDI,
            0b01000111: self.PRN,
            0b10100000: self.ADD,
            0b10100001: self.SUB,
            0b10100010: self.MUL,
            0b10100100: self.DIV,
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET
        }

    def HLT(self):
        self.pc += 1
        sys.exit()

    def LDI(self):
        reg_idx = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_idx] = value

        self.pc += 3

    def PRN(self):
        reg_idx = self.ram_read(self.pc + 1)
        print(self.reg[reg_idx])

        self.pc += 2

    def ADD(self):
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2 = self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = (num_1 + num_2)

        self.pc += 3

    def SUB(self):
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2 = self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = (num_1 - num_2)

        self.pc += 3

    def MUL(self):
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2 = self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = (num_1 * num_2)

        self.pc += 3

    def DIV(self):
        num_1 = self.reg[self.ram_read(self.pc + 1)]
        num_2 = self.reg[self.ram_read(self.pc + 2)]

        self.reg[self.ram_read(self.pc + 1)] = (num_1 // num_2)

        self.pc += 3

    def PUSH(self):
        self.reg[6] -= 1
        # print('$$$$$$$', self.sp)

        reg_num = self.ram_read(self.pc + 1)

        value_to_push = self.reg[reg_num]

        stack_address = self.reg[6]

        self.ram_write(value_to_push, stack_address)

        self.pc += 2

    def POP(self):
        value_to_pop = self.ram_read(self.reg[6])

        self.reg[6] += 1

        reg_num = self.ram_read(self.pc + 1)

        self.reg[reg_num] = value_to_pop

        self.pc += 2

    def CALL(self):
        return_address = self.pc + 2

        self.reg[6] -= 1

        self.ram[self.reg[6]] = return_address

        self.pc = self.reg[self.ram_read(self.pc + 1)]

    def RET(self):
        SP = self.ram[self.reg[6]]
        self.pc = SP
        self.reg[6] += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        self.address = 0

        try:
            with open(program_filename) as f:

                for line in f:
                    line = line.split('#')
                    # print(line)
                    line = line[0].strip()
                    # print(line)

                    if line == '':
                        continue

                    value = int(line, 2)
                    # print(value)

                    self.ram[self.address] = value

                    self.address += 1

        except FileNotFoundError:
            print(
                f"The file {sys.argv[1]} does not exist. Please enter a valid file name.")
            sys.exit()

        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010,  # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111,  # PRN R0
        #     0b00000000,
        #     0b00000001,  # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        while self.running:

            IR = self.ram_read(self.pc)
            # op_size = ((IR >> 6) & 0b11) + 1

            if IR in self.branch_table:

                self.branch_table[IR]()
                # self.pc += op_size

                # if (IR >> 4) != 1:
                #     self.pc += (IR >> 6) + 1

                # # Add code to advance the PC to the address of the subroutine called
                # else:
                #     self.pc = 0

        # operand_a = self.ram_read(self.pc + 1)
        # operand_b = self.ram_read(self.pc + 2)

        # if IR == HLT:
        #     self.running = False

        # elif IR == LDI:
        #     self.reg[operand_a] = operand_b
        #     self.pc += 3

        # elif IR == PRN:
        #     print(self.reg[operand_a])
        #     self.pc += 2

        # elif IR == ADD:
        #     self.alu("ADD", operand_a, operand_b)
        #     self.pc += 3

        # elif IR == SUB:
        #     self.alu("SUB", operand_a, operand_b)
        #     self.pc += 3

        # elif IR == MUL:
        #     self.alu("MUL", operand_a, operand_b)
        #     self.pc += 3

        # elif IR == DIV:
        #     self.alu("DIV", operand_a, operand_b)
        #     self.pc += 3
