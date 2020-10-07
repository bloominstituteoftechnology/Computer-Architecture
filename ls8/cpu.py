"""CPU functionality."""

import sys



LDI=    0b10000010 # LDI R0,8
PRNR0 =  0b01000111 # PRN R0
ADD =    0b10100000
HLT=     0b00000001




class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0]*256
        self.reg = [0]*8
        self.pc = 0
        self.reg[7] = 0xF4
        self.sp = 7
        
         
         
    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv)<2:
             print('Remember to pass second filename')
             exit()
             
        file = sys.argv[1]     
        
        try:
            with open(file, 'r')as f:
                for line in f:
                    if line !="\n" and line[0] !="#":
                       self.ram[address]= int(line[0:8],2)
                       address +=1
        except FileNotFoundError:
            print(f'Error from {sys.argv[0]}: file{sys.argv[1]}not found!')   
            exit()            
            
    def ram_read(self, key):
        return self.ram[key]
    
    def ram_write(self, mar, mdr):
        mar %= 256
        
        self.ram[mar] = mdr
    
    def PUSH(self, value=None) :
        self.sp -=1
        if not value:
            value = self.reg[self.ram_read(self.pc +1)]  
        
    def POP(self )  :
        value = self.ram[self.sp]
        target_reg_address = self.ram[self.pc + 1]
        self.reg[target_reg_address] = value
                    # Increment SP
        self.sp += 1
        self.pc += 2
        
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b]
        elif op == "OR":
            self.reg[reg_a] |= self.reg[reg_b]
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
        running = True
        
        while running:
            command = self.ram[self.pc]
             
            op_a = self.ram_read(self.pc +1)
            op_b = self.ram_read(self.pc +2)
             
            if command == 0b10000010: #LDI
                self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc +2)
                
            elif command == 0b01000111: # PRN
                print(self.reg[self.ram_read(self.pc + 1)])
            #  elif command == 
            
            elif command == 0b10100010: # MUL
                self.alu("MUL", self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            
            elif command == 0b00000001:  #HLT
                running = False
                 
            elif command == 0b01000101 : ##PUSH
                self.reg[7] -=1
                self.ram_write(self.reg[7], self.reg[op_a] )
                #  value = self.ram[self.sp]
                #  if not value:
                #     value = self.reg[self.ram_read(self.pc +1)]  
                    
            elif command == 0b01000110: ##POP
                value = self.ram[self.reg[7]]
                target_reg_address = self.ram[self.pc + 1]
                self.reg[target_reg_address] = value
                            # Increment SP
                self.reg[7] += 1
                    
            else:   
                print('unknown command')
                running = False
            
            self.pc +=(command >>6)  +1
                