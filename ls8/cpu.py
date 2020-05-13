"""CPU functionality."""

import sys

LDI = 0
HLT = 1
PRN = 3


class CPU:
    """Main CPU class."""

    def __init__(self):
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.init_value = 0

        
    def load(self, program):
        """Load a program into memory."""

        address = 0

        with open(sys.argv[1]) as f:
            for line in f:
                # print(line)
                if line == '':
                    continue
                comment_split = line.split('#')
                # print(comment_split) # [everything before #, everything after #]

                num = comment_split[0].strip()

                self.ram[address] = int(num)
                address += 1


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

    def mult(self, a, b):
        pass

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010

        running = True
        ir = None

        while running:
            command = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)

            if command == HLT:
                running = False
                self.pc += 1
                sys.exit()
            elif command == LDI:
                self.reg[reg_a] = reg_b
                self.pc += 3
            elif command == PRN:
                print(self.reg[reg_a])
                self.pc += 2

            else:
                #If command is non recognizable
                print(f"Unknown instruction")
                running = False
                #Lets Crash :(
