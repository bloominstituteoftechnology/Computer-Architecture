"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256    # stores the program on load()
        self.reg = [0] * 8      # 8 registers
        self.pc = 0             # current address

    def load(self):
        """Load a program into memory."""

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

        address = 0

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

    def ldi(self, reg, val):
        reg = reg & 0b00000111 # bitwise AND to prevent out-of-index
        val = val & 0b11111111 # bitwise AND to limit values
        self.reg[reg] = val

    def ram_read(self, addr):
        return self.ram[addr]

    def ram_write(self, val, addr):
        self.ram[addr] = val

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
        self.pc = 0
        ir = 0 # instruction register

        while True: # use HLT to escape loop
            ir = self.ram_read(self.pc)

            if ir == 0b00000001:    # halt command
                break
            elif ir == 0b10000010:  # LDI: set register value
                mem_addr_reg = self.ram_read(self.pc + 1)
                mem_data_reg = self.ram_read(self.pc + 2)
                self.ldi(mem_addr_reg, mem_data_reg)
                self.pc += 3 # increment pc counter
            elif ir == 0b01000111:  # PRN: print from register
                mem_addr_reg = self.ram_read(self.pc + 1)
                mem_addr_reg = mem_addr_reg & 0b00000111 # OoB limiter
                print(self.reg[mem_addr_reg])
                self.pc += 2 # increment pc counter
            else:
                print(f'Unsupported opcode: {ir} at address: {self.pc}')
                break