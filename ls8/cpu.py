"""
CPU functionality for "LS-8" Emulator.
"""

import sys

# OPERATIONS:

# General:
CALL = 0b01010000
CMP = 0b10100111
JEQ = 0b01010101
JMP = 0b01010100
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
RET = 0b00010001
XOR = 0b10101011
# Stack:
POP = 0b01000110
PUSH = 0b01000101
# Interrupts:
INT = 0b01010010
IRET = 0b00010011
# Bitwise Shift:
SHL = 0b10101100
SHR = 0b10101101
# Bitwise Logical operators:
AND = 0b10101000
NOT = 0b01101001
OR = 0b10101010
XOR = 0b10101011
# ALU Operations:
ADD = 0b10100000
DIV = 0b10100011
MOD = 0b10100100
MUL = 0b10100010
MULT = MUL
SUB = 0b10100001
# Comparison:
JGE = 0b01011010
JLE = 0b01011001
JGT = 0b01010111
JLT = 0b01011000



# ---------------------------------------------------------------------
# CPU CLASS AND METHODS:

class CPU:
    """
    Main CPU class.
    """

    def __init__(self):
        """Construct a new CPU."""
        # Initialize empty memory (RAM), 256 bytes (8 * 256 = 2048 bits):
        self.ram = [0] * 256
        
        # Initialize PC (Program Counter) as 0:
        self.pc = 0
        # Initialize CPU as not running ("off") to start:
        self.running = False
        # Create registers, and set all as empty to start:
        self.registers = [0] * 8
    
    def alu(self, operation, register_a, register_b):
        """
        ALU operations.
        """

        if operation == ADD:
            print(f"ADD: self.registers[{register_a}] = {self.registers[register_a]} + self.registers[{register_b}] = {self.registers[register_b]} --> = {self.registers[register_a] + self.registers[register_b]}")
            self.registers[register_a] += self.registers[register_b]
        elif operation == SUB:
            print(f"SUB: self.registers[{register_a}] = {self.registers[register_a]} - self.registers[{register_b}] = {self.registers[register_b]} --> = {self.registers[register_a] - self.registers[register_b]}")
            self.registers[register_a] -= self.registers[register_b]
        elif operation == MUL or operation == MULT:
            print(f"MULT: self.registers[{register_a}] = {self.registers[register_a]} * self.registers[{register_b}] = {self.registers[register_b]} --> = {self.registers[register_a] * self.registers[register_b]}")
            self.registers[register_a] *= self.registers[register_b]
        elif operation == DIV:
            print(f"DIV: self.registers[{register_a}] = {self.registers[register_a]} / self.registers[{register_b}] = {self.registers[register_b]} --> = {self.registers[register_a] / self.registers[register_b]}")
            self.registers[register_a] /= self.registers[register_b]
        elif operation == MOD:
            print(f"MOD: self.registers[{register_a}] = {self.registers[register_a]} % self.registers[{register_b}] = {self.registers[register_b]} --> = {self.registers[register_a] % self.registers[register_b]}")
            self.registers[register_a] %= self.registers[register_b]
        else:
            raise Exception("Unsupported ALU operation")
    
    def load(self, memory_filename):
        """
        Load a program into memory.
        """
        # Load memory/instructions file:
        address = 0
        try:
            # 
            with open(memory_filename) as file:
                for line in file:
                    # Get instruction from file:
                    instruction = line.split("#")[0].strip(" ")
                    # Skip any empty lines or lines with only comments but no values/instructions:
                    if instruction == "" or instruction == "\n":
                        continue
                    # Add to RAM:
                    self.ram[address] = int(instruction, base=2)
                    # Increment to go to next address in RAM:
                    address += 1

        except FileNotFoundError:
            sys.exit(f"File {memory_filename} not found.")

        # # For now, we've just hardcoded a program:
        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # address = 0
        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    def ram_read(self, address_mar):
        return self.ram[address_mar]
    
    def ram_write(self, address_mar, value_mdr):
        self.ram[address_mar] = value_mdr
    
    def run(self):
        """Run the CPU."""
        # Start running CPU (set "running" to True):
        self.running = True

        # Load instructions set into memory: 
        # If instructions file specified in runtime system arguments, load that file's 
        # instructions into memory (RAM):
        if len(sys.argv) == 2:
            self.load(memory_filename=sys.argv[1])
        # If filename not entered via either system arguments or separate load() method 
        # call, exit and ask for user to specify memory filename:
        ram_is_empty = all(element == 0 for element in self.ram)
        if len(sys.argv) != 2 and ram_is_empty:
            sys.exit("Please enter as: cpu.py memory_filename")


        while self.running:
            # Go to PC's (Program Counter's) current address in memory (RAM), 
            # store the value at that address in the Instruction Register (IR), 
            # and get the next 2 items in RAM for efficiency in case they are operands:
            instruction, operand_a, operand_b = self.ram[self.pc:self.pc+3]
            op_size = (instruction >> 6) + 1
            # print(f"PC: {self.pc}")
            # print(f"ram: {self.ram}")
            # print(f"ram: {self.ram[self.pc:self.pc+3]}")
            # print(f"op_size: {op_size}\n")

            # Sets PC: If instruction sets PC:
            if (instruction >> 4) & 0b0001: # if int(bin(instruction >> 4)[-1]):
                print("\ninstruction sets the PC")
            # ALU Operations:
            elif instruction >> 5 & 0b001:  # if int(bin(instruction >> 4)[-2]):
                print("\ninstruction is an ALU operation")
                register_a = operand_a & 0b00000111
                register_b = operand_b & 0b00000111
                self.alu(operation=instruction, register_a=register_a, register_b=register_b)
            # Otherwise handle the specific instruction accordingly:
            if instruction == HLT:
                self.running = False
                print("\nHLT")
            if instruction == LDI:
                register = operand_a & 0b00000111
                value = operand_b
                self.registers[register] = value
                print(f"\nLDI: set self.registers[{register}] = {value}")
            if instruction == PRN:
                register = operand_a & 0b00000111
                value = self.registers[register]
                print(value)
                print(f"\nPRN: value = {value}")
            
            # Increment PC to the next instruction's location in RAM:
            self.pc += op_size

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
            print(" %02X" % self.registers[i], end='')

        print()


if __name__ == "__main__":
    cpu = CPU()
    # cpu.load()
    cpu.run()