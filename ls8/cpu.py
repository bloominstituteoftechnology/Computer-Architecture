"""CPU functionality."""

import sys

op_codes = {
    "HLT": 0b00000001,
    "LDI": 0b10000010,
    "PRN": 0b01000111,
    "MUL": 0b10100010
}

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.pc = 0
        self.running = False
        self.branchtable = {}
        self.branchtable["LDI"] = self.LDI
        self.branchtable["PRN"] = self.PRN
        self.branchtable["HLT"] = self.HLT
        self.branchtable["MUL"] = self.MUL


    def load(self):
        """Load a program into memory."""

        address = 0
        if len(sys.argv) < 2:
            print("Please pass in a second file name: python3 ls8.py second_filename.py")
            sys.exit()
        file_name = sys.argv[1]
        # file_name = "examples/mult.ls8"
        # print(f"File Name: {file_name}")
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
        self.running = True
        
        while self.running:
            IR = self.ram_read(self.pc)
            if IR is op_codes["LDI"]:
                self.branchtable["LDI"]()

            if IR is op_codes["PRN"]:
                self.branchtable["PRN"]()
            
            if IR is op_codes["HLT"]:
                self.branchtable["HLT"]()
                
            if IR is op_codes["MUL"]:
                self.branchtable["MUL"]()

            self.pc += 1

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def LDI(self):
        operand_a = self.ram_read(self.pc + 1)
        operand_b = self.ram_read(self.pc + 2)
        self.reg[operand_a] = operand_b
        self.pc += op_codes["LDI"] >> 6

    def PRN(self):
        operand_a = self.ram_read(self.pc + 1)
        print(self.reg[operand_a])
        self.pc += op_codes["PRN"] >> 6
    
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
        self.pc += op_codes["MUL"] >> 6


cpu = CPU()
cpu.load()
cpu.run()

    