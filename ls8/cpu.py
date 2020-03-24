"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""

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


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    # these below seem to have to do with the register values?
    #self.ir = None
    #self.mar = None
    #self.mdr = None
    #self.fl = None
    # I beleive all of the are PC, MAR, MDR, SP, IR, FL and should be 2 more?

    # FUTURE IMPLEMENTATION:
    # MAR contains the address that is being read or written to.
    # MDR contains the data that was read or the data to write.
    # Two of the registers hold those above values in a CPU also need SP stack pointer
    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        self.ram[address] = value

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
        # Register address, Memory Address, Value

        ir = None # Instruction Register (instruction)
        
        while True:
            #print(bin(self.ram[self.pc]))
            #self.pc += 1

            ir = self.ram[self.pc]

            if ir >= 64: # operand 1
                operand_a = self.ram_read(self.pc +1)
            if ir >= 128: # operand 2
                operand_b = self.ram_read(self.pc +2)
                
            self.do_logic(ir, operand_a, operand_b)
            
    
    def do_logic(self, ir, operand_a, operand_b= None):
        LDI = 130
        PRN = 71
        HLT = 1

        if ir == LDI:
            self.reg[operand_a] = operand_b
            self.pc += 3  
        elif ir == PRN:
            reg_value = self.reg[operand_a]
            print(reg_value)
            self.pc += 2
        elif ir == HLT:
            sys.exit()
