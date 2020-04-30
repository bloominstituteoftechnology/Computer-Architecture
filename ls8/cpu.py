"""CPU functionality."""

import sys

HLT = 0x01
LDI = 0x82
PRN = 0x47
MUL = 0xA2
POP = 0x46
PUSH = 0x45
CALL = 0x50
RET = 0x11
ADD = 0xA0

HALTED = 0x80

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = [0] * 256
        self.reg = [0] * 8
        self.reg[7] = 0xF4
        self.pc = 0
        self.fl = 0
        self.branch_table = {
            HLT: self.handle_hlt,
            LDI: self.handle_ldi,
            PRN: self.handle_prn,
            MUL: self.handle_mul,
            POP: self.handle_pop,
            PUSH: self.handle_push,
            CALL: self.handle_call,
            RET: self.handle_ret,
            ADD: self.handle_add
        }
    
    def handle_hlt(self):
        self.fl |= HALTED
    
    def handle_ldi(self, register, immediate):
        self.reg[register] = immediate
    
    def handle_prn(self, register):
        print(self.reg[register])
    
    def handle_mul(self, register_a, register_b):
        self.reg[register_a] = self.reg[register_a] * self.reg[register_b]
    
    def handle_pop(self, register):
        self.reg[register] = self.ram_read(self.reg[7])
        self.reg[7] += 1

    def handle_push(self, register):
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.reg[register])
    
    def handle_call(self, register):
        self.reg[7] -= 1
        self.ram_write(self.reg[7], self.pc + 2)
        self.pc = self.reg[register]

    def handle_ret(self):
        self.pc = self.ram_read(self.reg[7])
        self.reg[7] += 1
    
    def handle_add(self, register_a, register_b):
        self.alu('ADD', register_a, register_b)

    def ram_read(self, mar):
        return self.ram[mar]
    
    def ram_write(self, mar, mdr):
        self.ram[mar] = mdr

    def load(self):
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:
        if len(sys.argv) > 1:
            file_name = sys.argv[1]

            with open(file_name, 'r') as file:
                lines = file.readlines()
                program = []

                for line in lines:
                    split_line = line.split()
                    if len(split_line) > 0 and ord(split_line[0][0]) >= 48 and ord(split_line[0][0]) <= 57:
                        program.append(split_line[0])

                for instruction in program:
                    self.ram[address] = int(instruction, 2)
                    address += 1
        else:
            print('Error: expected a program file as an argument')


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
        while not self.fl & HALTED:
            ir = self.ram_read(self.pc)
            num_operands = (ir & 0xC0) >> 6
            sets_pc = (ir & 0x10) != 0
            
            if num_operands == 0:
                self.branch_table[ir]()
            elif num_operands == 1:
                self.branch_table[ir](self.ram_read(self.pc + 1))
            elif num_operands == 2:
                self.branch_table[ir](self.ram_read(self.pc + 1), self.ram_read(self.pc + 2))
            else:
                print('Invalid instruction given: invalid number of operands!')
                break
            
            if not sets_pc:
                self.pc += num_operands + 1

