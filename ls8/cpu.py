"""CPU functionality."""

import sys

# All instructions will be class constants, to keep conditionals readable
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.int_registers = [0] * 5
        self.ram = [0b00000000] * 256

    @property
    def pc(self):
        '''Returns the Program Counter, address of currently executing
        instruction'''
        return self.int_registers[0]

    @pc.setter
    def pc(self, value):
        self.int_registers[0] = value

    @property
    def ir(self):
        '''Instruction Register, contains copy of currently executing 
        instruction'''
        return self.int_registers[1]

    @ir.setter
    def ir(self, value):
        self.int_registers[1] = value

    @property
    def mar(self):
        '''Memory Address Register, holds the memory address being read or 
        written to.'''
        return self.int_registers[2]

    @property
    def mdr(self):
        '''Memory Data Register, holds the value to write or the value read'''
        return self.int_registers[3]

    @property
    def fl(self):
        '''Flags register'''
        pass

    def ram_read(self, mar):
        '''
        Returns the value stored at the Memory Addres Register (mar)
        Spec specifies that mdr and mar are explicitely passed in as variables
        '''
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        '''
        Writes the value stored in the Memory Data Register (mdr) to the 
        location specified by the Memory Address Register(mar). Spec specifies
        that mdr and mar are explicitely passed in as variables.
        '''
        self.ram[mar] = mdr

    def load(self, program):
        """Load a program into memory."""

        address = 0

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

        running = True

        while running:
            self.ir = self.ram_read(self.pc)

            #TODO Maybe these are conditional reads, depending on what the
            # actual operation that is being specified. Maybe there is no harm
            # in reading and not using them. Think about this.
            operand_a = self.ram_read(self.pc +1 )
            operand_b = self.ram_read(self.pc + 2)

            if self.ir == HLT:
                running = False #Not necessary, keeping with convetion
                break

            #TODO consider breaking these out like the ALU is broken out
            # a dictionary style switch might be good.
            if self.ir == LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3
            elif self.ir == PRN:
                print(self.registers[operand_a])
                self.pc += 2




