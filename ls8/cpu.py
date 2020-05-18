"""CPU functionality."""

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # program counter
        self.pc = 0
        # 8 new registers
        self.reg = [0] * 8
        # memory storage for ram
        self.ram = [0] * 256
        # register
        self.ir = 0
        # last regiester
        self.sp = 7
        # flag register
        self.fl = 6

        # op table
        self.op_table = {
            0b10000010: self._ldi,
            0b01000111: self._prn,
            0b10100010: self._mult,
            0b00000001: self._hlt,
            0b01000101: self._push,
            0b01000110: self._pop,
            0b01010000: self._call,
            0b00010001: self._ret,
            0b10100000: self._add,
            0b01010110: self._jne,
            0b01010100: self._jmp,
            0b01010101: self._jeq,
            0b10100111: self._cmp
        }

    def _ldi(self, reg_a, reg_b):
        self.reg[reg_a] = reg_b

    def _prn(self, reg_a, reg_b):
        # print
        print(self.reg[reg_a])

    def _add(self, reg_a, reg_b):
        # add
        self.reg[reg_a] = self.reg[reg_a] + self.reg[reg_b]

    def _mult(self, reg_a, reg_b):
        # multiply
        self.reg[reg_a] = self.reg[reg_a] * self.reg[reg_b]

    def _hlt(self, reg_a, reg_b):
        # stop
        sys.exit()

    def _push(self, reg_a, reg_b):
        # push value in current register to stack
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.reg[reg_a]

    def _pop(self, reg_a, reg_b):
        # remove value from top of stack, place in given reg
        self.reg[reg_a] = self.ram[self.reg[self.sp]]
        self.reg[self.sp] += 1

    def _call(self, reg_a, reg_b):
        # address of instruction
        self.reg[self.sp] -= 1
        self.ram[self.reg[self.sp]] = self.pc + 2
        # pc is val in cur reg
        self.pc = self.reg[reg_a]
        return True

    def _ret(self, reg_a, reg_b):
        # remove val from top of stack, place in reg_a
        self._pop(reg_a, 0)
        self.pc = self.reg[reg_a]
        return True

    def _jne(self, reg_a, reg_b):
        val = self.reg[self.fl]
        if val == 2 or val == 4:
            return self._jmp(reg_a, 0)

    def _jmp(self, reg_a, reg_b):
        self.pc = self.reg[reg_a]
        return True

    def _jeq(self, reg_a, reg_b):
        if self.reg[self.fl] == 1:
            return self._jmp(reg_a, 0)

    def _cmp(self, reg_a, reg_b):
        val_a = self.reg[reg_a]
        val_b = self.reg[reg_b]

        if val_a == val_b:
            # turn bit from 0 to 1
            self.reg[self.fl] = 1
        elif val_a > val_b:
            self.reg[self.fl] = 2
        else:
            self.reg[self.fl] = 4

    # accepts address to read and returns value stored

    def ram_read(self, mar):
        # mar contains address that is being read or written to
        return self.ram[mar]

    # accepts value to write, and address to write it to
    def ram_write(self, mdr, mar):
        # contains date that was read or written or data to write
        self.ram[mar] = mdr

    def load(self, prog):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        with open(prog) as program:
            for instruction in program:
                instruction_split = instruction.split('#')
                instruction_stripped = instruction_split[0].strip()

                if instruction_stripped == '':
                    continue
                instruction_num = int(instruction_stripped, 2)
                self.ram_write(instruction_num, address)
                address += 1

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

    # def alu(self, op, reg_a, reg_b):
    #     """ALU operations."""

    #     if op == "ADD":
    #         self.reg[reg_a] += self.reg[reg_b]
    #     # elif op == "SUB": etc
    #     if op == 'OR':
    #         if reg_a == 1 and reg_b == 0:
    #             return True
    #         elif reg_a == 0 and reg_b == 1:
    #             return True
    #         elif reg_a == 1 and reg_b == 1:
    #             return True
    #         else:
    #             return False
    #     if op == 'XOR':
    #         if reg_a == 1 and reg_b == 0:
    #             return True
    #         if reg_a == 0 and reg_b == 1:
    #             return True
    #         else:
    #             return False
    #     if op == 'NOR':
    #         if reg_a == 0 and reg_b == 0:
    #             return True
    #         else:
    #             return False

    #     else:
    #         raise Exception("Unsupported ALU operation")

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

        while True:
            self.ir = self.ram[self.pc]
            reg_a = self.ram[self.pc + 1]
            reg_b = self.ram[self.pc + 2]

            jump = self.op_table[self.ir](reg_a, reg_b)
            if not jump:
                self.pc += (self.ir >> 6) + 1


#         HLT = 0b00000001
#         LDI = 0b10000010
#         PRN = 0b01000111
#         MUL = 0b10100010
#         PUSH = 0b01000101
#         POP = 0b01000110
# # ******************
#         CALL = 0b01010000

#         running = True

        # while running:
        #     instruction = self.ram_read(self.pc)
        #     reg_a = self.ram_read(self.pc + 1)
        #     reg_b = self.ram_read(self.pc + 2)
        #     if instruction == HLT:
        #         running = False
        #         self.pc += 1
        #         sys.exit()
        #     elif instruction == LDI:
        #         self.reg[reg_a] = reg_b
        #         self.pc += 3
        #     elif instruction == PRN:
        #         print(self.reg[reg_a])
        #         self.pc += 2
        #     elif instruction == MUL:
        #         print(self.reg[reg_a] * self.reg[reg_b])
        #         self.pc += 3

        #     elif instruction == PUSH:
        #         # choose register
        #         reg = self.ram[self.pc+1]
        #         # get value from register
        #         val = self.reg[reg]
        #         # decrement memory address by one
        #         self.reg[self.sp] -= 1
        #         # vave value from register into memory
        #         self.ram[self.reg[self.sp]] = val
        #         # increment pc by 2
        #         self.pc += 2

        #     elif instruction == POP:
        #         # reg holding sp
        #         reg = self.ram[self.pc+1]
        #         # value from place in memory
        #         val = self.ram[self.reg[self.sp]]
        #         # save value into register we arelooking at
        #         self.reg[reg] = val
        #         # increment pointer
        #         self.reg[self.sp] += 1
        #         # increment pc by 2
        #         self.pc += 2

        #     # elif instruction == CALL:
        #     #     self.reg[self.sp] -= 1
        #     else:
        #         print(f'this instruction is not valid: {hex(instruction)}')
        #         running = False
        #         sys.exit()
