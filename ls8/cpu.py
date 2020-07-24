"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.fl= [0] * 8
        self.pc = 0
        self.ram = [0] * 256
        self.isRunning = False
        #stack pointer
        self.sp= 7
        self.reg[self.sp]= 0xF4
        #TODO set up branch table

    instructionDefs = {
        'HLT': 0b00000001,
        'LDI': 0b10000010,
        'PRN': 0b01000111,
        'MULT': 0b10100010,
        'PUSH': 0b01000101,
        'POP': 0b01000110,
        'CALL': 0b01010000,
        'RET': 0b00010001,
        'ADD': 0b10100000
    }

    def ram_read(self, MAR):
        storedValue = self.ram[MAR]
        return storedValue

    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR

    def load(self):
        """Load a program into memory."""

        address = 0
        try: 
            with open(sys.argv[1]) as f:
                for line in f:
                    try:
                        line = line.split('#', 1)[0]

                        line = int(line, 2)
                        self.ram_write(line, address)
                        address += 1
                    except ValueError:
                        pass

        except FileNotFoundError:
            print(f"Couldn't find file {sys.argv[1]}")

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        # elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            # self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def stackPush(self, value):
        # 1. Decrement the `SP`.
        self.reg[self.sp]-= 1

        pointer= self.reg[self.sp]
        self.ram_write(value, pointer)
    
    def stackPop(self):
        pointer= self.reg[self.sp]
        value= self.ram_read(pointer)
        # 2. Increment `SP`.
        self.reg[self.sp]+= 1
        return value

    def run(self):
        """Run the CPU."""
        self.isRunning = True

        # run the operations
        while self.isRunning == True:
            IR= self.ram[self.pc]
            
            # grab the set pc bit(4th bit)
            setsPcMask= IR & 0b00010000
            setsPc= setsPcMask >> 4

            if IR >> 6 == 2:
                operand_a= self.ram_read(self.pc + 1)
                operand_b= self.ram_read(self.pc + 2)
            elif IR >> 6 == 1:
                operand_a= self.ram_read(self.pc + 1)

            # # HLT
            # # no operands
            if IR == self.instructionDefs['HLT']:
                self.isRunning= False

            # LDI
            # takes 2 operands
            elif IR == self.instructionDefs['LDI']:
                self.reg[operand_a] = operand_b
                if setsPc ==  0:
                    self.pc += 3

            # PRN
            # takes one operand
            elif IR == self.instructionDefs['PRN']:
                if setsPc ==  0:
                    self.pc += 2
                print(self.reg[operand_a])
            
            # MULT
            # takes 2 operands
            elif IR == self.instructionDefs['MULT']:
                product= self.reg[operand_a] * self.reg[operand_b]
                self.reg[operand_a]= product
                if setsPc ==  0:
                    self.pc+= 3

            elif IR == self.instructionDefs['ADD']:
                self.alu('ADD', operand_a, operand_b)
                self.pc+= 3

            # PUSH
            # takes one operand
            elif IR == self.instructionDefs['PUSH']:
                value= self.reg[operand_a]
                self.stackPush(value)

                if setsPc ==  0:
                    self.pc+= 2

            # POP
            # takes one operand
            elif IR == self.instructionDefs['POP']:
                value= self.stackPop()
                self.reg[operand_a]= value

                if setsPc ==  0:
                    self.pc+=2

            # CALL
            # takes one operand
            #sets the pc
            elif IR == self.instructionDefs['CALL']:
                isntrAddr= self.pc + 2

                self.stackPush(isntrAddr)

                regNum= operand_a
                subAddr= self.reg[regNum]
                self.pc= subAddr


            # RET
            # takes no operands
            elif IR == self.instructionDefs['RET']:
                retAddr= self.stackPop()
                self.pc= retAddr

            else:
                print('invalid inst')
                self.isRunning = False

