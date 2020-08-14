"""CPU functionality."""

import sys
# Need codes/ binary num, you need opcodes
HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    ops = {
        0x00: "NOP",
        0x01: "HLT", 
        0x50: "CALL",
        0X11:  "RET",
        0X52: "INT", 
        0x13: "IRET", 
        0x54: "JMP", 
        0x55: "JEQ", 
        0x56: "JNE",
        0x57: "JNG",
        
    } #This is what will run operations.

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.cpu_reg = [0] * 8
        self.pc = 0 
        self.running = True

    def ram_read(self, MAR): 
        """"
        accepts an address to read ( in binary and return the address)
        """
        return self.ram(MAR)

    def ram_write(self, MDR, MAR): 
        """
        Will accept value to write and the address to write it to.

        """
        return self.ram[MAR] == MDR
        

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8 aka load a number into a register
            0b00000000, #R0
            0b00001000, # 8
            0b01000111, # PRN R0
            0b00000000, # Register 0
            0b00000001, # HLT
        ]

        for instruction in program:
            self.ram[address] = instruction
            address += 1


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


        # Set while loop for when cpu is runnign

        while self.running:

            IR = self.ram_read(self.pc)# pc, This will look at where the program counter is looking mirroring it
            operand_a = self.ram_read(self.pc + 1) # pc + 1
            operand_b = self.ram_read(self.pc + 2) # pc + 2

            #Update the program counte
            #Look at the first two bits of the instructions
            # If the command sets the pc directly then you don't want to do this. 

            
            self.pc += 1 + (IR >> 6)

            # Inside this while loop will rest conditionals
            # Before we can set conditionals we need to get the command
            # So we will read the ram to get the command, By adding ram functions
            if IR == HLT: 
                self.running = False
                # We could also use sys.exit as well. 
            
            elif IR == LDI: # We need to set register to a value.
                # First we nee to figure out.
                # What is the register number. --> Operand a and the value is operand b
                # What is the value.
                # How do i set the register as well.
                self.reg[operand_a] = operand_b


            elif IR == PRN:
                # We need to capture the number that we are currently on
                # Then we need to print it's contents
                # Where,  do we get the register number --> operand_a
                # How will we print out the contents,

                print(self.reg[operand_a])
                   









                

            


    

