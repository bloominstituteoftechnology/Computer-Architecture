"""CPU functionality."""

import sys

HALT = 0b00000001
PRN = 0b01000111
LDI = 0b10000010
MUL = 0b10100010

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.pc = 0 # program counter
        self.reg = [0] * 8 # example R0 - R7
        self.ram = [0] * 256 # list
        self.running = True


    def load(self, filename):
        """Load a program into memory."""
        try:
            address = 0

            # if len(sys.argv) < 2:
            #     print(f'Please pass in second filename')
            #     sys.exit()

        
        # with open(filename) as fp:
        #     for line in fp:
        #         comment_split = line.split("#")
        #         num = comment_split[0].strip()
        #         if num == '':  # ignore blanks
        #             continue
        #         val = int(num, 2)
        #         self.ram[address] = val
        #         address += 1

            with open(filename) as file: # reading the passed in filename
                for line in file: # for every line in the file
                    split_line = line.split('#') # we want to skip anything starting with a '#'
                    cmd = split_line[0].strip() # we also want to 

                    if cmd == '': # remove/skip any white space
                        continue

                    instruction = int(cmd, 2) # turning the string into binary with int function passing (2 args)

                    # print(f'instructions: ', instruction)
                    
                    self.ram[address] = instruction
                    address += 1
    
        except FileNotFoundError: # if an error or file not found, print this 
            print(f'{sys.argv[0]}: {sys.argv[1]} file was not found!')
            sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == MUL:
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

    def run(self):
        """Run the CPU."""

        while self.running: 
            instruction = self.ram[self.pc]

            if instruction == LDI:
                reg_location = self.ram_read(self.pc + 1)
                reg_value = self.ram_read(self.pc + 2)
                # self.ram_write(reg_location, reg_value)
                self.reg[reg_location] = reg_value
                print(self.reg[reg_location])
                self.pc += 3
            elif instruction == PRN:
                curr_val = self.ram[self.pc + 1]
                print(self.reg[curr_val])
                self.pc += 2
            elif instruction == HALT:
                self.running = False
                self.pc += 1
            elif instruction == MUL:
                reg_location = self.ram_read(self.pc + 1)
                reg_value = self.ram_read(self.pc + 2)
                self.reg[reg_location] *= self.reg[reg_value]
                self.pc += 3
            else:
                print(f'No such {instruction} exists')
                sys.exit(1)
        

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, address, value):
        self.ram[address] = value

