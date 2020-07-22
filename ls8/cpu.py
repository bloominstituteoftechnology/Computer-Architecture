"""CPU functionality."""

import sys

# op_codes = {
#     "HLT": 0b00000001,
#     "LDI": 0b10000010,
#     "PRN": 0b01000111,
#     "MUL": 0b10100010
# }

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 244
        self.running = False
        self.branchtable = {}
        self.branchtable["LDI"] = self.LDI
        self.branchtable["PRN"] = self.PRN
        self.branchtable["HLT"] = self.HLT
        self.branchtable["MUL"] = self.MUL
        self.branchtable["DIV"] = self.DIV
        self.branchtable["ADD"] = self.ADD
        self.branchtable["SUB"] = self.SUB
        self.branchtable["AND"] = self.AND
        self.branchtable["POP"] = self.POP
        self.branchtable["PUSH"] = self.PUSH
        self.op_codes = {}
        self.op_codes["HLT"] = 0b00000001
        self.op_codes["LDI"] = 0b10000010
        self.op_codes["PRN"] = 0b01000111
        self.op_codes["MUL"] = 0b10100010
        self.op_codes["DIV"] = 0b10100011
        self.op_codes["ADD"] = 0b10100000
        self.op_codes["SUB"] = 0b10100001
        self.op_codes["AND"] = 0b10101000
        self.op_codes["POP"] = 0b01000110
        self.op_codes["PUSH"] = 0b01000101

    def load(self):
        """Load a program into memory."""

        address = 0
        if len(sys.argv) < 2:
            print("Please pass in a second file name: python3 ls8.py second_filename.py")
            sys.exit()
        file_name = sys.argv[1]
        # file_name = "ls8/examples/stack.ls8"
        try:
            file = open(file_name, "r")
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file was not found.")
            sys.exit()
        
        for line in file.readlines():
            instruction = line.split("#", 1)[0].strip()
            # print(f"Instruction: {instruction}")
            if len(instruction) > 5:
                self.ram_write(address, int(instruction, 2))
            address += 1
        file.close()
        # print(f"Random Access Memory: {self.ram}")
        
    def alu(self, op):
        """ALU operations."""

        if self.op_codes["ADD"] is op:
            self.branchtable["ADD"]()
        elif self.op_codes["SUB"] is op:
            self.branchtable["SUB"]()
        elif self.op_codes["MUL"] is op:
            self.branchtable["MUL"]()
        elif self.op_codes["DIV"] is op:
            self.branchtable["DIV"]()
        elif self.op_codes["AND"] is op:
            self.branchtable["AND"]()
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
        self.running = True
        
        while self.running:
            IR = self.ram_read(self.pc)

            if IR is self.op_codes["LDI"]:
                self.branchtable["LDI"]()

            if IR is self.op_codes["PRN"]:
                self.branchtable["PRN"]()
            
            if IR is self.op_codes["HLT"]:
                self.branchtable["HLT"]()
                
            if self.ALU_OP_CODE(IR):
                self.alu(IR)

            if IR is self.op_codes["POP"]:
                self.branchtable["POP"]()
            
            if IR is self.op_codes["PUSH"]:
                self.branchtable["PUSH"]()

            self.pc += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += self.op_codes["LDI"] >> 6

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += self.op_codes["PRN"] >> 6
    
    def HLT(self):
        sys.exit()

    def MUL(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        x = self.reg[operand_a]
        y = self.reg[operand_b]

        result = 0 
        count = 0
        while x:
            if x % 2 is 1:
                result += y << count
            count += 1
            x = int(x / 2)
        self.reg[operand_a] = result 
        self.pc += self.op_codes["MUL"] >> 6

    def ADD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        x = self.reg[operand_a]
        y = self.reg[operand_b]
        while y:
            carry = x & y
            x = x ^ y
            y = carry << 1
        self.reg[operand_a] = x
        self.pc += self.op_codes["ADD"] >> 6
    
    def SUB(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        x = self.reg[operand_a]
        y = self.reg[operand_b]
        if x < y:
            self.reg[operand_a] = x - y
        else:
            while y:
                borrow = (~x) & y
                x = x ^ y
                y = borrow << 1
            self.reg[operand_a] = x
        self.pc += self.op_codes["SUB"] >> 6

    def AND(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        x = self.reg[operand_a]
        y = self.reg[operand_b]
        result = x & y
        self.reg[operand_a] = result
        self.pc += self.op_codes["AND"] >> 6

    def DIV(self): 
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        x = self.reg[operand_a]
        y = self.reg[operand_b]
        self.reg[operand_a] = x / y
        self.pc += self.op_codes["DIV"] >> 6

    def POP(self):
        operand_a = self.ram_read(self.sp)
        operand_b = self.ram_read(self.pc + 1)
        self.reg[operand_b] = operand_a
        self.sp += self.op_codes["POP"] >> 6
        self.pc += self.op_codes["POP"] >> 6
        

    def PUSH(self):
        self.sp -= self.op_codes["PUSH"] >> 6
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.reg[operand_a]
        self.ram_write(self.sp, operand_b)
        self.pc += self.op_codes["PUSH"] >> 6

    def ALU_OP_CODE(self, IR):
        B = IR >> 5
        alu = B & 0b001  
        if alu is 1:
            return True 

cpu = CPU()
cpu.load()
cpu.run()
