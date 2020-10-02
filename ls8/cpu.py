"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.halted = False

    def load(self):
        """Load a program into memory."""

        # address = 0

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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        if len(sys.argv) != 2:
            print('Invalid number of args')
            sys.exit(1)

        try:
            with open(f"examples/{sys.argv[1]}") as f:
                address = 0
                for line in f:
                    comment_split = line.split("#")
                    num = comment_split[0]
                    # second arg in casting int is selecting the base. binary = 2
                    try:
                        instruction = int(num, 2)
                        self.ram[address] = instruction
                        address += 1
                        # print("{:08}: {:d}".format(instruction, instruction))
                    except:
                        print("Can't convert stirng to number")
                        # continue in this use case keeps program running rather than skipping the rest of the lines.
                        continue
        except:
            # custom error handling
            print("File not found")
            sys.exit(1)

    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mdr, mar):
        self.reg[mar] = mdr

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

        def unknown_command(*argv):
            print("IDK this command. Shutting off!")
            sys.exit(1)
        
        def HLT(*argv):
            self.halted = True

        def LDI(operand_a, operand_b):
            self.reg[operand_a] = operand_b
            self.pc += 2
        
        def PRN(*argv):
            print(self.reg[self.ram_read(self.pc+1)])
            self.pc += 1

        while not self.halted:
            command_to_execute = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            def commands(command):
                switcher = {
                    0b00000001: HLT,
                    0b10000010: LDI,
                    0b01000111: PRN,
                }
                return switcher.get(command, unknown_command)   

            execute_command = commands(command_to_execute)
            execute_command(operand_a, operand_b)
            self.pc += 1
