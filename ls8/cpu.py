"""CPU functionality."""

import sys

OP1 = 0b10000010
OP2 = 0b01000111
OP3 = 0b10100010
OP4 = 0b00000001
OP5 = 0b01000101
OP6 = 0b01000110
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.memory = [0] * 8
        self.memory[7] = 0xF4
        self.SP = self.memory[7]
        self.pc = 0
        self.branchtable = {} #set to empty dictionary
        self.branchtable[OP1] = self.handle_op1
        self.branchtable[OP2] = self.handle_op2
        self.branchtable[OP3] = self.handle_op3
        self.branchtable[OP4] = self.handle_op4
        self.branchtable[OP5] = self.handle_op5
        self.branchtable[OP6] = self.handle_op6
        self.halted = False

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = sys.argv[1]
        address = 0
        with open(program) as f:
            for line in f:
                # print(line[:8])
                line = line.split('#')[0] #split at the hash mark where comments start
                line = line.strip() #get rid of white space
                if line == '':
                    continue #if line is empty -- continue to top and run function again                
                val = int(line, 2)
                # val = '{0:08b}'.format(val) #adds 8 zeros, or makes the length of the number into binary
                self.ram[address] = val
                address += 1
           

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

    def handle_op1(self, pc): #LDI
     
        operand_a = self.ram_read(pc + 1)
        operand_b = self.ram_read(pc + 2)
        self.memory[operand_a] = operand_b
        self.pc += 3

    def handle_op2(self, pc): #print
   
        operand_a = self.ram_read(pc + 1)
        operand_b = self.memory[operand_a]
        print(operand_b)
        self.pc += 2

    def handle_op3(self, pc): #MULT
        operand_a = self.ram_read(pc + 1)
        num_1 = self.memory[operand_a]

        operand_b = self.ram_read(pc + 2)
        num_2 = self.memory[operand_b]

        mult = num_1 * num_2
        self.memory[operand_a] = mult
        # print(mult)
        self.pc += 3

    def handle_op4(self,pc): #HALT
        self.halted = True
        self.pc += 1
    
    def handle_op5(self,pc): #PUSH
        self.SP -= 1
        copy = self.ram_read(pc + 1) # read the instruction at that address, register 0
        self.ram[self.SP] = self.memory[copy] #saving value at reg 0 to SP location in stack
        self.pc += 2
        # print(f'testing {self.memory[copy]}')

    def handle_op6(self,pc): #POP
        location = self.ram_read(pc + 1)
        self.memory[location] = self.ram[self.SP]
        self.SP +=1
        self.pc += 2
        # print(f'testing {self.memory[location]}')


        


    def run(self):
        """Run the CPU."""
        while not self.halted:
            # print(f'Halted is {self.halted}')
            # print(f'this is the new pc {self.pc}')
            instruction = self.ram_read(self.pc)
            self.branchtable[instruction](self.pc)
       
        # ir = ''
        # halted = False
        # pc = 0
        # while not halted:
        #     instruction = self.ram_read(pc)

        #     if instruction == 0b10000010:
        #         operand_a = self.ram_read(pc + 1)
        #         operand_b = self.ram_read(pc + 2)
        #         self.memory[operand_a] = operand_b
        #         pc += 3
        #     elif instruction == 0b01000111:
        #         operand_a = self.ram_read(pc + 1)
        #         operand_b = self.memory[operand_a]
        #         print(operand_b)
        #         pc += 2
        #     elif instruction == 0b10100010:
        #         operand_a = self.ram_read(pc + 1)
        #         num_1 = self.memory[operand_a]

        #         operand_b = self.ram_read(pc + 2)
        #         num_2 = self.memory[operand_b]

        #         mult = num_1 * num_2

        #         print(mult)
        #         pc += 3
        #     elif instruction == 0b00000001:
        #         halted = True
        #         pc += 1

        

    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, value):
        self.ram[mdr] = value
        
