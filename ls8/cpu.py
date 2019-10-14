"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*265
        self.reg = [0] * 8

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
        HLT = 1
        LDI = 130   
        PRN = 71
        pc = 0

        while True:
            ir = self.ram_read(pc) # Instruction Register, currently executing instruction
            if ir == HLT:
                pc +=1
                break

            elif ir == LDI:
                regAddress = self.ram_read(pc+1)
                integer = self.ram_read(pc+2)
                self.reg[regAddress] = integer
                pc +=3

            elif ir == PRN:
                print(self.reg[self.ram_read(pc+1)   ])
                pc +=2

            else:
                print(f"Unknown instruction: {ir}")
                break

    # accepts the address to read and return the value stored there.
    # MAR = Memory Address Register, address that is being read or written to
    def ram_read(self, MAR):
        return self.ram[MAR]

    # accepts a value to write, and the address to write it to.
    # MAR = Memory Address Register, address that is being read or written to
    # MDR = Memory Data Register, address that is being read or written to
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR