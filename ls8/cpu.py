"""CPU functionality."""

import sys

# opcodes
CALL = 0b01010000
CMP = 0b10100111
HLT = 0b00000001
LDI = 0b10000010
MUL = 0b10100010
POP = 0b01000110
PUSH = 0b01000101
PRN = 0b01000111

# Stack Pointer is the index for Register
SP = 7

sys_file = ""
if len(sys.argv) < 2:
    print("In terminal must provide: python3 ls8.py <path-to-program-file>")
else:
    sys_file = sys.argv[1]


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.ram = [0] * 255
        self.register = [0] * 8
        # Set starting stack location within ram to hexadecimal 244
        self.register[SP] = 0xf4

    def load(self):
        """Load a program into memory."""
        new_program = []
        if sys_file:
            with open(sys_file) as new_file:
                for line in new_file:
                    new_code = line.split('#')[0].strip()
                    # take out blank lines
                    if new_code == "":
                        continue
                    # change str to int
                    new_code_i = int(new_code, 2)
                    new_program.append(new_code_i)
                print("new_program", new_program)
        else:
            quit()
            print(FileNotFoundError)

        address = 0

        for instruction in new_program:
            self.ram[address] = instruction
            address += 1

        # # For now, we've just hardcoded a program:
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

    def ram_read(self, ram_address):
        return self.ram[ram_address]

    def ram_write(self, value, address):
        self.ram[address] = value

    def CALL(self):
        # I believe this is like a repeat: change self.pc = to the value in the next self.ram
        ram_index = self.ram[self.pc + 1]
        # self.pc = ram_index

    def CMP(self):
        index_a = self.ram[self.pc + 1]
        index_b = self.ram[self.pc + 2]
        value_a = self.register[index_a]
        value_b = self.register[index_b]
        if value_a < value_b:
            self.ram[index_a] = self.ram[index_a] & 11111100
        elif value_a > value_b:
            self.ram[index_a] = self.ram[index_a] & 11111010
        else:
            self.ram[index_a] = self.ram[index_a] & 11111001

    def HLT(self):
        running = False
        sys.exit(0)

    def LDI(self):
        num = self.ram[self.pc + 1]
        value = self.ram[self.pc + 2]
        self.register[num] = value

    def PUSH(self, op_a):
        # decrement the SP to point to open space in ram
        self.register[SP] -= 1
        # at that location in ram save the value from reg[pc+1]
        self.ram[self.register[SP]] = self.register[op_a]

    def POP(self, op_a):
        # copy value from ram at the index stored in reg[SP] to reg at next index (op_a)
        self.register[op_a] = self.ram[self.register[SP]]
        # move the SP back up
        self.register[SP] += 1

    def PRN(self, op_a):
        print(self.register[op_a])

    # Arithmetic Logic Unit
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.register[reg_a] += self.register[reg_b]
        # elif op == "SUB": etc
        elif op == "MUL":
            self.register[reg_a] *= self.register[reg_b]
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

        running = True
        while running:
            # fetch
            inst = self.ram[self.pc]
            op_a = self.ram[self.pc + 1]
            op_b = self.ram[self.pc + 2]

            # decode opcode size
            opcode_size = (inst >> 6) + 1

            # decode
            if inst == LDI:
                self.LDI()

            elif inst == MUL:
                self.alu("MUL", op_a, op_b)

            elif inst == POP:
                self.POP(op_a)

            elif inst == PRN:
                self.PRN(op_a)

            elif inst == PUSH:
                self.PUSH(op_a)

            elif inst == HLT:
                self.HLT()

            else:
                print("Command not understood")
                running = False
                # sys.exit(1)

            self.pc += opcode_size
