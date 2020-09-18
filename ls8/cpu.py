"""CPU functionality."""

import sys

#week project
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000

# sprint
# FL bits: 00000LGE
# L Less-than: in a CMP, set to 1 if registerA < registerB,  otherwise is zero.
# G Greater-than: during a CMP, set to 1 if registerA > registerB, otherwise zero.
# E Equal: in a CMP, set to 1 if registerA == registerB, otherwise zero.
L_MASK = 0b00000100
G_MASK = 0b00000010
E_MASK = 0b00000001
# instructions
CMP = 0b10100111
JMP = 0b01010100
JNE = 0b01010110
JEQ = 0b01010101

# stretch problems
AND = 0b10101000
OR = 0b10101010
NOT = 0b01101001
XOR = 0b10101011
SHL = 0b10101100
SHR = 0b10101101
MOD = 0b10100100


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        # stack pointer
        self.sp = 7
        self.pc = 0
        self.running = False
        self.branchtable = {}
        self.branchtable[HLT] = self.hlt
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[PUSH] = self.push
        self.branchtable[POP] = self.pop
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[ADD] = self.add
        # sprint
        self.branchtable[CMP] = self.cmp
        self.branchtable[JMP] = self.jmp
        self.branchtable[JNE] = self.jne
        self.branchtable[JEQ] = self.jeq
        # flag
        self.flag = 0

   

    def ram_read(self, MAR):
        # accept address, read it, and return value 
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        # accept a value to write, an address to write to
        # MAR is memory address register, MDR is memory data register
        # write the value -> MDR to the address MAR
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0

        #hardcoded program:
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.strip().split("#", 1)[0]
                        line = int(line, 2)
                        self.ram[address] = line
                        address += 1
                    except ValueError:
                        pass
        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")
            sys.exit(1)
        except IndexError:
            print("Usage: ls8.py filename")
            sys.exit(1)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]

        elif op == "CMP":
            if self.reg[reg_a] < self.reg[reg_b]:
                self.flag = L_MASK
            elif self.reg[reg_a] > self.reg[reg_b]:
                self.flag = G_MASK
            else:
                self.flag = E_MASK
    
    def operation_helper(self, op):
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.alu(op, operand_a, operand_b)
        self.pc += 3



    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(
            f"TRACE: %02X | %02X %02X %02X |"
            % (
                self.pc,
                # self.fl,
                # self.ie,
                self.ram_read(self.pc),
                self.ram_read(self.pc + 1),
                self.ram_read(self.pc + 2),
            ),
            end="",
        )

        for i in range(8):
            print(" %02X" % self.reg[i], end="")

        print()

    def mul(self):
        self.operation_helper("MUL")

    def add(self):
        self.operation_helper("ADD")

    def ldi(self):
        # gets the address for registry
        operand_a = self.ram[self.pc + 1]
        # gets the value for the registry
        operand_b = self.ram[self.pc + 2]
        # set the registry at operand_a address to value of operand_b
        self.reg[operand_a] = operand_b
        # 2 step process so we increment by 3 to get the next set of instructions
        self.pc += 3

    def hlt(self):
        # stops the program
        self.running = False

    def prn(self):
        # get the address we want to print
        operand_a = self.ram[self.pc + 1]
        print(self.reg[operand_a])
        # 1 step process so we increment by 2 to get the next set of instructions
        self.pc += 2

    def push(self):
        # decrement the stack pointer
        self.reg[self.sp] -= 1
        # get register address from ram
        reg_num = self.ram[self.pc + 1]
        # get the value from the register
        value = self.reg[reg_num]

        # store on the top of the stack
        self.ram[self.reg[self.sp]] = value

        # increment the pc
        self.pc += 2

    def pop(self):
        # get the register address from ram
        reg_num = self.ram[self.pc + 1]
        # get the value from current top of the stack
        value = self.ram[self.reg[self.sp]]
        # set register at reg_num to the value
        self.reg[reg_num] = value
        # increment the stack pointer
        self.reg[self.sp] += 1
        # increment the pc
        self.pc += 2

    def call(self):
        # get the return address
        ret_addr = self.pc + 2
        # push return address to the ram
        # first decrement the stack pointer
        self.reg[self.sp] -= 1
        # set value of ram[stack pointer] to the return address
        self.ram[self.reg[self.sp]] = ret_addr

        # call the subroutine
        # get the register address from ram[pc+1]
        reg_num = self.ram[self.pc + 1]
        # set the pc to the value at the register address
        self.pc = self.reg[reg_num]

    def ret(self):
        # return from subroutine
        # pop the return address from the ram stack
        ret_addr = self.ram[self.reg[self.sp]]
        # increment the stack
        self.reg[self.sp] += 1
        # set pc to the return address
        self.pc = ret_addr

    def cmp(self):
        # cmp compares values of 2 registers
        operand_a = self.ram[self.pc + 1]
        operand_b = self.ram[self.pc + 2]
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3

    def jmp(self):
        # get given register from ram
        self.pc += 1
        given_reg = self.ram[self.pc]
        # set pc to the value of the register
        self.pc = self.reg[given_reg]

    def jeq(self):
        # If equal flag is set (true), jump to the address stored in the given register.
        given_reg = self.ram[self.pc + 1]
        if self.flag == E_MASK:
            self.pc = self.reg[given_reg]
        else:
            self.pc += 2

    def jne(self):
        # If E flag is clear (false, 0), jump to the address stored in the given register.
        given_reg = self.ram[self.pc + 1]
        if self.flag != E_MASK:
            self.pc = self.reg[given_reg]
        else:
            self.pc += 2

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            # get memory address thats stored in the register PC
            # store the result in the IR (instruction register)
            ir = self.pc
            inst = self.ram[ir]
            try:
                self.branchtable[inst]()
            except KeyError:
                print(f"KeyError at {self.reg[self.ram[inst]]}")
                sys.exit(1)