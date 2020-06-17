"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        # init 8 registers
        self.reg = [0] * 8
        # we increment pc--it's the index of the current instructions
        self.pc = 0
        # Init memory with 256 bits
        self.ram = [0b0] * 256
        # Per our spec, reg 7 = 0xF4
        self.reg[7] = 0xF4
        self.sp = self.reg[7]

    def load(self, filename=None):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if filename:
            with open('./examples/' + filename) as f:
                address = 0
                for line in f:
                    line = line.split("#")[0].strip()
                    print(line)
                    if line == '':
                        continue
                    else:
                        instruction = int(line, 2)  # by default this is base 10 so we need to change this to parse base 2 number
                        self.ram[address] = instruction  
                        address += 1         

        else:
            program = [
                # From print8.ls8
                0b10000010, # LDI R0,8
                0b00000000,
                0b00001000,
                0b01000111, # PRN R0
                0b00000000,
                0b00000001, # HLT
            ]

            for address, instruction in enumerate(program):
                self.ram[address] = instruction

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB": 
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        """prints what's stored in that specified address in RAM"""
        return self.ram[address]

    def ram_write(self, address, value):
        """Overwrites the address in ram with the value"""
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
        running = True
        while running:
            # Set the instruction register (it increments every loop)
            ir = self.ram[self.pc]
            # Used in some instructions
            operand_a = self.ram[self.pc + 1] # register 1
            operand_b = self.ram[self.pc + 2] # register 2

            # HLT, or Halt: exits the emulator
            if ir == 0b00000001:
                running = False
                self.pc += 1

            # LDI, or Load Immediate; set specified register to specific value
            elif ir == 0b10000010:
                self.reg[operand_a] = operand_b
                # Increment program counter by 3 steps in RAM
                self.pc += 3

            # PRN, or print register: prints the current register
            elif ir == 0b01000111:
                print(ir)
                self.pc += 1

            # Mul, or multiply: multiplies the next two values.
            elif ir == 0b10100010:    
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3

            else:
                print(f"Unknown instruction {ir} at address {self.pc}")
                sys.exit(1)

if __name__ == '__main__':
    LS8 = CPU()
    LS8.load()
    for i in range(9):
        print(LS8.ram_read(i))
    LS8.ram_write(0, 15)
    print('==============')
    print(LS8.ram_read(0))
    print('==============')