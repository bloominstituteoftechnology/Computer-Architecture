"""CPU functionality."""

import sys

LDI = 0b10000010
PRN = 0b01000111
HLT = 0b00000001

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.ir = 0
        self.running = True
        self.commands = {
            0b10000010: self.ldi,
            0b01000111: self.prn,
            0b00000001: self.hlt
            
        }


    def ram_read(self, address):
        return self.ram[address]
    
    def ram_write(self,value, address):
        self.ram[address] = value

    def load(self):
        """Load a program into memory."""

        address = 0

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

    def run(self):
        """Run the CPU."""


        while self.running:
            ir = self.ram[self.pc]

            if ir == LDI:
                operand_a = self.ram_read(self.pc + 1)
                operand_b = self.ram_read(self.pc + 2)
                
                self.reg[operand_a] = operand_b
                self.pc += 3

            elif ir == PRN:
                operand_a = self.ram_read(self.pc + 1)
                print(self.ram_read(operand_a))
                self.pc +=2

            elif ir == HLT:
                self.running = False
                self.pc += 1
                # sys.exit()
            
            else:
                print(f'failure with {ir} at address {self.pc}')
                sys.exit()
                

    # def runV2(self):
    #     """Run the CPU."""


    #     while self.running:
    #         ir = self.ram[self.pc]

    #         operand_a = self.ram_read(self.pc +1)
    #         operand_b = self.ram_read(self.pc +2)

    #         try:
    #             operation_output = self.commands[ir](operand_a,operand_b)
    #             running = operation_output[0]
    #             self.pc += operation_output[1]

    #         except Exception as e:
    #             print(e)
    #             print(f"command: {ir}")
    #             sys.exit()
    
    # def ldi(self,operand_a,operand_b):
    #     self.reg[operand_a] = operand_b
    #     return(True, 3) #this is to check that it is still runnig [0] and how many pc spots to hop [1] in this case still runing is true and we hop 3 spots forward.

    # def prn(self, operand_a, operand_b):
    #     print(self.reg[operand_a])
    #     return(True, 2)
    
    # def hlt(self, operand_a, operand_b):
    #     return(False, 0)

    
