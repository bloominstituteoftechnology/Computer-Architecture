"""CPU functionality."""

import sys
program_filename = sys.argv[0]

HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.running = True
        self.address = 0
        self.pc = 0
        

    def ram_read(self, MAR):
        '''
        accept address to read
        returns value stored
        '''
        return self.ram[MAR]

    def ram_write(self, MDR, MAR):
        '''
        accepts value to write
        and address to write it to
        '''
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        with open(program_filename) as f:
            for line in f:
                line = line.split('#')
                line = line[0].strip()

                if line == '':
                    continue

            self.ram[self.address] = int(line, 2) # converts to base 2

            self.address += 1
        

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
            IR = self.ram_read(self.pc) # command, where pc is
            operand_a = self.ram_read(self.pc + 1) #pc + 1
            operand_b = self.ram_read(self.pc + 2) #pc + 
            
            #update program counter
            #look at the first two bits of the instruction
            self.pc += 1 + (IR >> 6)
            #get command


            #conditional for HLT, LDI, PRN
            if IR == HLT:
                self.running = False
                # could also use sys.exit()
            elif IR == LDI: #set register to a value
                #what is the register number? - operand_a What is the value? - operand_b How do I set register? - change self.reg
                self.reg[operand_a] = [operand_b]

            elif IR == PRN: #takes register number, prints out it's content
                #where to get register number? operand_a How to get contents? from inside self.reg
                print(self.reg[operand_a])


                
