"""CPU functionality."""

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
    
    def alu(self, op, register_a, register_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[register_a] += self.registers[register_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")
    
    def load(self):
        """
        Load a program into memory.
        """

        address = 0

        # For now, we've just hardcoded a program:
        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1

    def ram_read(self, address_mar):
        return self.ram[address_mar]
    
    def ram_write(self, address_mar, value_mdr):
        self.ram[address_mar] = value_mdr
    
    def run(self):
        """Run the CPU."""
        # Start running CPU (set "running" to True):
        self.running = True

        while self.running:
            # Go to PC's (Program Counter's) current address in memory (RAM), 
            # store the value at that address in the Instruction Register (IR), 
            # and get the next 2 items in RAM for efficiency in case they are operands:
            instruction, operand_a, operand_b = self.ram[self.pc:self.pc+3]
            op_size = (instruction >> 6) + 1

            # Check if instruction sets PC:
            if (instruction >> 4) & 0b0001: # if int(bin(instruction >> 4)[-1]):
                print("instruction sets the PC")
            # Check if instruction is an ALU operation:
            elif instruction >> 5 & 0b001:  # if int(bin(instruction >> 4)[-2]):
                print("instruction is an ALU operation")
            # Otherwise handle the specific instruction accordingly:
            if instruction == HLT:
                self.running = False
                print("HLT")
            if instruction == LDI:
                register = operand_a & 0b00000111
                value = operand_b
                self.registers[register] = value
                print(f"LDI: set self.registers[{register}] = {value}")
            if instruction == PRN:
                register = operand_a & 0b00000111
                value = self.registers[register]
                print(value)
                print(f"PRN: value = {value}")
            
            # Increment PC to the next instruction's location in RAM:
            print(f"op_size: {op_size}\n")
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
