"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.branchtable = {}
        self.branchtable[HLT] = self.handle_hlt
        self.branchtable[LDI] = self.handle_ldi
        self.branchtable[PRN] = self.handle_prn
        self.branchtable[MUL] = self.handle_mul
        self.halted = False

    def load(self):
        """Load a program into memory."""

        if len(sys.argv) != 2:
            print("usage: comp.py [filename]")
            sys.exit(1)

        progname = sys.argv[1]

        mar = 0

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
        #     self.ram[mar] = instruction
        #     mar += 1

        with open(progname) as f:
            for line in f:
                line = line.split("#")[0]
                line = line.strip()

                if line == "":
                    continue

                mdr = int(line, 2)
                # print(mdr)

                self.ram[mar] = mdr
                mar += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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

    def handle_hlt(self):
        self.halted = True
    
    def handle_ldi(self):
        reg_num = self.ram_read(self.pc + 1)
        value = self.ram_read(self.pc + 2)
        self.reg[reg_num] = value
    
    def handle_prn(self):
        reg_num = self.ram_read(self.pc + 1)
        print(self.reg[reg_num])

    def handle_mul(self):
        number1 = self.ram_read(self.pc + 1)

        number2 = self.ram_read(self.pc + 2)

        self.alu("MUL", number1, number2) 

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, mar):
        self.ram[mar] = mdr

    def run(self):
        """Run the CPU."""

        while self.halted == False:
            instruction = self.ram[self.pc]
            op_count = instruction >> 6
            instruction_length = op_count + 1
            self.branchtable[instruction]()

            if instruction == 0:
                print(f"Unknown instructions at {self.pc}")
                sys.exit(1)
            
            self.pc += instruction_length

        # halted = False

        # while not halted:
        #     instruction = self.ram[self.pc]
        #     operand_a = self.ram_read(self.pc + 1)
        #     operand_b = self.ram_read(self.pc + 2)

        #     if instruction == LDI: 
        #         self.reg[operand_a] = operand_b
        #         self.pc += 3
        #     elif instruction == PRN: 
        #         print(self.reg[operand_a])
        #         self.pc += 2
        #     elif instruction == HLT: 
        #         halted = True
        #         self.pc += 1
        #     else:
        #         print(f"Unknown instructions at {self.pc}")
        #         sys.exit(1)
