"""CPU functionality."""

import sys
HLT = 0b00000001
LDI = 0b10000010
PRN = 0b01000111
MUL = 0b10100010
class CPU:
    """Main CPU class."""
    def __init__(self):
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.branch_table = {}
        self.branch_table[HLT] = self.handle_hlt
        self.branch_table[LDI] = self.handle_ldi
        self.branch_table[PRN] = self.handle_prn
        self.branch_table[MUL] = self.handle_mul
    def ram_read(self, MAR):
        return self.ram[MAR]
    def ram_write(self, MDR, MAR):
        self.ram[MAR] = MDR
    def load(self):
        """Load a program into memory."""
        address = 0
        with open(sys.argv[1]) as f:
            for line in f:
                string_val = line.split("#")[0].strip()
                if string_val == '':
                    continue
                v = int(string_val, 2)
                self.ram[address] = v
                address += 1
    def alu(self, op, reg_a, reg_b):
        """ALU operations."""
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "SUB":
            self.reg[reg_a] -= self.reg[reg_b]
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
        
    def handle_push(self):

    def handle_pop(self):

    
    def handle_hlt(self):
        print("***** HALT COMMAND INITIATED ******")
        running = False
        self.pc += 1
        sys.exit()
    def handle_ldi(self, reg_a, reg_b):
        print("******** LDI COMMAND INITIATED *******")
        self.reg[reg_a] = reg_b
        print(self.reg[reg_a], "--- After")
        self.pc += 3
        print(self.reg, "--- self.reg")
    def handle_prn(self, reg_a):
        print("******* PRINT COMMAND INITIATED *********")
        print(self.reg[reg_a])
        self.pc += 2
    def handle_mul(self, reg_a, reg_b):
        print("******** MULTIPLY COMMAND INITIATED ********")
        self.alu("MUL", reg_a, reg_b)
        self.pc += 3
    def run(self):
        """Run the CPU."""
        running = True
        while running == True:
            instruction = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            if instruction == LDI:
                self.branch_table[instruction](reg_a, reg_b)
                print(reg_a, reg_b)
            elif instruction == MUL:
                self.branch_table[instruction](reg_a, reg_b)
            elif instruction == PRN:
                self.branch_table[instruction](reg_a)
            else:
                self.branch_table[instruction]()
            # instruction = LDI
            # self.branch_table[instruction](reg_a, reg_b)
            # instruction = MUL
            # self.branch_table[instruction](reg_a, reg_b)
            # instruction = PRN
            # self.branch_table[instruction](reg_a)
            # instruction = HLT
            # self.branch_table[instruction]()
        running = False
        sys.exit()
        '''while running == True:
            instruction = self.ram_read(self.pc)
            reg_a = self.ram_read(self.pc + 1)
            reg_b = self.ram_read(self.pc + 2)
            if instruction == HLT:
                print("***** HALT COMMAND INITIATED ******")
                running = False
                self.pc += 1
                sys.exit()
            elif instruction == LDI:
                print("******** LDI COMMAND INITIATED *******")
                print(self.reg, "--- self.reg")
                print(reg_a, "--- reg_a")
                print(reg_b, "--- reg_b")
                print(self.reg[reg_a], "--- Before")
                self.reg[reg_a] = reg_b
                print(self.reg[reg_a], "--- After")
                self.pc += 3
                print(self.reg, "--- self.reg")
            elif instruction == PRN:
                print("******* PRINT COMMAND INITIATED *********")
                print(self.pc, "--- self.pc")
                print(self.reg, "--- self.reg")
                print(reg_a, "--- reg_a")
                print(self.reg[reg_a])
                self.pc += 2
            elif instruction == MUL:
                print("******** MULTIPLY COMMAND INITIATED ********")
                print(self.reg, " --- self.reg")
                print(self.reg[reg_a], " -- reg_a")
                print(self.reg[reg_b], " -- reg_b")
                self.alu("MUL", reg_a, reg_b)
                mul = self.reg[reg_a] * self.reg[reg_b]
                print(mul)
                self.pc += 3
            else:
                #print(f'unknown instruction {instruction} at address {pc}')
                running = False
                sys.exit()'''

