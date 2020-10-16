"""CPU functionality."""

import sys




# pulled from printl8.ls8 example file
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110
CALL = 0b01010000
RET = 0b00010001
ADD = 0b10100000
CMP = 0b10100111
JEQ = 0b01010101
JNE = 0b01010110
JMP = 0b01010100

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.halted = False
        self.sp = 0xf4
        self.flag = 0b00000000
    
        
        
    # should accept the address to read and return the value stored there.
    # Memory Address Register (MAR) contains the address that is being read or written to
    def ram_read(self, MAR):
        return self.ram[MAR]

    # should accept a value to write, and the address to write it to.
    # Memory Data Register (MDR) contains the data that was read or the data to write
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) != 2:
            print("usage: comp.py progname")
            sys.exit(1)
        try:
            with open(sys.argv[1]) as f:
                for line in f:
                    line = line.strip()
              
                    
                    if line == '' or line[0] == '#':
                        continue
                    
                    try:
                        str_value = line.split("#")[0]
                   
                        instruction = int(str_value, 2)
                       
                        
                        self.ram[address] = instruction
                        address += 1
                    
                    except ValueError:
                        print(f"Invalid number: {str_value}")
                        sys.exit(1)
                    
                    
        except FileNotFoundError:
            print(f"File not found: {sys.argv[1]}" )
            sys.exit(2)
            


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
        
    # HALT
    # like exit() in python
    def HLT(self):
        self.halted = False
        

    # LDI Register Immediate
    # sets a specified register to a specified value.
    def LDI(self, register, MDR):
        self.reg[register] = MDR

    # `PRN register` pseudo-instruction
    # Print numeric value stored in the given register.
    def PRN(self, register):
        print(self.reg[register])
    
    def ADD(self,a ,b):
        self.reg[a] += self.reg[b]
        self.pc += 3
    
    def MUL(self,a , b ):
        print(self.reg[a])
        print(self.reg[b])
        self.reg[a] = self.reg[a] * self.reg[b]
        self.pc += 3
        
    def CMP(self, a , b):
        if self.reg[a] < self.reg[b]:
            self.flag = 0b00000100 # less than flag
         
        if self.reg[a] > self.reg[b]:
            self.flag = 0b00000010 # greater than flag
     
        if self.reg[a] == self.reg[b]:
            self.flag = 0b00000001 
         
        
        
        
    def JMP(self,value):
        self.pc = value
        
        
            
    def push_val(self, value):
        self.sp -= 1               
        top_of_stack_addr = self.sp
        self.ram[top_of_stack_addr] = value
        
    def pop_val(self):
        top_of_stack_addr = self.sp       
        value = self.ram[top_of_stack_addr]
        self.sp += 1
           
        return value
        
            
                
        

    def run(self):
        """Run the CPU."""
      
        while not self.halted:
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            instruction_register = self.pc
            instruction = self.ram[instruction_register]
   
          
            

            # # Set the value of a register to an integer.
            if instruction == LDI:
                self.LDI(operand_a, operand_b)
                self.pc += 3

            # Print to the console the decimal integer value that is stored in the given register.
            elif instruction == PRN:
                self.PRN(operand_a)
                self.pc += 2
                
            #multiple the two integers
            elif instruction == MUL:
       
                self.MUL(operand_a, operand_b)
                
            elif instruction == ADD:
                self.ADD(operand_a,operand_b)
                
                
            elif instruction == PUSH:
                self.sp -= 1
                reg_num = self.ram[self.pc +1]
                value = self.reg[reg_num]
                
                
                top_of_stack_addr = self.sp
                self.ram[top_of_stack_addr] = value
            
                
                self.pc += 2
                
             
           
            elif instruction == POP:
              
                top_of_stack_addr = self.sp
                
                value = self.ram[top_of_stack_addr]
                
                reg_num = self.ram[self.pc + 1]
                self.reg[reg_num] = value
                self.sp += 1
           
                self.pc += 2
                
            elif instruction == CALL:
                #get addres of the next instruction after the call 
                return_addr = self.pc + 2
               
                
                self.push_val(return_addr)
                
                reg_num = self.ram[self.pc + 1]
                subroutine_addr = self.reg[reg_num]
                
                self.pc = subroutine_addr
                
           
                
            elif instruction == RET:
                return_addr = self.pop_val()
                
                self.pc = return_addr
                
            elif instruction == CMP:
                self.CMP(operand_a,operand_b)
                self.pc += 3
                
            elif instruction == JEQ:
                # print('JEQ',operand_a)
              
                if self.flag == 0b00000001:
                    self.pc = self.reg[operand_a]
                    
                else:
                    self.pc += 2
                
            elif instruction == JNE:
          
                if self.flag != 0b00000001:
                    self.pc = self.reg[operand_a]
                    
                else:
                    self.pc += 2
                
                    
            elif instruction == JMP:
                # value = self.reg[operand_a]
                self.pc = self.reg[operand_a]
             
               
                
       
            # exit the loop if a HLT instruction is encountered, regardless of whether or not there are more lines of code in the LS-8 program you loaded.We can consider HLT to be similar to Python's exit() in that we stop whatever we are doing, wherever we are.
            elif instruction == HLT:
                self.halted = True
                # self.pc += 1
            