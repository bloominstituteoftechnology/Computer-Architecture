"""CPU functionality."""
import re
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 7 # Variables for cpu to use with instructions. Register
        self.reg.append(0b11110100) # F4 in binary, used for sp
        self.sp = self.reg[7] # Stack Pointer, address to top stack, or F4
        self.ram = [None] * 256 # memory slots to keep track of variables
        self.pc = 0 # pointer to track operations in register. Program Counter
        self.running = True
        self.branchtable = {

        }

    def ram_read(self, MAR): # Memory Address Register
        # get the value at ram address
        return self.ram[MAR]
    
    def ram_write(self, MAR, MDR): # Memory Data Register
        # write over a specified address in ram
        self.ram[MAR] = MDR
        print(f"Address: {MAR} = {MDR}")

    def load(self, argument):
        """Load a program into memory.
        Bonus: check to make sure the user has put a command line argument
         where you expect, and print an error and exit if they didn’t."""
        try:
            with open(argument, "r") as f:
               program = f.read()

            instructions = re.findall(r'\d{8}', program) # match first block of numbers
            for address, instruction in enumerate(instructions):
                x = int(instruction, 2)  # Convert binary string to integer
                self.ram[address] = x

                #    if instruction[0].isdigit():
                #         line = instruction.split("#")
        except FileNotFoundError:
            print("Error with file from command line")

        # # For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

    def alu(self, op, reg_a, reg_b):
        """ALU operations. arithmetic logic unit"""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] += -self.reg[reg_b]
        elif op == "MUL":
            product = self.reg[reg_a] * self.reg[reg_b]
            self.reg[reg_a] = product
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
        """
        10000010 # LDI R0,8
        00000000
        00001000
        01000111 # PRN R0
        00000000
        00000001 # HLT
        """
        # should be similar to lecture
        LDI = 0b10000010 # These are instructions we need to translate
        PRN = 0b01000111
        HLT = 0b00000001
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110


        while self.running:
            IR = self.ram_read(self.pc) # Instruction Register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(self.reg)
            # self.trace()
            if IR == HLT:
                self.running = False

            elif IR == LDI: # next value is the pc, one after is the value to set register to
               self.reg[operand_a] = operand_b
               self.pc += 3
               

            elif IR == PRN: # psuedo instr. Print value stored at register
                print(self.reg[operand_a])
                self.pc += 2
            
            elif IR == PUSH: # Decrement Stack Pointer, take register value into RAM
                # Decrement stack pointer
                self.sp += -1

                # Get register number
                reg_num = operand_a
                value = self.reg[reg_num]

                # The stack pointer tells us where to put the value
                self.ram[self.sp] = value

                # move the program counter when done
                self.pc += 2

            elif IR == POP: # Pop value at top of stack from RAM into given register, increment
                # value to pop comes from where the stack pointer is
                value = self.ram[self.sp]

                # pop it into register
                self.reg[operand_a] = value
                self.sp += 1

                # move the program counter when done
                self.pc += 2
                
            elif IR == MUL: # multiply the next two
               self.alu("MUL", operand_a, operand_b)
               self.pc += 3

            else:
                print(f"This whole court is outta order!")
        


