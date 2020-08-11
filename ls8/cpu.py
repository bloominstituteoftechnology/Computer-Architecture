"""CPU functionality."""

import sys
import re

# inst = {
#     "LDI": 0b10000010,  # Sets the Value of a reg to an int
#     "HLT": 0b00000001,  # halts the program, "ends it"/"stops it"
#     "PRN": 0b01000111,  # Prints the value at the next reg
#     "MUL": 0b10100010,  # multiply reg at +1 with reg at +2
# }


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0] * 8
        self.fl = 0b00000000
        self.pc = 0
        self.sp = 0xF3
        self.is_run = False
        self.call_flag = False
        pass

    def ram_read(self, mar):
        print("MAR: ", mar)
        return self.reg[mar]

    def ram_write(self, mdr, value):

        self.reg[mdr] = value

        # return print(f"RAM_WRITE: V: {value} to R: {self.reg[mdr]}")

    def load(self, prog_file):
        """Load a program into memory."""

        prog = open(prog_file, "r")
        address = 0
        # program = []

        for inst in prog:
            # print("Inst: ", inst)
            if inst[0] != "#":
                if "1" in inst or "0" in inst:
                    inst = inst[slice(8)]
                    # inst = inst[0]
                    self.ram[address] = int(inst, 2)
                    address += 1

        # print("RAM: ", self.ram)
        # print(f"Sp: {self.sp} Reg Len: {len(self.reg)}")
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
        #     self.ram[address] = int(instruction)
        #     address += 1
        # print("RAM: ", self.ram)

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        if op == "CMP":
            if reg_a == reg_b:
                self.fl = 0b00000001
                print(f"ALU flag: {self.fl}")

            if reg_a > reg_b:
                self.fl = 0b00000100

            else:
                self.fl = 0b00000010

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

    def LDI(self):
        reg_index = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        # print("LDI")
        self.reg[reg_index] = value
        # self.ram_write(
        #     self.ram[self.pc + 1], self.ram[self.pc + 2])
        # print(self.ram[])
        # print("PC + 1: ", self.ram[self.pc + 1])
        # print("PC + 2: ", self.ram[self.pc + 2])
        # print(f"Value: {value}")
        # print(f"REG: {self.reg}")
        self.pc += 3
        # run = False

    def HLT(self):
        self.is_run = False
        self.pc += 1

    def PRN(self):
        index = self.ram[self.pc + 1]
        value = self.reg[index]
        # print(f"Value: {value}, Register Index : {index}")
        print(f"Value: {value}")
        self.pc += 2

    def MUL(self):
        num1 = self.ram_read(self.ram[self.pc + 1])
        num2 = self.ram_read(self.ram[self.pc + 2])
        print("MUL answere: ", num1 * num2)
        self.pc += 3

    def POP(self):

        # print(f"Reg index: {self.reg[self.ram[self.pc + 1]]}")
        # print(f"Sp: {self.sp}")
        # take from the stack and add it to the reg location
        # weird cause they both are  in reg
        # top parts of reg is stack
        value = self.ram[self.sp]
        self.reg[self.ram[self.pc + 1]] = value
        # print(f"REG: {self.reg}")
        # print(
        # f"You have POP-d v:{self.reg[self.sp]} to reg: {self.ram[self.pc + 1]}")
        self.sp += 1
        self.pc += 2

    def PSH(self, inc=True):

        self.sp -= 1
        # print(f"Sp: {self.sp}")
        # write the value in ram at pc to the stack (top parts of RAM)
        # save ram value to stack
        value = self.reg[self.ram[self.pc + 1]]
        self.ram[self.sp] = value
        # print(f"REG: {self.reg}")
        # print(f"You have PUSHED V:{value} to R: {self.sp}")
        if inc:
            self.pc += 2

    def ADD(self):
        reg_a = self.ram[self.pc + 1]
        reg_b = self.ram[self.pc + 2]
        self.alu("ADD", reg_a, reg_b)
        self.pc += 3

    def AND(self):
        pass

    def CALL(self):
        """
        push current pc to stack, so we can return later
            we do not want to inc the pc while pushing
        set pc to the address in the given register...
        register will hold a location that points to 
        somewhere in ram, we will go there and do the things
        .....value is stored in a reg
        """
        self.sp -= 1
        self.ram[self.sp] = self.pc
        # print(f"RAM AT : {self.sp} is set to : {self.pc + 1}")
        # print(f"PC is being set to: {self.reg[self.ram[self.pc + 1]]}")
        self.pc = self.reg[self.ram[self.pc + 1]]
        # self.HLT()

    def CMP(self):
        """
        comepare 2 given regs
        set flags according to the out put
        reg_a === reg_b = flag  E to 1 or 0
        reg_a < reg_b = flag L to 1 or 0
        reg_a > reg_b = flag G to 1 or 0
        """
        # print("CMP")
        reg_a = self.reg[self.ram[self.pc + 1]]
        # print(f"reg_a: {reg_a}")
        reg_b = self.reg[self.ram[self.pc + 2]]
        # print(f"reg_b: {reg_b}")

        if reg_a == reg_b:
            self.fl = 1
        else:
            self.fl = 0
        # self.fl = 0x00
        # self.alu("CMP", reg_a, reg_b)
        self.pc += 3

    def DEC(self):
        pass

    def DIV(self):
        pass

    def INC(self):
        pass

    def INT(self):
        pass

    def IRET(self):
        pass

    def JEQ(self):
        """
        if the Equal flag is true (0b00000001)
        then jump to the register
        """
        # print("JEQ")
        # print(f"FLAG: {self.fl}")
        mask = 0b00000001

        a = self.fl & mask
        # print(f"A: {a}")

        if a:
            # print("we jump")
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            # print("we dont jump")
            self.pc += 2

    def JGE(self):
        pass

    def JGT(self):
        pass

    def JLE(self):
        pass

    def JLT(self):
        pass

    def JMP(self):
        # print("JMP")
        self.pc = self.reg[self.ram[self.pc + 1]]

    def JNE(self):
        """
        jump to given register if E flag is false
        mask with &
        itll equal eaither 0 or 2
        """
        # print("JNE")
        mask = 0b00000001
        a = self.fl & mask
        # print(f"A: {a}")

        if a == 0b00000000:
            # print("we jump")
            self.pc = self.reg[self.ram[self.pc + 1]]
        else:
            # print("we dont jump")
            self.pc += 2

        pass

    def LD(self):
        pass

    def MOD(self):
        pass

    def NOP(self):
        pass

    def NOT(self):
        pass

    def OR(self):
        pass

    def PRA(self):
        pass

    def RET(self):
        """
        retrive are saved location, should be in stack
        and set the to pc
        inc pc 2 so we dont run call again.
        dec sp becuase we are poppin lockin
        """
        self.pc = self.ram[self.sp]
        self.pc += 2
        self.sp -= 1

        pass

    def SHL(self):
        pass

    def SHR(self):
        pass

    def ST(self):
        pass

    def SUB(self):
        pass

    def XLA(self):
        pass

    def call_func(self, n):
        func_stack = {
            0b10000010: self.LDI,
            0b00000001: self.HLT,
            0b01000111: self.PRN,
            0b10100010: self.MUL,
            0b01000110: self.POP,
            0b01000101: self.PSH,
            0b10100000: self.ADD,
            0b10101000: self.AND,
            0b01010000: self.CALL,
            0b10100111: self.CMP,
            0b01100110: self.DEC,
            0b10100011: self.DIV,
            0b01100101: self.INC,
            0b01010010: self.INT,
            0b00010011: self.IRET,
            0b01010101: self.JEQ,
            0b01011010: self.JGE,
            0b01010111: self.JGT,
            0b01011001: self.JLE,
            0b01011000: self.JLT,
            0b01010100: self.JMP,
            0b01010110: self.JNE,
            0b10000011: self.LD,
            0b10100100: self.MOD,
            0b00000000: self.NOP,
            0b01101001: self.NOT,
            0b10101010: self.OR,
            0b01001000: self.PRA,
            0b00010001: self.RET,
            0b10101100: self.SHL,
            0b10101101: self.SHR,
            0b10000100: self.ST,
            0b10100001: self.SUB,
            0b10101011: self.XLA

        }
        if n in func_stack:
            func_stack[n]()
        else:
            print(f"No instrunction found! IR: {n}")
            sys.exit(1)

    def run(self):
        """Run the CPU."""
        self.is_run = True

        while self.is_run:
            # print("----------------")
            # print(f"PC: {self.pc + 1}")
            ir = self.ram[self.pc]  # the instruction or code to run
            self.call_func(ir)
            # print("----------------")

            # if ir == inst["LDI"]:
            #     self.ram_write(
            #         self.ram[self.pc + 1], self.ram[self.pc + 2])
            #     # print(self.ram[])
            #     # print("PC + 1: ", self.ram[self.pc + 1])
            #     # print("PC + 2: ", self.ram[self.pc + 2])
            #     self.pc += 3
            #     # run = False

            # elif ir == inst["HLT"]:
            #     run = False
            #     self.pc += 1

            # elif ir == inst["PRN"]:
            #     index = int(str(self.ram[self.pc + 1]), 2)
            #     value = self.reg[index]
            #     print(f"Value: {value}, Register Index : {index}")
            #     self.pc += 2

            # elif ir == inst["MUL"]:
            #     num1 = self.ram_read(self.ram[self.pc + 1])
            #     num2 = self.ram_read(self.ram[self.pc + 2])
            #     print("MUL answere: ", num1 * num2)
            #     self.pc += 3

            # else:
            #     print(f"No instrunction found! IR: {bin(int(ir,2))}")
            #     sys.exit(1)
