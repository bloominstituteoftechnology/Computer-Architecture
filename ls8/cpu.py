"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self, ram=[0] * 25, reg=[0] * 8, pc=0):
        """Construct a new CPU."""
        self.ram = ram
        self.reg = reg
        self.pc = pc

    def ram_read(self, pc_address):
        return self.ram[pc_address]

    def ram_write(self, pc_address, value):
        self.ram[pc_address] = value

    def load(self):
        """Load a program into memory."""
        address = 0

        #if user error with filename print error and exit
        if len(sys.argv) != 2:
            print("please provide filename")
            print(sys.stderr)
            sys.exit(1)
        
        #get hashes from input file
        try:
            with open(sys.argv[1]) as file:
                for line in file:
                    file_hashes = line.split("#")
                    possible_instruction = file_hashes[0]
                    first_bit = possible_instruction[0]
                    #skip empty lines
                    if possible_instruction != " ":
                        #if the instruction begins with 1 or 0 add to ram
                        if first_bit == "1" or first_bit == "0":
                            instruction_str = possible_instruction[0:8]
                            instruction = int(instruction_str, base=2)
                            print(instruction)
                            self.ram_write(self.ram[address], instruction)
                            self.ram[address] = instruction
                            address += 1
        except FileNotFoundError:
            print("File not found!")
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
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] * self.reg[reg_b]
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

    def run(self):
        """Run the CPU."""
        self.load()
        HTL = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010
        MUL = 0b10100010

        ALU_OP = [MUL]

        running = True
        while running:
            command = self.ram[self.pc]
            # print(command)
            if command == HTL:
                running = False
            elif command == LDI:
                #reg location
                operand_a = self.ram_read(self.pc + 1)
                #value
                operand_b = self.ram_read(self.pc + 2)
                #set value of a register to an integer
                self.reg[operand_a] = operand_b
                self.pc += 3
            elif command == PRN:
                #Print numeric value stored in the given register
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            # elif command in ALU_OP:
            #     print("command found")
            #     self.alu(command, self.ram_read + 1, self.ram_read + 2)
            #     self.pc += 3
            else:
                print("Error: Command not found")
                print(command)
                exit()

