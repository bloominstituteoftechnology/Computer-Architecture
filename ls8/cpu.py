"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.halted = False

    def load(self):
        """Load a program into memory."""

        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                value = line.split("#")[0].strip()
                if value == '':
                    continue
                v = int(value, 2)
                self.ram[address] = v
                address += 1
                        

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
            print(" %02X" % self.reg[i], end='')

        print()
    
    def ram_read(self, MAR):
        value = self.ram[MAR]
        return value
    
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    
    def LDI(self):
        self.registers[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        
    
    
    def PRN(self):
        print(self.registers[self.ram_read(self.pc+1)])
    
    
    def HLT(self):
        self.halted = True

    
    def run(self):
       
       while not self.halted:
           IR =self.ram_read(self.pc)
           if IR == 130:
               self.LDI()
               self.pc += 3
           elif IR == 71: 
               self.PRN()
               self.pc += 2
           elif IR == 1:
               self.HLT() 
               self.pc += 1
           elif IR == 162:
               self.alu("MUL",self.ram_read(self.pc+1), self.ram_read(self.pc+2))
               self.pc += 3

           else:
               exit(1) 
            
        

       
