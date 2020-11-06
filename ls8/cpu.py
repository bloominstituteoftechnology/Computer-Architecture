"""CPU functionality."""

import sys
import os.path
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
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
        #pass
        self.ram = [0] * 256 # 256 ram can only be as 0-355
        self. pc = 0 #program counter
        self.reg = [0] * 8 # 8 bit regester
        self.mar = 0 #memory address register memory address to read or write
        self.mdr = 0 #memory data register holds the value to write or read
        self.flag = 0 #flag register hold flag status
        self.halted = False
        self.running = True

        # SPpoints at the value at the top of the stack (most recently pushed), or at address F4 ifempty.
        self.reg[7] = 0xF4  # 244 # int('F4', 16)
        self.ir = 0
        # Setup Branch Table
        self.branchtable = {}
        self.branchtable[HLT] = self.execute_HLT
        self.branchtable[LDI] = self.execute_LDI
        self.branchtable[PRN] = self.execute_PRN
        self.branchtable[MUL] = self.execute_MUL
        self.branchtable[PUSH] = self.execute_PUSH
        self.branchtable[POP] = self.execute_POP
        self.branchtable[CALL] = self.execute_CALL
        self.branchtable[ADD] = self.execute_ADD
        self.branchtable[RET] = self.excute_RET

        # Property wrapper

    @property
    def sp(self):
        return self.reg[7]

    @sp.setter
    def sp(self, a):
        self.reg[7] = a & 0xFF

    def instruction_size(self):
        return ((self.ir >> 6) & 0b11) + 1

    def instruction_sets_pc(self):
        return ((self.ir >> 4) & 0b0001) == 1

    def ram_read(self, mar):
        if mar >= 0 and mar < len(self.ram):
            return self.ram[mar]
        else:
            print(f"Error:{mar}")
            return -1

    def ram_write(self, mar, mdr):
        if mar >= 0 and mar < len(self.ram):
            self.ram[mar] = mdr & 0xFF
        else:
            print(f"Error:{mdr}")

    def load(self, file_name):
        """Load a program into memory."""

        address = 0

        file_path = os.path.join(os.path.dirname(__file__), file_name)
        try:
            with open(file_path) as f:
                for line in f:
                    num = line.split("#")[0].strip()  # "10000010"
                    try:
                        instruction = int(num, 2)
                        self.ram[address] = instruction
                        address += 1
                    except:
                        continue
        except:
            print(f'Could not find file named: {file_name}')
            sys.exit(1)


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


        while not self.halted:
            self.ir = self.ram_read(self.pc) # these are info reg and program counter
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if not self.instruction_sets_pc():
                self.pc += self.instruction_size()
            self.exexute_instruction(operand_a,operand_b)
    def exexute_instruction(self, operand_a, operand_b):
        if self.ir in self.branchtable:
            self.branchtable[self.ir](operand_a, operand_b)
        else:
            print('Error')
            sys.exit(1)




    def execute_HLT(self, a=None, b=None):
        self.halted = True

    def execute_LDI(self, reg_num, val):
        self.reg[reg_num] = val

    def execute_PRN(self, reg_num, b=None):
        print(self.reg[reg_num])

    def execute_MUL(self, reg_num, reg_num2):
        self.reg[reg_num] *= self.reg[reg_num2]

    def execute_PUSH(self, reg_num, b=None):
        self.sp -= 1
        self.mdr = self.reg[reg_num]
        self.ram_write(self.sp, self.mdr)

    def execute_POP(self, dest_reg_num, b=None):
        self.mdr = self.ram_read(self.sp)
        self.reg[dest_reg_num] = self.mdr
        self.sp += 1

    def execute_CALL(self, dest_reg_num, b=None):
        self.sp -=1
        self.ram_write(self.sp, self.pc + self.instruction_size())
        self.pc = self.reg[dest_reg_num]

    def excute_RET(self, a=None, b=None):
        self.mdr = self.ram_read(self.sp)
        self.pc = self.mdr
        self.sp += 1

    def execute_ADD(self, reg_num, reg_num1):
        self.reg[reg_num] += self.reg[reg_num1]

