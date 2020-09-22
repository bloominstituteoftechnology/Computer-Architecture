"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # Internal Registers
        self.pc     = 0b00000000
        self.ir     = NOP
        self.mar    = 0b00000000
        self.mdr    = 0b00000000
        self.fl     = 0b00000000  # 00000LGE - only last 3 bits matter

        # General Purpose Registers
        self.reg = [0] * 8  # this is the CPU's register

        # Memory
        self.ram = [0] * 265 # size of the computer's memory


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
        while True:
            self.ir = self.ram_read(self.pc)

            if self.ir == HLT:
                print("Halting program. Goodbye.")
                break
            elif self.ir == LDI:
                self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
                self.pc += 3
            elif self.ir == PRN:
                print(self.reg[self.ram_read(self.pc+1)])
                self.pc +=2
            else:
                print("Unknown command. Halting program. Goodbye.")
                break

    def ram_read(self, address = None):
        if address is not None:
            self.mar = address

        self.mdr = self.ram[self.mar]
        return self.mdr

    def ram_write(self, address = None, value = None):
        if address is not None:
            self.mar = address
        if value is not None:
            self.mdr = value

        self.ram[self.mar] = self.mdr

 
if __name__ == "__main__":
    cpu = CPU()
    print(len(cpu.ram))

    cpu.ram_write()
    print(cpu.ram[3])
