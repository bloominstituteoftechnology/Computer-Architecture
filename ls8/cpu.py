"""CPU functionality."""

import sys

HLT = 0b00000001		
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        #Add list properties to the `CPU` class to hold 256 bytes of memory 
        self.ram = [0] * 256
        # and 8 general-purpose registers.
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        #R0
        #R1
        #R2
        #R3
        #R4
        #R5 reserved as the interrupt mask (IM)
        #R6 reserved as the interrupt status (IS)
        #R7 reserved as the stack pointer (SP)

        #Internal Registers
        #PC: Program Counter, address of the currently executing instruction
        self.pc = 0
        #IR: Instruction Register, contains a copy of the currently executing instruction
        self.ir = 0
        #MAR: Memory Address Register, holds the memory address we're reading or writing
        self.mar = 0
        #MDR: Memory Data Register, holds the value to write or the value just read
        self.mdr = 0
        #FL: Flags, see below
        self.fl = 0
        # Running
        self.running = True

    #`ram_read()` should accept the address to read and return the value stored there.
    def ram_read(self, address):
        return self.ram[address]

    #`ram_write()` should accept a value to write, and the address to write it to.
    def ram_write(self, address, val):
        self.ram[address] = val

    def load(self, filename):
        """Load a program into memory."""

        address = 0

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

        # open the file
        with open(filename) as my_file:
            # go through each line to parse and get
            # the instruction
            for line in my_file:
                # try and get the instruction/operand in the line
                comment_split = line.split("#")
                maybe_binary_number = comment_split[0]
                try:
                    x = int(maybe_binary_number, 2)
                    #print("{:08b}: {:d}".format(x, x))
                    self.ram_write(x, address)
                    address += 1
                except:
                    continue
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == MUL:
            self.reg[reg_a] *= self.reg[reg_b]
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
        while self.running:
            command_to_execute = self.ram_read(self.pc)
            operation_1 = self.ram_read(self.pc + 1)
            operation_2 = self.ram_read(self.pc + 2)

            self.execute_instruction(command_to_execute, operation_1, operation_2)
            
    def execute_instruction(self, instruction, operation_1, operation_2): 
        print(instruction)
        if instruction == LDI:
            self.reg[operation_1] = operation_2
            self.pc += 3
        elif instruction == PRN:
            print(self.reg[operation_1])
            self.pc += 2
        elif instruction == HLT:
            self.running = False
            self.pc += 1
        elif instruction == MUL:
            self.alu(instruction, operation_1, operation_2)
            self.pc += 3
        else:
            print("I don't know what to do.")
            sys.exit(1)
            pass

