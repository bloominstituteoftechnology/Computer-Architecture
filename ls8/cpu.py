"""CPU functionality."""

import sys

SP = 7
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
ADD = 0b10100000
HLT = 0b00000001
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.reg[SP] = 0xF4
        self.fl = 0
        self.branchtable = {}
        self.branchtable[LDI] = self.ldi
        self.branchtable[PRN] = self.prn
        self.branchtable[MUL] = self.mul
        self.branchtable[ADD] = self.add
        self.branchtable[HLT] = self.hlt
        self.branchtable[POP] = self.pop
        self.branchtable[PUSH] = self.push
        self.branchtable[CALL] = self.call
        self.branchtable[RET] = self.ret
        self.branchtable[CMP] = self.cmp
        self.branchtable[JEQ] = self.jeq
        self.branchtable[JNE] = self.jne
        self.branchtable[JMP] = self.jmp

    def load(self, filename):
        """Load a program into memory."""

        try:
            address = 0

            with open(filename) as f:
                for line in f:
                    t = line.split('#')
                    n = t[0].strip()

                    if n == '':
                        continue

                    try:
                        n = int(n, 2)
                    except ValueError:
                        print(f"Invalid number '{n}'")
                        sys.exit(1)

                    self.ram[address] = n
                    address += 1

        except FileNotFoundError:
	        print(f"File not found: {sys.argv[1]}")
	        sys.exit(2)
        # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "CMP":
            # `FL` bits: `00000LGE`
            if self.reg[reg_a] == self.reg[reg_b]:
                # Set 'E' flag to 1
                self.fl = 0b00000001
            else:
                self.fl = 0
            # elif self.reg[reg_a] < self.reg[reg_b]:
            #     # Set 'L' flag to 1
            #     self.fl &= 0b00000100
            # elif self.reg[reg_a] > self.reg[reg_b]:
            #     # Set 'G' flag to 1
            #     self.fl &= 0b00000010
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
        while True:
            ir = self.ram_read(self.pc)
            jmp_jne_jeq = self.branchtable[ir]()
            inst_sets_pc = (ir >> 4) & 1
            if inst_sets_pc != 1 or jmp_jne_jeq == False:
                number_of_operands = (ir & 0b11000000) >> 6
                how_far_to_move_pc = number_of_operands + 1
                self.pc += how_far_to_move_pc

    def ldi(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b

    def hlt(self):
        exit()

    def prn(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])

    def mul(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("MUL", operand_a, operand_b)

    def add(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("ADD", operand_a, operand_b)

    def push(self):
        # Get the reg num to push
        reg_num = self.ram_read(self.pc + 1)

        # Get the value to push
        value = self.reg[reg_num]

        # Push the value to stack
        self.push_value(value)

    def push_value(self, value):
        # Decrement SP
        self.reg[SP] -= 1

        # Copy the value to the SP address
        top_of_stack_addr = self.reg[SP]
        self.ram_write(top_of_stack_addr, value)

    def pop(self):
        # Get reg to pop into
        reg_num = self.ram_read(self.pc + 1)

		# Get the value at the top of the stack
        value = self.pop_value()

		# Store the value in the register
        self.reg[reg_num] = value

    def pop_value(self):
	    # Get the top of stack addr
	    top_of_stack_addr = self.reg[SP]

	    # Get the value at the top of the stack
	    value = self.ram_read(top_of_stack_addr)

	    # Increment the SP
	    self.reg[SP] += 1

	    return value

    def call(self):
        # Compute the return addr
        return_addr = self.pc + 2

        # Push return addr on stack
        self.push_value(return_addr)

        # Get the value from the operand reg
        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]

        # Set the pc to that value
        self.pc = value

    def ret(self):
        # Pop the value off the stack
        value = self.pop_value()

        # Set the pc to that value
        self.pc = value

    def cmp(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.alu("CMP", operand_a, operand_b)

    def jeq(self):
        # If `equal` flag is set (true)
        if self.fl == 1:
            # Jump to the address stored in the given register
            self.pc = self.jmp_to()
            return True
        else:
            return False

    def jne(self):
        # If `E` flag is clear (false, 0)
        if self.fl != 1:
            # jump to the address stored in the given register
            self.pc = self.jmp_to()
            return True
        else:
            return False

    def jmp(self):
        # Jump to the address stored in the given register.
        # Set the `PC` to the address stored in the given register.
        self.pc = self.jmp_to()
        return True

    def jmp_to(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.reg[reg_num]

        return value
