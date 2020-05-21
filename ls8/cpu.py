"""CPU functionality."""

import sys
SP = 7

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8 
        self.ram = [0] * 256 
        self.reg[SP] = 0XF4

    def ram_read(self, mar):
        return self.ram[mar]

    
    def ram_write(self,mar,mdr):
        self.ram[mar] = mdr


    def load(self, prog):
        """Load a program into memory."""

        address = 0

        with open(prog) as program:
            for ins in program:
                ins_split = ins.split('#')
                ins_value = ins_split[0].strip()

                print(f"INS VAL >>>{ins_value}")

                if ins_value == '':
                    continue
                ins_num = int(ins_value, 2)
                print(f"TO RAM {ins_num , address}")
                self.ram_write(address ,ins_num)
                address += 1 



        #For now, we've just hardcoded a program:

        # program = [
        #     # From print8.ls8
        #     0b10000010, # LDI R0,8
        #     0b00000000,
        #     0b00001000,
        #     0b01000111, # PRN R0
        #     0b00000000,
        #     0b00000001, # HLT
        # ]

        # for instruction in program:
        #     self.ram[address] = instruction
        #     address += 1


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
        HLT = 0b00000001
        LDI = 0b10000010
        PRN = 0b01000111
        MUL = 0b10100010
        PUSH = 0b01000101
        POP = 0b01000110
        CALL = 0b01010000
        RET = 0b00010001
        ADD = 0b10100000
        running = True

        while running:
            instruction = self.ram_read(self.pc)
            opr_a = self.ram_read(self.pc + 1)
            opr_b = self.ram_read(self.pc + 2)
            #print(instruction)
            if instruction == HLT:
                running = False
                self.pc +=1
                
            elif instruction == LDI:
                self.reg[opr_a] = opr_b
                self.pc += 3 
            
            elif instruction == PRN:
                print(self.reg[opr_a])
                self.pc += 2
            
            elif instruction == MUL:
                product = self.reg[opr_a] * self.reg[opr_b]
                self.reg[opr_a] = product
                self.pc += 3

            elif instruction == ADD:
                added = self.reg[opr_a] + self.reg[opr_b]
                self.reg[opr_a] = added
                self.pc += 3 

            elif instruction == PUSH:
                data = self.reg[opr_a]
                self.reg[SP] -= 1 
                self.ram_write(self.reg[SP], data)
                self.pc += 2

            elif instruction == POP:
                value = self.ram_read(self.reg[SP])
                self.reg[SP] += 1
                self.reg[opr_a] = value
                self.pc += 2 

            elif instruction == CALL:
                #reg2 = self.ram[opr_a]
                self.reg[SP] -= 1
                self.ram[self.reg[SP]] = self.pc + 2
                self.pc = self.reg[opr_a]

            elif instruction == RET:
                self.pc = self.ram[self.reg[SP]]
                self.reg[SP] += 1 

            else:
                print(f"bad input: {bin(instruction)}")
                running = False
                