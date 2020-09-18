"""CPU functionality."""
import sys
SP = 7
LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
# SPRINT ADDITION BELOW
CMP = 0b10100111 # ALU OP
JMP = 0b01010100 # PC MUTATOR
JEQ = 0b01010101 # PC MUTATOR
JNE = 0b01010110 # PC MUTATOR

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""

        self.ram = [0] * 256
        self.registers = [0] * 8 # R0-R7
        self.registers[SP] = 0xF4 # stack pointer
        self.pc = 0 # Program Counter, address of the currently-executing instuction
        self.flag = 0B00000000

        # "Variables" in hardware. Known as "registers".
        # There are a fixed number of registers
        # They have fixed names
        # R0, R1, R2, ... , R6, R7

    # accepts the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]

    # accepts a value to write, and the address to write it to
    def ram_write(self, value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        try:
            address = 0
            with open(sys.argv[1]) as file:
                for line in file:
                    split_file = line.split("#")
                    value = split_file[0].strip()
                    if value == "":
                        continue

                    try:
                        instruction = int(value, 2)
                    except ValueError:
                        print(f"Invalid number '{value}'")
                        sys.exit(1)

                    self.ram[address] = instruction
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit()


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        # SPRINT CMP
        elif op == "CMP":
            if self.registers[reg_a] < self.registers[reg_b]:
                self.flag = 0b00000100 # less than flag
            if self.registers[reg_a] > self.registers[reg_b]:
                self.flag = 0b00000010 # greater than flag
            if self.registers[reg_a] == self.registers[reg_b]:
                self.flag = 0b00000001 # equal flag
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
        self.running = True
        while self.running:
            instruction = self.ram_read(self.pc)  # Instruction register, copy of the currently-executing instruction

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if instruction == HLT: # HLT - halt the CPU and exit the emulator.
                self.running = False
                self.pc += 1

            elif instruction == PRN:
                print(self.registers[operand_a])
                self.pc += 2

            elif instruction == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3

            elif instruction == MUL:
                reg_a = self.ram_read(self.pc + 1)
                reg_b = self.ram_read(self.pc + 2)
                self.registers[reg_a] = self.registers[reg_a] * self.registers[reg_b]
                self.pc +=3

            elif instruction == PUSH:
                # Decrement Stack Pointer(SP)
                self.registers[SP] -= 1
                # Get the reg num to push
                register_num = self.ram_read(self.pc + 1)
                # Get the value to push
                value = self.registers[register_num]
                # Copy the value to the SP address
                top_of_stack_addr = self.registers[SP]
                self.ram[top_of_stack_addr] = value
                # increment program counter to put program back on track
                self.pc += 2

            elif instruction == POP:
                # Get reg to pop into
                register_num = self.ram_read(self.pc + 1)
                # Get the top of stack addr
                top_of_stack_addr = self.registers[SP]
		        # Get the value at the top of the stack
                value = self.ram_read(top_of_stack_addr)
		        # Store the value in the register
                self.registers[register_num] = value
		        # Increment the SP
                self.registers[SP] += 1
                # increment program counter to put program back on track
                self.pc += 2
# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            elif instruction == CMP: # Compare the values in two registers.
                op_a = self.ram_read(self.pc + 1)
                op_b = self.ram_read(self.pc + 2)
                self.alu("CMP", op_a, op_b)
                self.pc += 3

            # Jump to the address stored in the given register.
            elif instruction == JMP:
                # get address from register
                reg_num = self.ram_read(self.pc + 1)
                # set pc to address
                self.pc = self.registers[reg_num]

            # If equal flag is set (true), jump to the address in the given register.
            elif instruction == JEQ:
                if self.flag == 0b00000001:
                    reg_num = self.ram_read(self.pc + 1)
                    self.pc = self.registers[reg_num]
                else:
                    self.pc += 2

            # If E flag is clear (false, 0), jump to the address in the given register.
            elif instruction == JNE:
                if self.flag != 0b00000001:
                    reg_num = self.ram_read(self.pc + 1)
                    self.pc = self.registers[reg_num]
                else:
                    self.pc += 2
            else:
                self.pc += 1
