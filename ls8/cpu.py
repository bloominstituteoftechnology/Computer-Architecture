"""CPU functionality."""

import sys

#check for file arg
if len(sys.argv) != 2:
    print("usage: ls8.py *insert a program file name as argument*")
    sys.exit(1)


class CPU:
    """Main CPU class."""

    def __init__(self, reg = [0] * 20, ram = [0] * 20, pc = 0):
        """Construct a new CPU."""
        self.reg = reg
        self.ram = ram
        self.pc = pc # memory address starting at 0 when initialized
    
    def load(self):
        """Load a program into memory."""
        program = []

        with open(sys.argv[1]) as f:
            for line in f:
                comment_split = line.split('#')
                num = comment_split[0].strip()
                try:
                    program.append(int(num, 2))
                except ValueError:
                    pass

        address = 0

        # # For now, we've just hardcoded a program:

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
        elif op == "MUL":
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


    def ram_read(self, memory_address_register):
        value = self.ram[memory_address_register]
        return value

    def ram_write(self, memory_data_register, memory_address_register):
        self.ram[memory_address_register] = memory_data_register

    def run(self):
        """Run the CPU."""
        running = True
        print("running")
        while running:

            ir = self.pc
            op = self.ram[ir]
            instruction_size = ((op & 11000000) >> 6) + 1
            
            if op == 0b10000010: # LDI (load into register a value)
                operand_a = self.ram[self.pc + 1] # targeted register
                operand_b = self.ram[self.pc + 2] # value to load
                self.reg[operand_a] = operand_b
                # self.pc += 3

            elif op == 0b10100010: # MUL (call alu with paramaters)
                operand_a = self.ram[self.pc + 1]
                operand_b = self.ram[self.pc + 2]
                self.alu("MUL", operand_a, operand_b)
                # self.pc += 3

            elif op == 0b01000111: # PRN (print value from given register)
                operand_a = self.reg[self.pc + 1]
                print(self.reg[operand_a])
                # self.pc += 2

            elif op == 0b00000001: # HLT (halt cpu)
                running = False
            
            else:
                print("Unrecognized instruction: " + str(op))
                running = False
            
            self.pc += instruction_size


