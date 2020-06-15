"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        
        pass

    def load(self, file_name):
        """Load a program into memory."""

        address = 0
        program = []
        with open(file_name) as f:
            lines = f.readlines()
            for line in lines:
                if line[0]!= '#':
                    num = int(line[0:8], 2)
                    num1 = bin(num)
                    binary = format(num,"08b")
                    program.append(binary)

        print(program)
      
       
                
        
        
       
        
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
    
    def ram_read(self, counter):
        return self.ram[counter]
        # counter += counter
        
      
    
    def ram_write(self,counter, value):
        self.reg[counter] = value


    def run(self):
        """Run the CPU."""
        HLT = 0b00000001
        pc = self.pc
         # 0b10000010
        print('running')
        running = True
        while running:
            ir = self.ram_read(pc)
            if ir == 0b10000010:
              
                self.ram_write(self.ram_read(pc+1), self.ram_read(pc+2))
                print("LDI, pc, pc+1", ir, self.ram_read(pc+1), self.ram_read(pc+2)) 
                pc +=3  #3
            elif ir == HLT:
                running = False
                print("HLT, pc, pc+1", ir, pc, self.ram_read(pc+1) )
                print(f"Encountered HLT at address {pc}")
                pc = pc + 1
                
                sys.exit(1)
            elif ir == 0b01000111:
                print(self.ram_read(pc+1))
                print("PRN, pc, pc+1", ir, pc, self.ram_read(pc+1) )
                pc = pc + 2

            else:
                print(f'Unknown instruction {ir} at address {pc}')
                sys.exit(1)

      
