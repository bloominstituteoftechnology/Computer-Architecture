"""CPU functionality."""

#hlt halts the program
#ldi load immediate
#prn print
#load "immediate", store a value in a register, or "set this register to this value"

import sys


class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.sp = 7
        self.reg[self.sp] = 0xf4 # where 7 is the stack pointer, the last index in the reg
        self.pc = 0
        self.branchtable = {}
        self.branchtable[0b00000001] = self.operand_HLT
        self.branchtable[0b01000111] = self.operand_PRN
        self.branchtable[0b10000010] = self.operand_LDI
        self.branchtable[0b10100010] = self.operand_MUL
        self.branchtable[0b01000101] = self.operand_PUSH
        self.branchtable[0b01000110] = self.operand_POP
        self.branchtable[0b10100000] = self.operand_ADD


    def load(self):
        """Load a program into memory."""
        params = sys.argv
        if len(params) != 2: # a file is being passed through
            print("usage: file.py filename")
            sys.exit(1)
        if len(params)==2:   
            try:
                with open(params[1]) as f:
                    address = 0
                    for line in f:
                        # print(line)
                        comment_split = line.split("#")
                        # Strip out whitespace
                        num = comment_split[0].strip()
                        # Ignore blank lines
                        if num == '':
                            continue
                        val = int("0b"+num,2)
                        self.ram_write(address, val)
                        address += 1    
            except FileNotFoundError:
                print("File not found")
                sys.exit(2)


    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            
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
    def ram_read(self, mar):
        #memory address registry mar, this might as well be the index
        #memory data register mdr
        #cpu register --> fixed small number of special storage locations built in
        #hexadecimal leading 0x binary leading 0b
        return self.ram[mar]

    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr
        
    def operand_LDI(self,):
        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        self.pc += 3
    def operand_PRN(self,):
        print(self.reg[self.ram_read(self.pc+1)])
        self.pc += 2
    def operand_HLT(self,):
        return  False
    def operand_MUL(self,):
        self.reg[self.ram_read(self.pc+1)]=(self.reg[self.ram_read(self.pc+1)] * self.reg[self.ram_read(self.pc+2)])
        self.pc +=3
    def operand_PUSH(self,):
        self.reg[self.sp] -= 1 # decrements as the stacks starts at the end
        reg_num = self.ram[self.pc + 1]
        register_value = self.reg[reg_num]
        self.ram[self.reg[self.sp]] = register_value
        self.pc += 2 # program counter
    def operand_POP(self,):
        value = self.ram[self.reg[self.sp]]
        reg_num = self.ram[self.pc + 1]
        self.reg[reg_num] = value
        self.reg[self.sp] +=1
        self.pc += 2
    def operand_ADD(self,):
        # print(self.pc, self.sp)
        num_1 = self.reg[self.ram[self.pc+1]]
        num_2 = self.reg[self.ram[self.pc+2]]
        self.reg[self.ram[self.pc+1]] = num_1 + num_2
        self.pc +=3

    def run(self):
        """Run the CPU.""" 
        IR = None
        HLT = 0b00000001
        PRN = 0b01000111
        LDI = 0b10000010
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        while not (self.ram_read(self.pc) is HLT):
            instruction = self.ram_read(self.pc)
            if instruction == CALL:
                # print("call")
                return_address = self.pc + 2
                self.reg[self.sp] -=1
                self.ram[self.reg[self.sp]] = return_address
                reg_num = self.ram[self.pc + 1]
                self.pc = self.reg[reg_num]
            elif instruction == RET:
                # print("ret")
                self.pc = self.ram[self.reg[self.sp]]
                self.reg[self.sp] += 1
            else:
                # print(instruction)
                self.branchtable[instruction]()

# pc = CPU()
# pc.run()
# pc.read_params()
