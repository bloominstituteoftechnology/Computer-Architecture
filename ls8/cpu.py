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
        self.E_flag = 0
        self.L_flag = 0
        self.G_flag = 0
        self.branchtable = {
            0b10100000: self.ADD,
            0b10000010: self.LDI,
            0b01000111: self.PRN, 
            0b00000001: self.HLT, 
            0b10100010: self.MUL, 
            0b01000101: self.PUSH,
            0b01000110: self.POP,
            0b01010000: self.CALL,
            0b00010001: self.RET,
            0b10100111: self.CMP,
            0b01010100: self.JMP,
            0b01010101: self.JEQ,
            0b01010110: self.JNE
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

            instructions = re.findall(r'\d{8}', program) # match 8 digit numbers
            for address, instruction in enumerate(instructions):
                x = int(instruction, 2)  # Convert binary string to integer
                self.ram[address] = x

        except FileNotFoundError:
            print("Error with file from command line")


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

        while self.running:
            IR = self.ram_read(self.pc) # Instruction Register
            operand_a = self.ram_read(self.pc + 1)
            operand_b = self.ram_read(self.pc + 2)
            # print(self.reg)
            #self.trace()
            if IR in self.branchtable:
                self.branchtable[IR](operand_a, operand_b)

            else:
                print(f"This whole court is outta order!")
                self.running = False

    def ADD(self, operand_a, operand_b):
        self.alu("ADD", operand_a, operand_b)
        self.pc += 3

    def CALL(self, operand_a, operand_b):
        # get ret address of next function
        return_address = self.pc + 2
        # operand_b
        # We can't use the regular PUSH because that pushed from register
        self.PUSH_ANY(return_address)
        # Set PC to subroutin address
        self.pc = self.reg[operand_a]

    def CMP(self, operand_a, operand_b): 
        if self.reg[operand_a] == self.reg[operand_b]:
            self.L_flag = 0
            self.G_flag = 0
            self.E_flag = 1 # I think you might have to clean up others to 0
        if self.reg[operand_a] < self.reg[operand_b]:
            self.G_flag = 0
            self.E_flag = 0
            self.L_flag = 1
        if self.reg[operand_a] > self.reg[operand_b]:
            self.E_flag = 0
            self.L_flag = 0
            self.G_flag = 1

        self.pc += 3

    def HLT(self, operand_a, operand_b):
        self.running = False

    def JEQ(self, operand_a, operand_b):
        if self.E_flag == 1:
            self.JMP(operand_a, operand_b)
        else:
            self.pc += 2
    
    def JNE(self, operand_a, operand_b):
        if self.E_flag == 0:
            self.JMP(operand_a, operand_b)
        else:
            self.pc += 2

    def JMP(self, operand_a, operand_b):
        address = self.reg[operand_a]
        self.pc = address

    def LDI(self, operand_a, operand_b): 
        # opA is the value, opB is the value to set
        self.reg[operand_a] = operand_b
        self.pc += 3
               
    def MUL(self, operand_a, operand_b): # multiply the next two
        self.alu("MUL", operand_a, operand_b)
        self.pc += 3

    def POP(self, operand_a, operand_b):
        # sp is the value you want to put into the register
        value = self.ram[self.sp]
        # opA is the register you want to store into
        self.reg[operand_a] = value
        self.sp += 1
        self.pc += 2

    def PRN(self, operand_a, operand_b): 
        # opA is the reg index to print
        print(self.reg[operand_a])
        self.pc += 2
            
    def PUSH(self, operand_a, operand_b): # push register value onto stack
        # Decrement stack pointer
        self.sp += -1
        # opA tells us which register value, stack pointer is where to store
        self.ram[self.sp] = self.reg[operand_a]
        # move the program counter when done
        self.pc += 2

    def PUSH_ANY(self, value):
        self.sp += -1
        self.ram[self.sp] = value

    def RET(self, operand_a, operand_b):
        # pop value from stack into pc
        # same problem with pop fn and register
        self.pc = self.ram[self.sp]
        self.sp += 1




