"""CPU functionality."""

import sys

    

class CPU:
    """Main CPU class."""

    def __init__(self):
        self.reg = [0] * 8 # 8 registers
        self.ram = [0] * 256 # memory of 256 bit
        self.program_counter = 0
        self.running = False 
        # class variable for branch table
        # stack pointer starts at 7 
        stack_pointer = 7 
        instruction_branch_table = {
            "LDI" : 0b10000010,
            "PRN" : 0b01000111,
            "HLT" : 0b00000001,
            "MULT" : 0b10100010,
            "PUSH" : 0b01000101,
            "POP" : 0b01000110,
            "CALL" : 0b01010000,
            "RET" : 0b00010001,
        }
    def load(self, filename):
        """ 
        load a program into ram, use run to run it

        """
        counter = 0 
        with open(filename, 'r') as f:
            program = f.readlines()
            for line in program:
                line = line.split('#') # ignore comments
                line = line[0].strip()

                if line =='': # ignore newlines
                    continue
                self.ram[counter] = int(line, 2)
                counter += 1
    
    # load thing at b into register at a        
    def LDI(self, a, b):
        self.reg[a] = b 
    # print contents of thing at a 
    def PRN(self, a, b):
        print(f'contents of reg at b {self.reg[a]}')
    # halt program by set running to False
    # since run while loop checks for this 
    def HLT(self):
        self.running = False
    def ADD(self, a, b):
        self.alu("ADD", a, b)
    def MUL(self, a, b):
        self.alu("MUL", a, b)

# MAR contains the address that is being read or written to. 
# he MDR contains> the data that was read or the data to write.
    
    # return address in RAM
    def ram_read(self, MAR) -> str:
        return self.ram[MAR]

    # write to RAM, return nothing
    def ram_write(self, MAR, MDR) -> None:
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]    
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.program_counter,
            #self.fl,
            #self.ie,
            self.ram_read(self.program_counter),
            self.ram_read(self.program_counter + 1),
            self.ram_read(self.program_counter + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    # hard coded program
        #     # program = [
        #     # From print8.ls8          
        #     0b10000010,  # LDI R0,8         
        #     0b00000000,  # NOP: Do nothing for this instruction.            
        #     0b00001000,  # this is the number 8        
        #     0b01000111,  # PRN R0          
        #     0b00000000,  # NOP: Do nothing for this instruction.          
        #     0b00000001,  # HLT         
        # ]          

    # execute the instructions stored in self.ram 
    def run(self):
        self.running = True

        while self.running:

            IR = self.ram_read(self.program_counter)

            if IR == 0b10000010: #LDI
                operand_a = self.ram_read(self.program_counter + 1)
                operand_b = self.ram_read(self.program_counter + 2)
                self.ram_write(operand_b, operand_a)
                self.program_counter += 3
            elif IR == 0b01000111: #PRN
                operand_a = self.ram_read(self.program_counter + 1)
                self.ram_write(operand_b, operand_a)
                print(f'printing... {self.ram[operand_a]}')           
                self.program_counter += 2

            elif IR == 0b00000001: #HLT
                self.running = False
                print("Program Halted")
            else:
                print("Unknown Instruction")
                self.running = False