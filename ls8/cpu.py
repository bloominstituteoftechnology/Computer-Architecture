"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.running = True
        self.ir = {
            0b10100010:'MUL',
            0b00000001:'HLT',
            0b10000010:'LDI',
            0b01000111:'PRN'
            }
     

    def load(self, file_name):
        """Load a program into memory."""

        address = 0
        program = []
        with open(file_name) as f:
            
         
            for address, line in enumerate(f):
                line = line.split("#")
                try:
                    v = int(line[0], 2)
                    
                except ValueError:
                    continue
                self.ram[address] = v
       
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

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        
        value = op >> 6 
        value = value + 1
        # print('value', value)
        op = self.ir[op]
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == 'MUL':
            print(self.reg[reg_a] * self.reg[reg_b])
            self.pc += value
        elif op == 'LDI':
            self.ram_write(reg_a, reg_b)
            self.pc += value #3
        elif op == 'HLT':
            self.running = False
            self.pc += value
            sys.exit(1)
        elif op == 'PRN':
            print(self.reg[reg_a])
            self.pc += value
        else:
            raise Exception("Unsupported ALU operation")
            sys.exit(1)

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
    
    def ram_read(self, counter):
        return self.ram[counter]
        # counter += counter
        
      
    
    def ram_write(self,counter, value):
        self.reg[counter] = value


    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        # ir = {
        #     'MUL':0b10100010,
        #     'HLT':0b00000001,
        #     'LDI':0b10000010,
        #     'PRN':0b01000111
        #     }
        ir = {
            0b10100010:'MUL',
            0b00000001:'HLT',
            0b10000010:'LDI',
            0b01000111:'PRN'
            }
            
     
         # 0b10000010
       
      
        while self.running:
            # ir = self.ram_read(pc)
            
            # if ir == 0b10000010:
              
            #     self.ram_write(self.ram_read(pc+1), self.ram_read(pc+2))
            #     print("LDI, pc, pc+1", ir, self.ram_read(pc+1), self.ram_read(pc+2)) 
            #     pc +=3  #3
            # elif ir == HLT:
            #     running = False
                
            #     pc = pc + 1
                
            #     sys.exit(1)
            # elif ir == 0b01000111:
            #     print(self.ram_read(pc+1))
                
            #     pc = pc + 2
            # elif ir == 0b10100010:
            #     print(self.ram_read(pc), self.ram_read(pc+1), self.ram_read(pc+2))
               
            #     self.alu(self.ram_read(pc), self.ram_read(pc+1), self.ram_read(pc+2))
                
            # else:
            #     print(f'Unknown instruction {ir} at address {pc}')
            #     sys.exit(1)
          
            self.alu(self.ram_read(self.pc), self.ram_read(self.pc+1), self.ram_read(self.pc+2))
            
