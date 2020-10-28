"""CPU functionality."""

import sys

HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
PUSH = 0b1000101
POP = 0b1000110
CALL = 0b01010000
RET = 0b00010001
ADD  = 0b10100000
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] *256
        self.pc = 0 #point to the instruction in memory
        self.reg = [0] *8
        self.reg[7] = 0xF4
        self.running = False

    def load(self, filename):
        """Load a program into memory."""
        address = 0
        with open(filename) as f:
            for line in f:
                comment_split = line.split('#')
                num = comment_split[0].strip()
                if num =='':
                    continue
                command = int(num, 2)
                self.ram_write(command, address)
                address +=1
    
        
       
        
        
        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010,# LDI R0,8
            0b00000000,
            0b00001000,
            0b10000010,# LDI R1,9
            0b00000001,
            0b00001001,
            0b10100010, # MUL R0,R1
            0b00000000,
            0b00000001,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1
        

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *=self.reg[reg_b]

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
    def ram_read(self, address):
        '''MAR contain address that is being read or written too'''
        return self.ram[address]
    def ram_write(self, value, address):
        '''MDR contains the data to read or write '''
        self.ram[address] = value
        #self.running = True

    def run(self):
        """Run the CPU."""
        #self.load()
        #running = True
        while not self.running:
           commondToExecute = self.ram[self.pc]
           opr_a = self.ram[self.pc + 1]
           opr_b = self.ram[self.pc + 2]
           if commondToExecute == HLT:
               self.running = True
               self.pc +=1
           elif commondToExecute == LDI:
               self.reg[opr_a] = opr_b
               self.pc +=3
           elif commondToExecute ==PRN:
               print(self.reg[opr_a])
               self.pc +=2
           elif commondToExecute == MUL:
               self.alu('MUL', opr_a, opr_b)
               self.pc +=3
           elif commondToExecute == ADD:
               self.alu('ADD', opr_a, opr_b)
               self.pc +=3
           elif commondToExecute == PUSH:
               #decrement stack pointer
               self.reg[SP] -=1
               #write the value stored in register onto stack
               ValueToStore = self.reg[opr_a]
               self.ram_write(ValueToStore, self.reg[SP])
               self.pc +=2
           elif commondToExecute == POP:
                #save the value on the top of stack onto the register
                topmostValue = self.ram_read(self.reg[SP])
                self.reg[opr_a]=topmostValue
                # increment the stack pointer
                self.reg[SP] +=1
                self.pc +=2
           elif commondToExecute == CALL:
                #store address of the next instruction onto the stack
                self.reg[SP] -=1
                addressOfNextInstruction = self.pc+2
                self.ram_write(addressOfNextInstruction, self.reg[SP])
                #jump to the address of the given register
                regToGetAdressFrom = opr_a
                AddressToJumpTo = self.reg[opr_a]
                self.pc = AddressToJumpTo
           elif commondToExecute == RET:
                #pop the top most value from the stack
                AdressToReturnTo = self.ram_read(self.reg[SP])
                #set the pc to the same value
                self.pc = AdressToReturnTo
                self.reg[SP] +=1
           else:
              print("IDK this instruction Existing")
              sys.exit(1)


                

        

