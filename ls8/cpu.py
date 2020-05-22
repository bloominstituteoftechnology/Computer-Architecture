"""CPU functionality."""

import sys


SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.registers = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.halted = False
        self.equal = False
        

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
        elif op == "CMP":
            if self.registers[reg_a] == self.registers[reg_b]:
               self.equal = True
            else:
                self.equal = False
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
        return self.ram[MAR]               

    def ram_write(self, MDR, MAR):         
        self.ram[MAR] = MDR 
    
    def push_value(self, value):
        self.registers[SP] -= 1
        self.ram_write(value, self.registers[SP])

    def pop_value(self):
        value = self.ram_read(self.registers[SP])
        self.registers[SP] += 1
        return value               
            
    def LDI(self, operand_a, operand_b):
        self.registers[operand_a] = operand_b
        self.pc += 3
                              
    def PRN(self, operand_a, operand_b):
        print(self.registers[operand_a])
        self.pc += 2
    
    def HLT(self, operand_a, operand_b):                  
        self.halted = True
        self.pc += 1
        sys.exit(0) 

    def PUSH(self, operand_a, operand_b):
        self.push_value(self.registers[operand_a])     
        self.pc += 2                                    

    def POP(self, operand_a, operand_b):
        self.registers[operand_a] = self.pop_value()                                       
        self.pc +=2                                                    

    def CALL(self, operand_a, operand_b):
        self.push_value(self.pc + 2)
        self.pc = self.registers[operand_a]

    
    def RET(self, operand_a, operand_b):
        self.pc = self.pop_value()

    def MUL(self, operand_a, operand_b):
        self.alu("MUL", operand_a, operand_b)
        self.pc +=3

    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc +=3


    def JMP(self, operand_a, operand_b):
        self.pc = self.registers[operand_a]

    def JEQ(self, operand_a, operand_b):
        if self.equal == True:
            self.pc = self.registers[operand_a]
        else:
            self.pc += 2

    def JNE(self, operand_a, operand_b):
        if self.equal == False:
            self.pc = self.registers[operand_a]
        else:
            self.pc += 2

    def CMP(self, operand_a, operand_b):
        self.alu("CMP", operand_a, operand_b)
        self.pc += 3


    
    def run(self):
        self.pc = 0
        run_instructions = {
            1: self.HLT,
            17: self.RET,
            71: self.PRN,
            69: self.PUSH,
            70: self.POP,
            80: self.CALL,
            130: self.LDI,
            160: self.ADD,
            162: self.MUL,
            84: self.JMP,
            85: self.JEQ,
            86: self.JNE,
            167: self.CMP,
           }
        while not self.halted:
            IR = self.ram_read(self.pc)
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            run_instructions[IR](operand_a, operand_b)

        self.halted = True
           
    
        

       
