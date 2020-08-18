"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256     # ram = [0,0,0, 0, 0.. -> 256 0's]
        self.reg = [0] * 8       # register-on the cpu.. reg = [0,0,0,0,0,0,0,0]
        self.pc = 0              # Program Counter - the index into memory of the currently-executing instruction

    def load(self):
        """Load a program into ram."""

        filename = sys.argv[1]
        address = 0

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
        
        with open(filename) as f:
            for line in f:
                
                line = line.split("#")[0].strip()
                
                if line == "":
                    continue
                
                else:
                    self.ram[address] = int(line, 2)
                    address += 1
                
                print(line)

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1

    # ask for tomorrow, not needed for day 1
    
    def ram_read(self, address):
        return self.ram[address]
        
    
    def ram_write(self, value, address):
        self.ram[adress] = value
        return value
    
    def alu(self, op, reg_a, reg_b):
        """ALU / Math operations."""

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
        
        # Codes
        HLT = 0b00000001 # Halt/ Stop
        LDI = 0b10000010 # Assign 
        PRN = 0b01000111 # Print numeric value stored in the given register.
        
        running = True
        
        while running:
            ir = self.ram[self.pc] # Instruction Register
            
            if ir == HLT:
                running = False
                self.pc += 1
            
            elif ir == LDI:
                reg_num = self.ram[self.pc + 1]
                value = self.ram[self.pc + 2]
                self.reg[reg_num] = value
                # increment 
                self.pc += 3
            
            elif ir == PRN:
                reg_num = self.ram[self.pc + 1]
                print(f"PRN- Numeric value stored in given register -> {self.reg[reg_num]}")
                self.pc += 2
            
            
            
                
            
            
            
            
            
            
            
            
            
            
            
        
