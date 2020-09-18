"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.SP = 7 # this is our stack pointer position in the registers
        self.ram = [0] * 256
        self.registers = [0] * 8 # registers 0 - 7
        self.registers[self.SP] = 0xF4 #the seventh register is where the stack pointer starts at.
        self.pc = 0 # Program Counter, address of the currently executing 
        # the registers are "variables" and there are
        # a fixed number of them (8)
        self.flag = 0b00000000


        self.HLT = 0b00000001
        self.PRN = 0b01000111
        self.LDI = 0b10000010 
        self.MUL = 0b10100010
        self.PUSH = 0b01000101
        self.POP = 0b01000110

        # Sprint Challenge Additions
        self.CMP = 0b10100111
        self.JMP = 0b01010100
        self.JEQ = 0b01010101
        self.JNE = 0b01010110


    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        # args = sys.argv[0]
        # print(args, 'the first argument in sys.argv')
        args2 = sys.argv[1]
        # print(args2, 'second argument in sys.argv')




        with open(f"{args2}", 'r') as pro_file:

            for line in pro_file:
                # print(line)

                # we will check each line, take out the notes and save those program numbers in
                # our programs array. 
                split_line = line.split('#')
                # print(split_line) # returns ['binary number', 'comments from #']
                bit = split_line[0].strip() #takes care of white space from first line 


                if bit == "":
                    continue

                try:
                    instruction = int(bit,2) # this turns our string of bit code, into an actual 
                    # binary digit, which is what we want

                except ValueError:
                    print(f"Invalid value: {bit}")
                
                self.ram[address] = instruction
                address += 1

        # print(args2[0], 'second argument in second spot')
        # program = [
            # From print8.ls8
            # 0b10000010, # LDI R0,8
            # 0b00000000,
            # 0b00001000,
            # 0b01000111, # PRN R0
            # 0b00000000,
            # 0b00000001, # HLT
        # ]

        # print(program)

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "CMP":
            if self.registers[reg_a] > self.registers[reg_b]:
                self.flag = 0b00000010

            elif self.registers[reg_a] < self.registers[reg_b]:
                self.flag = 0b00000100

            else:
                self.flag = 0b00000001

        else:
            raise Exception("Unsupported ALU operation")

    def ram_read(self, address):
        return self.ram[address]

    def ram_write(self, value, address):
        #overwrite in the ram position, or place this value at that position
        self.ram[address] = value

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


        operating = True
        while operating:
            ir = self.ram_read(self.pc) # Instruction register reading the current item in the PC

            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)

            if ir == self.HLT:
                operating = False
                self.pc += 1

            elif ir == self.PRN:
                print(self.registers[operand_a])
                self.pc += 2

            elif ir == self.LDI:
                self.registers[operand_a] = operand_b
                self.pc += 3

            elif ir == self.MUL:
                
                self.registers[operand_a] = self.registers[operand_a] * self.registers[operand_b]
                self.pc += 3
            
            elif ir == self.PUSH:
                # to push an item, we got to decrement the stack pointer
                self.registers[self.SP] -= 1

                # then we must get the reg num to push , 
                reg_num = self.ram_read(self.pc + 1)


                # we will set a value variable that is the value of the register num 
                # in the list of registers and then we will work on adding that value to 
                # be the value that is placed where the top of the stack is
                value = self.registers[reg_num]

                # now we will take that value and place it in the SP address
                top_of_stack_addr = self.registers[self.SP]
                self.ram[top_of_stack_addr] = value

                # increment our PC 
                self.pc += 2
       
            elif ir == self.POP:
                # we must get the register number of what we want to pop
                reg_num = self.ram_read(self.pc + 1)

                # get the address of top of stack
                top_of_stack_addr = self.registers[self.SP]

                # get the value that is at the top of the stack
                value = self.ram_read(top_of_stack_addr)

                # we then want to take that value and it to the register number we got

                self.registers[reg_num] = value

                # increment our SP
                self.registers[self.SP] += 1
                 
                # lastly we will increment the PC 
                # to continue well with the program
                self.pc += 2

            elif ir == self.CMP:
                # CMP is an operation handled in the ALU
                self.alu('CMP', operand_a, operand_b)

                self.pc += 3

            elif ir == self.JMP:
                # we will check the current address stored in the 
                # given register 
                cur_reg = operand_a
                # then we will set our PC to the address 
                # stored in the given register
                self.pc = self.registers[cur_reg]

            elif ir == self.JEQ:
                # we have to check if the flag is set to equal, or true
                # then we go ahead and jump to the address
                # stored in the given register

                if self.flag == 0b00000001:

                    # the address is operand a that we have above

                    self.pc = self.registers[operand_a]

                # else we will jump 2 on our program counter
                else:
                    self.pc += 2

            elif ir == self.JNE:
                # if the E flag is clear or false, we will jump to the address stored in the given 
                # register, if not we will jump 2 on our PC
                if self.flag != 0b00000001:

                    # the register address is operand a
                    self.pc = self.registers[operand_a]

                else:
                    self.pc += 2



