"""CPU functionality."""

import sys

HLT  =  0b00000001
MUL  =  0b10100010
LDI  =  0b10000010
PRN  =  0b01000111
PUSH =  0b01000101
POP  =  0b01000110

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.reg = [0] * 8
        self.ram = [0] * 256
        self.pc = 0
        self.registers = [0] * 8
        self.SP = 7

        self.operations = {}
        self.operations[HLT] = self.handle_HLT
        self.operations[LDI] = self.handle_LDI
        self.operations[MUL] = self.handle_MUL
        self.operations[PRN] = self.handle_PRN
        self.operations[PUSH] = self.handle_PUSH
        self.operations[POP] = self.handle_POP
        

    

    def load(self, file_name):
        """Load a program into memory."""

        address = 0
        # For now, we've just hardcoded a program:

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
        try:
            with open(file_name) as file:
                for line in file:
                    split_file = line.split("#")[0]
                    comm = split_file.strip()
                    if comm == "":
                        continue
                    instruction = int(comm, 2)
                    self.ram[address] = instruction
                    address += 1
        except FileNotFoundError:
            print(f"{sys.argv[0]} {sys.argv[1]} file not found")
            sys.exit()

    def ram_read(self, MAR):
        return self.ram[MAR]

    def ram_write(self, MAR, MDR):
        self.ram[MAR] = MDR

    def alu(self, op, reg_a, reg_b):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        #elif op == "SUB": etc
        else:
            raise Exception("Unsupported ALU operation")

    def handle_HLT(self):
        self.running = False

    def handle_LDI(self):
        op_a = self.ram_read(self.pc+1)
        op_b = self.ram_read(self.pc+2)
        self.reg[op_a] = op_b
        self.pc += 3

    def handle_MUL(self):
        op_a = self.ram_read(self.pc+1)
        op_b = self.ram_read(self.pc+2)
        self.reg[op_a] = self.reg[op_a]*self.reg[op_b]
        self.pc += 3

    def handle_PRN(self):
        reg_num = self.ram_read(self.pc+1)
        print(self.reg[reg_num])
        self.pc += 2

    def handle_PUSH(self):
        ir = self.ram_read(self.pc)
        val = ir
        op_count = val >> 6  
        ir_len = 1 + op_count
        self.reg[7] -= 1
        reg_num = self.ram_read(self.pc+1)
        val = self.reg[reg_num]
        stack_pointer = self.reg[7]
        self.ram[stack_pointer] = val
        self.pc += ir_len

    def handle_POP(self):
        ir = self.ram_read(self.pc)
        val = ir
        op_count = val >> 6  
        ir_len = 1 + op_count
        stack_pointer = self.reg[7]
        reg_num = self.ram_read(self.pc+1)
        val = self.ram[stack_pointer]
        self.reg[reg_num] = val
        self.reg[7] += 1
        self.pc += ir_len

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
            ir = self.ram_read(self.pc)
            if ir in self.operations:
                fun = self.operations[ir]
                fun()
