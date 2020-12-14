"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b01000101
POP = 0b01000110

SP = 7 

class CPU:
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.pc = 0
        self.reg = [0] * 8
        self.reg[7] = 0xF4 #refer PowerON state in Spec
        self.running = True

    def ram_read(self,addr):
        return self.ram[addr]

    def ram_write(self,val,addr):
        self.ram[addr] = val

    def load(self,filename):
        """Load a program into memory."""

        address = 0
       # program = []
        try: 
            with open(filename) as f:
                for line in f:
                    comment_split = line.split("#")
                    maybe_binary_number = comment_split[0]
                    try:
                        x = int(maybe_binary_number, 2)
                        self.ram_write(x, address)
                        address += 1
                    except:
                        continue
        except FileNotFoundError:
            print("Cannot find this file..")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        # if op == "ADD":
        #     self.reg[reg_a] += self.reg[reg_b]
        if op == MUL: 
            self.reg[reg_a] *= self.reg[reg_b]
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


    def num_of_operands(self, instruction_to_execute):
        return ((instruction_to_execute >> 6) & 0b11) + 1

    def run(self):
        """Run the CPU."""
        
        #self.load()
        while self.running:
            instruction_to_excecute = self.ram[self.pc]
            operand_a = self.ram_read(self.pc+1)
            operand_b = self.ram_read(self.pc+2)
            if instruction_to_excecute == LDI:
                self.reg[operand_a] = operand_b
                self.pc += self.num_of_operands(instruction_to_excecute)
            elif instruction_to_excecute == PRN:
                reg = self.reg[operand_a]
                print (reg)
                self.pc += self.num_of_operands(instruction_to_excecute)
            elif instruction_to_excecute == HLT:
                self.running = False
                self.pc += self.num_of_operands(instruction_to_excecute)
            elif instruction_to_excecute == MUL:
                self.alu(instruction_to_excecute,operand_a,operand_b)
                self.pc += self.num_of_operands(instruction_to_excecute)
            elif instruction_to_excecute == PUSH:
                self.reg[SP] -=1 # decrement the stack pointer
                self.ram_write(self.reg[operand_a],self.reg[SP])
                self.pc += self.num_of_operands(instruction_to_excecute)
            elif instruction_to_excecute == POP:
                self.reg[operand_a] = self.ram_read(self.reg[SP])
                self.reg[SP]+=1
                self.pc += self.num_of_operands(instruction_to_excecute)
            else:
                print ("idk what to to")
                pass

   
        
