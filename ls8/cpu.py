"""CPU functionality."""

import sys

class CPU:
    """Main CPU class."""
    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.sp = 244
        self.fl = 0b000
        self.running = False
        self.advance_pc = True
        self.print_stuff = False
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
        self.branchtable["CALL"] = self.CALL
        self.branchtable["RET"] = self.RET
        self.branchtable["JMP"] = self.JMP
        self.branchtable["DEC"] = self.DEC
        self.branchtable["INC"] = self.INC
        self.branchtable["PRA"] = self.PRA
        self.branchtable["LD"] = self.LD
        self.branchtable["CMP"] = self.CMP
        self.branchtable["JEQ"] = self.JEQ
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
        self.op_codes["CALL"] = 0b01010000
        self.op_codes["RET"] = 0b00010001
        self.op_codes["JMP"] = 0b01010100
        self.op_codes["DEC"] = 0b01100110
        self.op_codes["INC"] = 0b01100101
        self.op_codes["PRA"] = 0b01001000
        self.op_codes["LD"] = 0b10000011
        self.op_codes["CMP"] = 0b10100111
        self.op_codes["JEQ"] = 0b01010101

    def load(self):
        """Load a program into memory."""
        address = 0
        if len(sys.argv) < 2:
            print("Please pass in a second file name: python3 ls8.py second_filename.py")
            sys.exit()
        file_name = sys.argv[1]
        # file_name = "ls8/examples/printstr.ls8"
        try:
            file = open(file_name, "r")
        except FileNotFoundError:
            print(f"{sys.argv[0]}: {sys.argv[1]} file was not found.")
            sys.exit()
        
        for line in file.readlines():
            instruction = line.split("#")[0]
            instruction = instruction.strip()  
            if len(instruction) > 0:
                self.ram_write(address, int(instruction, 2))
                address += 1 
        file.close()
        
    def alu(self, op):
        """ALU operations."""
        if self.op_codes["ADD"] is op:
            self.branchtable["ADD"]()
            if self.print_stuff:
                self.print_out("ADD")
        elif self.op_codes["SUB"] is op:
            self.branchtable["SUB"]()
            if self.print_stuff:
                self.print_out("SUB")
        elif self.op_codes["MUL"] is op:
            self.branchtable["MUL"]()
            if self.print_stuff:
                self.print_out("MUL")
        elif self.op_codes["DIV"] is op:
            self.branchtable["DIV"]()
            if self.print_stuff:
                self.print_out("DIV")
        elif self.op_codes["AND"] is op:
            self.branchtable["AND"]()
            if self.print_stuff:
                self.print_out("AND")
        elif self.op_codes["DEC"] is op:
            self.branchtable["DEC"]()
            if self.print_stuff:
                self.print_out("DEC")
        elif self.op_codes["INC"] is op:
            self.branchtable["INC"]()
            if self.print_stuff:
                self.print_out("INC")
        elif self.op_codes["CMP"] is op:
            self.branchtable["CMP"]()
            if self.print_stuff:
                self.print_out("CMP")
        else:
            raise Exception("Unsupported ALU operation")

    def mutators(self, op):
        """ PC Mutators """
        if op is self.op_codes["CALL"]:
            self.branchtable["CALL"]()
            if self.print_stuff:
                self.print_out("CALL")
        if op is self.op_codes["RET"]:
            self.branchtable["RET"]()
            if self.print_stuff:
                self.print_out("RET") 
        if op is self.op_codes["JMP"]:
            self.branchtable["JMP"]()
            if self.print_stuff:
                self.print_out("JMP")
        if op is self.op_codes["JEQ"]:
            self.branchtable["JEQ"]()
            if self.print_stuff:
                self.print_out("JEQ")

    def standard_op(self, op):
        if op is self.op_codes["LDI"]:
            self.branchtable["LDI"]()
            if self.print_stuff:
                self.print_out("LDI")
        if op is self.op_codes["PRN"]:
            self.branchtable["PRN"]()
            if self.print_stuff:
                self.print_out("PRN")
        if op is self.op_codes["HLT"]:
            self.branchtable["HLT"]()
            if self.print_stuff:
                self.print_out("HLT")
        if op is self.op_codes["POP"]:
            self.branchtable["POP"]()
            if self.print_stuff:
                self.print_out("POP")  
        if op is self.op_codes["PUSH"]:
            self.branchtable["PUSH"]()
            if self.print_stuff:
                self.print_out("PUSH")
        if op is self.op_codes["PRA"]:
            self.branchtable["PRA"]()
            if self.print_stuff:
                self.print_out("PRA")
        if op is self.op_codes["LD"]:
            self.branchtable["LD"]()
            if self.print_stuff:
                self.print_out("LD")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """
        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            # self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def print_out(self, op_code):
        print(f"Code {op_code} ran. Registers: {self.reg}... The flag is {self.fl}, The PC is {self.pc}")

    def run(self):
        """Run the CPU."""
        self.running = True
        while self.running:
            self.advance_pc = True
            IR = self.ram_read(self.pc)
            increase_pc = (IR >> 6) + 1
            if self.PC_MUTATATOR(IR):
                self.mutators(IR)
            elif self.ALU_OP_CODE(IR):
                self.alu(IR)
            else:
                self.standard_op(IR)
            if self.advance_pc:
                self.pc += increase_pc

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
    
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

    def AND(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        x = self.reg[operand_a]
        y = self.reg[operand_b]
        result = x & y
        self.reg[operand_a] = result

    def DIV(self): 
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        x = self.reg[operand_a]
        y = self.reg[operand_b]
        self.reg[operand_a] = x / y

    def POP(self):
        operand_a = self.ram_read(self.sp)
        operand_b = self.ram_read(self.pc + 1)
        self.reg[operand_b] = operand_a
        self.sp += self.op_codes["POP"] >> 6
        
    def PUSH(self, ):
        self.sp -= self.op_codes["PUSH"] >> 6
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.reg[operand_a]
        self.ram_write(self.sp, operand_b)

    def ALU_OP_CODE(self, IR):
        B = IR >> 5
        alu = B & 0b001  
        if alu is 1:
            return True 
    
    def PC_MUTATATOR(self, IR):
        B = IR >> 4
        mutator = B & 0b0001
        if mutator is 1: 
            return True

    def CALL(self):
        operand_a = self.pc + 2
        self.sp -= self.op_codes["PUSH"] >> 6
        self.ram_write(self.sp, operand_a)
        operand_b = self.ram_read(self.pc + 1)
        self.pc = self.reg[operand_b]
        self.advance_pc = False
        
    def RET(self):
        operand_a = self.ram_read(self.sp)
        self.sp += self.op_codes["POP"] >> 6
        self.pc = operand_a
        self.advance_pc = False

    def JMP(self):
        operand_a = self.ram_read(self.pc + 1)
        self.pc = self.reg[operand_a]
        self.advance_pc = False

    def DEC(self):
        operand_a = self.ram_read(self.pc + 1)
        self.reg[operand_a] = self.reg[operand_a] - 1

    def INC(self):
        operand_a = self.ram_read(self.pc + 1)
        self.reg[operand_a] = self.reg[operand_a] + 1

    def PRA(self):
        operand_a = self.ram_read(self.pc + 1)
        print(f"{chr(self.reg[operand_a])}")

    def LD(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        MAR = self.reg[operand_b]
        self.reg[operand_a] = self.ram[MAR]
        
    def CMP(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.fl &= 0b000
        if self.reg[operand_a] ^ self.reg[operand_b] is 0:
            self.fl = 0b00000001
        elif self.reg[operand_a] > self.reg[operand_b]:
            self.fl = 0b00000010
        elif self.reg[operand_a] < self.reg[operand_b]:
            self.fl = 0b00000100   

    def JEQ(self):
        operand_a = self.ram_read(self.pc + 1)
        if self.fl & 1 is 1:
            self.pc = self.reg[operand_a]
            self.advance_pc = False


# cpu = CPU()
# cpu.load()
# cpu.run()
