"""CPU functionality."""

import sys
program_filename = sys.argv[1]

HLT = 0b00000001 
LDI = 0b10000010
PRN = 0b01000111
ADD = 0b10100000
MUL = 0b10100010
DIV = 0b10100011
SUB = 0b10100001
POP = 0b01000110
PUSH = 0b01000101
CALL = 0b01010000
RET = 0b00010001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.running = True
        self.address = 0
        self.pc = 0
        self.reg[6] = 0xF4


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
        self.address = 0
        
        """Load a program into memory."""
        try: 
            with open(program_filename) as f:
                
                for line in f:
                    
                    line = line.split('#')
                    line = line[0].strip()

                    if line == '':
                        continue

                    if line[0] == '1' or line[0] == '0':
                        num = line[:8]
                        self.ram[self.address] = int(num, 2) # converts to base 2

                        self.address += 1
                
        except FileNotFoundError:
            print(f'{sys.argv[1]} not found')
            sys.exit()

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
            self.ram[self.address] = instruction
            self.address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
        elif op == "DIV":
            self.reg[reg_a] /= self.reg[reg_b] 
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
            # print(f'IR is {IR}')
            # print(f'PC is {self.pc')
            operand_a = self.ram_read(self.pc + 1) #pc + 1
            operand_b = self.ram_read(self.pc + 2) #pc + 2
            
            #update program counter
            #look at the first two bits of the instruction
            # self.pc += 1 + (IR >> 6)
            #get command

            #conditional for HLT, LDI, PRN
            if IR == HLT:
                self.running = False
                # could also use sys.exit()
                
            elif IR == LDI: #set register to a value
                #what is the register number? - operand_a What is the value? - operand_b How do I set register? - change self.reg
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif IR == PRN: #takes register number, prints out it's content
                #where to get register number? operand_a How to get contents? from inside self.reg
                print(self.reg[operand_a])
                self.pc += 2
            
            elif IR == ADD:
                self.alu("ADD", operand_a, operand_b)
                self.pc += 3
                
            elif IR == SUB:
                self.alu("SUB", operand_a, operand_b)
            
            elif IR == MUL:
                self.alu("MUL", operand_a, operand_b)
                self.pc += 3
                
            elif IR == DIV:
                self.alu("DIV", operand_a, operand_b)
                self.pc += 3
                
            elif IR == PUSH:
                #decrement the pointer
                self.reg[6] -= 1
                #look ahead in the memory
                reg_num = self.reg[operand_a]
                self.ram[self.reg[6]] = reg_num
                #get value
                num_to_push = self.reg[reg_num]
                #copy into the stack
                self.pc += 2
                
            elif IR == POP:
                #set register
                SP = self.ram[self.reg[6]]
                #get value from last position of SP
                self.reg[operand_a] = SP
                #get register number and copy to register
                reg_num = self.ram[self.pc + 1]
                #move register up
                self.reg[6] += 1
                self.pc += 2
            
            elif IR == CALL:
                # remember where to return to and get address of next instruction
                next_inst_address = self.pc + 2
                # Decrement the pointer
                self.reg[6] -= 1
                # push onto stack
                self.ram[self.reg[6]] = next_inst_address
                self.pc = self.reg[operand_a]
                
            elif IR == RET:
                #pop off stack
                SP = self.ram[self.reg[6]]
                #set stack pointer to pointer
                self.pc = SP
                #increment the pointer
                self.reg[6] += 1
                
                
                

                
                
                
                


                
