"""CPU functionality."""

import sys
import re

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Initialize Register
        self.reg = [0] * 8
        self.reg[7] = 0xF4

        # Initialize Memory
        self.ram = [0] * 256

        # Initialize internal registers
        self.pc = 0
        self.ir = 0
        self.mar = 0
        self.mdr = 0
        self.fl = 0

        # Initialize operation values
        self.operand_a = 0
        self.operand_b = 0

        # Initialize halt as false. CPU does not start halted

        self.halt = False

        # Initialize pc_override for when pc is manually set by function

        self.pc_override = False

        # Initialize branch_table
        self.branch_table = {}
        self.branch_table[0b10000010] = self.LDI
        self.branch_table[0b01000111] = self.PRN
        self.branch_table[0b00000001] = self.HLT
        self.branch_table[0b01000101] = self.PUSH
        self.branch_table[0b01000110] = self.POP
        self.branch_table[0b01010000] = self.CALL
        self.branch_table[0b00010001] = self.RET

        
        
        #Initialize alu_table
        self.alu_table = {}
        self.alu_table[0b10100010] = "MUL"
        self.alu_table[0b10100000] = "ADD"
        self.alu_table[0b10101000] = "AND"
        self.alu_table[0b10100111] = "CMP"



    def load(self, program):
        """Load a program into memory."""

        address = 0

        for instruction in program:
            self.ram_write(address, instruction)
            address += 1

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "AND":
            self.reg[reg_a] &= self.reg[reg_b]
        elif op == "CMP":
            if reg_a == reg_b:
                self.fl = 0b00000001
            elif reg_a > reg_b:
                self.fl = 0b00000010
            else:
                self.fl = 0b00000100

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

    def ram_read(self, address):
        """
        Function that reads from memory. Takes in the address to read.
        Returns the value stored at that address in the RAM.
        """
        self.mar = address
        self.mdr = self.ram[self.mar]

        return self.mdr

    def ram_write(self, address, value):
        """
        Function that writes to memory. Takes in the value to write,
        the address to write to. Saves value at the given address.
        """
        self.mar = address
        self.ram[self.mar] = value
        self.mdr = self.ram[self.mar]

    def run(self):
        """Run the CPU."""

        while not self.halt:         
            self.ir = self.ram_read(self.pc)
            self.operand_a = self.ram_read(self.pc + 1)
            self.operand_b = self.ram_read(self.pc + 2) 
            self.trace()

            # reset pc_override to check if PC needs to be adjusted 
            self.pc_override = False

            # Determine if alu operation or branch_table operation
            bit_5 = (self.ir & 2 ** 5) >> 5

            if bit_5:
                op = self.alu_table[self.ir]
                self.alu(op, self.operand_a, self.operand_b)
            
            if not bit_5:
                self.branch_table[self.ir]()

            if not self.pc_override:
                bit_6 = (self.ir & 2 ** 6) >> 6
                bit_7 = (self.ir & 2 ** 7) >> 7

                if bit_6: 
                    self.pc += 2
                if bit_7:
                    self.pc += 3
        sys.exit()
                

    def LDI(self):
        """
        Set register to this value
        """
        self.reg[self.operand_a] = self.operand_b

    def PRN(self):
        """
        Prints numeric value stored at register address
        """
        print(self.reg[self.operand_a])

    def HLT(self):
        """
        Sets halt value to true
        """
        self.halt = True

    def PUSH(self):
        """
        Pushes value at given register on to computer stack
        """
        self.reg[7] -= 1
        value = self.reg[self.operand_a]
        self.ram_write(self.reg[7], value)
    
    def POP(self):
        """
        Pops value at current stack pointer off the stack 
        and stores it at the given register
        """
        value = self.ram_read(self.reg[7])
        self.reg[self.operand_a] = value
        self.reg[7] += 1

    def CALL(self):
        """
        Calls a subroutine (function) stored at the address in the register.
        
        The address of the instruction directly after CALL is pushed onto the stack. 
        The PC is set to the address stored in the given register.
        """
        pass

    def RET(self):
        """
        Returns from subroutine.
        Pop the value from the top of the stack and store it in the PC.
        """
        pass
