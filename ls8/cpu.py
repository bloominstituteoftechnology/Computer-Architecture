"""CPU functionality."""

import sys

ldi = 0b10000010
print_command = 0b01000111
mult = 0b10100010
halt = 0b00000001
push = 0b01000101
pop = 0b01000110
call = 0b01010000 
ret = 0b00010001
add = 0b10100000
cmpp = 0b10100111
jmp = 0b01010100
jeq = 0b01010101
class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256 #256 bits
        self.memory = [0] * 8 # 8 bit
        self.memory[7] = 0xF4 #address 7 reserved for F4 position in ram
        self.SP = self.memory[7] #set pc to that point in memory
        self.pc = 0
        self.flag = 0b00000000
        self.branchtable = {} #set to empty dictionary
        self.branchtable[ldi] = self.handle_ldi
        self.branchtable[print_command] = self.handle_print_command
        self.branchtable[mult] = self.handle_mult
        self.branchtable[halt] = self.handle_halt
        self.branchtable[push] = self.handle_push
        self.branchtable[pop] = self.handle_pop
        self.branchtable[call] = self.handle_call
        self.branchtable[ret] = self.handle_ret
        self.branchtable[add] = self.handle_add
        self.branchtable[cmpp] = self.handle_cmp
        self.branchtable[jmp] = self.handle_jump
        self.branchtable[jeq] = self.handle_jeq
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
           

        for instruction in program: # for every instruction in the program
            self.ram[address] = instruction #go to that address in ram and set it as the instruction
            address += 1 #increment counter to next address in ram
        


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

    def pc(self):
        pass
    def handle_ldi(self, pc): #LDI
        operand_a = self.ram_read(pc + 1) #saving the value of arg1 (the register) to a variable
        operand_b = self.ram_read(pc + 2) #saving the value of arg2 (the number) to a variable
        self.memory[operand_a] = operand_b # save number to the register in memory
        self.pc += 3 #increase to the next instruction

    def handle_print_command(self, pc): #print
        operand_a = self.ram_read(pc + 1) # save arg1 (register number) to variable
        operand_b = self.memory[operand_a] #access that register number's value in memory and save to variable
        print(operand_b) #print that value
        self.pc += 2 #increase to the next instruction

    def handle_mult(self, pc): #MULT
        operand_a = self.ram_read(pc + 1) #save arg1 (register number) to variable
        num_1 = self.memory[operand_a] # access that register's value and save to variable

        operand_b = self.ram_read(pc + 2) #save arg1 (register number) to variable
        num_2 = self.memory[operand_b] #access that rigister's value and save to variable

        mult = num_1 * num_2 #multiply both values together
        self.memory[operand_a] = mult #save product to the register 
        # print(mult)
        self.pc += 3 #increase to next instruction
    
    def handle_add(self,pc): #HALT
        operand_a = self.ram_read(pc + 1) #save arg1 (reg number) to variable
        num_1 = self.memory[operand_a] #access that register's value

        operand_b = self.ram_read(pc + 2) #save arg1 (reg number) to variable
        num_2 = self.memory[operand_b] #access that register's value

        add = num_1 + num_2 #add both values
        self.memory[operand_a] = add #save the answer to register
        # print(mult)
        self.pc += 3 #increase to next instruction

    def handle_halt(self,pc): #HALT
        self.halted = True # switch halted to true
        self.pc += 1 #incrase to next instruction
    
    def handle_push(self,pc): #PUSH

        self.SP -= 1 #decrement the stack pointer
        copy = self.ram_read(pc + 1) # read the instruction at the given address, save to variable
        self.ram[self.SP] = self.memory[copy] #saving value at the given reg to the stack
        self.pc += 2 #incease to next instruction


    def handle_pop(self,pc): #POP
        location = self.ram_read(pc + 1) #grab given address and save to variable
        self.memory[location] = self.ram[self.SP] #save the value from top of stack to that register
        self.SP +=1 #incease stack counter
        self.pc += 2 # increase to next instruction
    
    def handle_call(self,pc): #call
        self.SP -= 1 #decrement stack counter
        self.ram[self.SP] = self.pc + 2 #address of the instruction directly after CALL is pushed onto the stack -- used to return to 
        address = self.ram_read(pc + 1) # save given address to variable
        self.pc = self.memory[address] # go to that register address and run that function

    def handle_cmp(self,pc):
        operand_a = self.ram_read(pc + 1) #save arg1 (register number) to variable
        num_1 = self.memory[operand_a] # access that register's value and save to variable

        operand_b = self.ram_read(pc + 2) #save arg1 (register number) to variable
        num_2 = self.memory[operand_b] #access that rigister's value and save to variable

        if num_1 == num_2:
            self.flag = 0b00000001
        elif num_1 < num_2:
            self.flag = 0b00000100
        elif num_1 > num_2:
            self.flag = 0b0000010
    
    def handle_jump(self,pc):
        address = self.ram_read(pc + 1)
        self.pc = address

    def handle_jeq(self,pc):
        if self.flag == 0b00000001:
            address = self.ram(pc + 1)
            self.pc = address
        else:
            self.pc += 2


    def handle_ret(self,pc): #ret
        self.pc = self.ram[self.SP] #set the pc to the value from top of stack (where you left off)
        self.SP += 1 #increase stack pointer
       
        
    def run(self):
        """Run the CPU."""
        
        while not self.halted:
            instruction = self.ram_read(self.pc)
            self.branchtable[instruction](self.pc)
       
    def ram_read(self, mar):
        return self.ram[mar]

    def ram_write(self, mdr, value):
        self.ram[mdr] = value
        
