"""CPU functionality."""

#hlt halts the program
#ldi load immediate
#prn print
#load "immediate", store a value in a register, or "set this register to this value"

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0

    def load(self):
        """Load a program into memory."""
        self.read_params()

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
            # self.ram[address] = instruction
            # address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
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
    def ram_read(self, mar):
        #memory address registry mar, this might as well be the index
        #memory data register mdr
        #cpu register --> fixed small number of special storage locations built in
        #hexadecimal leading 0x binary leading 0b
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def read_params(self,):
        params = sys.argv
        if len(params) != 2: # a file is being passed through
            print("usage: file.py filename")
            sys.exit(1)
        if len(params)==2:   
            try:
                with open(params[1]) as f:
                    address = 0
                    for line in f:
                        # print(line)
                        comment_split = line.split("#")
                        # Strip out whitespace
                        num = comment_split[0].strip()
                        # Ignore blank lines
                        if num == '':
                            continue
                        val = int("0b"+num,2)
                        self.ram_write(address, val)
                        address += 1    
            except FileNotFoundError:
                print("File not found")
                sys.exit(2)
        



    def run(self):
        """Run the CPU."""
        pc = 0 
        IR = None
        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010
        MUL = 0b10100010

        running = True
        self.load()
        while running:
            if self.ram_read(pc) == LDI: #LDI
                # print(self.ram_read(pc+1))
                # print(self.ram_read(pc+2))
                self.reg[self.ram_read(pc+1)] = self.ram_read(pc+2)
                pc += 3
            elif self.ram_read(pc) == PRN:#PRN
                print(self.reg[self.ram_read(pc+1)])
                pc += 2
            elif self.ram_read(pc) == MUL:
                self.reg[self.ram_read(pc+1)]=(self.reg[self.ram_read(pc+1)] * self.reg[self.ram_read(pc+2)])
                pc +=3
            elif self.ram_read(pc) == HLT:#HLT            
                running = False
            
            # command = memory[pc]

# pc = CPU()
# pc.run()
# pc.read_params()
