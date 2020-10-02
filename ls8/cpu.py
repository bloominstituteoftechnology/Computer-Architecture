"""CPU functionality."""

import sys

# Program Actions
LDI = 0b10000010 # LOAD IMMEDIATE
PRN = 0b01000111 # PRINT
HLT = 0b00000001 # HALT
MUL = 0b10100010 # MULTIPLY
PUSH = 0b01000101 
POP = 0b01000110


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 # 256 bytes of memory
        self.registers = [0] * 8 # General Purpose Registers 0 - 7
        self.pc = 0 # Program Counter
        self.sp = 7 # Stack Pointer

    # access the RAM inside the CPU object
    # MAR (Memory Address Register) - contains the address that is 
        # being read / written to
    def ram_read(self, MAR):
        # accepts the address to read and return the value stored there
        return self.ram[MAR]
    
    # access the RAM inside the CPU object
    # MDR (Memory Data Register) - contains the data that was read or 
        # the data to write
    def ram_write(self, MAR, MDR):
        # accepts a vale to write and the address to write it to
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("Usage: ls8.py filename")
            sys.exit(1)

        try:
            address = 0
            with open(sys.argv[1]) as f:
                for line in f:
                    split_line = line.split('#')
                    code_value = split_line[0].strip()

                    if code_value == '':
                        continue

                    try:
                        code_value = int(code_value, 2)

                    except ValueError:
                        print(f"Invalid Number: {code_value}")
                        sys.exit(1)

                    self.ram_write(address, code_value)
                    address += 1

        except FileNotFoundError:
            print(f"{sys.argv[1]} file not found")
            sys.exit(2)

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.registers[reg_a] += self.registers[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.registers[reg_a] *= self.registers[reg_b]
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
            print(" %02X" % self.registers[i], end='')

        print()

    def run(self):
        """Run the CPU."""

        running = True
        self.registers[self.sp] = len(self.ram)

        while running:
            # read the memory address (MAR) that's stored in register PC (self.pc)
            # store the result in IR (Instruction Register)
            IR = self.ram_read(self.pc)

            # ram_read() - read bytes at PC + 1 and PC + 2 from RAM into variables 
            # operand_a and operand_b
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            # HALT
            if IR == HLT:
                # Exit Loop
                running = False
                # Update PC
                self.pc += 1

            # PRINT
            elif IR == PRN:
                # Print Reg
                print(self.registers[operand_a])
                # Update PC
                self.pc += 2

            # LDI = LOAD IMMEDIATE
            elif IR == LDI:
                # Assign value to Reg Key
                self.registers[operand_a] = operand_b
                # Update PC
                self.pc += 3

            # MUL
            elif IR == MUL:
                self.registers[operand_a] *= self.registers[operand_b]
                self.pc += 3

            # PUSH
            elif IR == PUSH:
                given_register = self.ram[self.pc + 1]
                value_in_register = self.registers[given_register]
                # Decrement the stack pointer
                self.registers[self.sp] -= 1
                # Write the value of the given register to memory at SP location
                self.ram[self.registers[self.sp]] = value_in_register
                self.pc += 2

            # POP
            elif IR == POP:
                given_register = self.ram[self.pc + 1]
                # write the value in memory at the top of stack to the given register
                value_from_memory = self.ram[self.registers[self.sp]]
                self.registers[given_register] = value_from_memory
                # increment the stack pointer
                self.registers[self.sp] += 1
                self.pc += 2

            else:
                sys.exit()
